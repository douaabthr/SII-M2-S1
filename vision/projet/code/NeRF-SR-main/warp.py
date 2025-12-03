import math
import torch
import numpy as np
import glob
import os
from PIL import Image
from torchvision import transforms as T
from tqdm import tqdm

from data.base_dataset import BaseDataset
from models.utils import *
from utils.colmap import read_cameras_binary, read_images_binary, read_points3d_binary
from data.llff_dataset import normalize, average_poses, center_poses, create_spiral_poses, create_spheric_poses

class LLFFDataset():

    def __init__(self, root_dir, result_dir, width, height):
        self.root_dir = root_dir
        self.result_dir = result_dir
        self.split = 'train'
        self.img_wh = (width, height)
        self.spheric_poses = False

        self.define_transforms()
        self.read_meta()
        self.white_back = False

    def define_transforms(self):
        self.transform = T.ToTensor()

    def read_meta(self):
        # --- Step 1: read cameras.bin ---
        camdata = read_cameras_binary('C:/Users/USER/Downloads/Test-images-COLMAP-20251129T161104Z-1-001/Test-images-COLMAP/sparse/0/cameras.bin')
        H = camdata[1].height
        W = camdata[1].width
        self.focal = camdata[1].params[0] * self.img_wh[0] / W

        # --- Step 2: read images.bin and poses ---
        imdata = read_images_binary('C:/Users/USER/Downloads/Test-images-COLMAP-20251129T161104Z-1-001/Test-images-COLMAP/sparse/0/images.bin')
        image_names_sorted = sorted([imdata[k].name for k in imdata])
        perm = np.argsort(image_names_sorted)

        self.image_paths = [os.path.join(self.root_dir, 'images', name) for name in image_names_sorted]

        w2c_mats = []
        bottom = np.array([0, 0, 0, 1.]).reshape(1, 4)
        for k in imdata:
            im = imdata[k]
            R = im.qvec2rotmat()
            t = im.tvec.reshape(3, 1)
            w2c_mats.append(np.concatenate([np.concatenate([R, t], 1), bottom], 0))
        w2c_mats = np.stack(w2c_mats, 0)
        poses = np.linalg.inv(w2c_mats)[:, :3]

        # --- Step 3: read 3D points and compute visibility & depth ---
        pts3d = read_points3d_binary('/content/drive/MyDrive/NeRF-SR-o/checkpoints/Test-images-COLMAP/sparse/0/points3D.bin')
        n_images = len(poses)
        n_points = len(pts3d)

        pts_world = np.zeros((1, 3, n_points))
        visibilities = np.zeros((n_images, n_points))

        for i, k in enumerate(pts3d):
            pts_world[0, :, i] = pts3d[k].xyz
            for j in pts3d[k].image_ids:
                if j-1 < n_images:
                    visibilities[j-1, i] = 1

        depths = ((pts_world - poses[..., 3:4]) * poses[..., 2:3]).sum(1)

        self.bounds = np.zeros((n_images, 2))
        for i in range(n_images):
            visibility_i = visibilities[i]
            zs = depths[i][visibility_i == 1]

            if zs.size == 0:
                # fallback if no points visible
                self.bounds[i] = [0.1, 1.0]
            else:
                self.bounds[i] = [np.percentile(zs, 0.1), np.percentile(zs, 99.9)]

        # --- Step 4: permute and center poses ---
        poses = poses[perm]
        self.bounds = self.bounds[perm]

        # COLMAP "right down front" -> "right up back"
        poses = np.concatenate([poses[..., 0:1], -poses[..., 1:3], poses[..., 3:4]], -1)
        self.poses, _ = center_poses(poses)

        # ray directions
        self.directions = get_ray_directions(self.img_wh[1], self.img_wh[0], self.focal, True)

        # --- Step 5: prepare reference image ---
        nerf_depths = sorted(glob.glob(os.path.join(self.result_dir, '*fine-depth-ori.npz')))
        for depth_path in tqdm(nerf_depths):
            i = int(os.path.basename(depth_path).split('-')[0])

            if i == 0:
                # --- première image du dossier comme référence ---
                image_files = sorted(os.listdir(os.path.join(self.root_dir, 'images')))
                # filtrer uniquement les fichiers .png (ou .jpg si nécessaire)
                image_files = [f for f in image_files if f.endswith('.png') or f.endswith('.jpg')]
                if len(image_files) == 0:
                    raise RuntimeError(f"Aucune image trouvée dans {os.path.join(self.root_dir, 'images')}")
                
                first_image_path = os.path.join(self.root_dir, 'images', image_files[0])
                image_path = first_image_path
        
                # Charger l'image et transformer
                img = Image.open(image_path).convert('RGB')
                img = img.resize(self.img_wh, Image.LANCZOS)
                img = self.transform(img)
                self.ref_rgbs = img

                # compute ref camera pose
                camdata_ref = read_cameras_binary(os.path.join(self.root_dir, 'sparse/0/cameras.bin'))
                imdata_ref = read_images_binary(os.path.join(self.root_dir, 'sparse/0/images.bin'))
                ref_idx = list(imdata_ref.keys())[0]
                im_ref = imdata_ref[ref_idx]

                R_ref = im_ref.qvec2rotmat()
                t_ref = im_ref.tvec.reshape(3, 1)
                w2c_ref = np.concatenate([np.concatenate([R_ref, t_ref], 1), np.array([0,0,0,1]).reshape(1,4)], 0)
                c2w_ref = np.linalg.inv(w2c_ref)[:3]

                self.ref_c2w = torch.FloatTensor(c2w_ref)
                self.ref_w2c = np.linalg.inv(np.concatenate([self.ref_c2w, np.array([0,0,0,1]).reshape(1,4)], 0))[:3]

            # --- Step 6: warp points to reference frame ---
            c2w = torch.FloatTensor(self.poses[i])
            rays_o, rays_d = get_rays(self.directions, c2w)
            nerf_depth = np.load(depth_path)['arr_0']
            nerf_depth = np.squeeze(nerf_depth, axis=2)

            if not self.spheric_poses:
                rays_o, rays_d = get_ndc_rays(self.img_wh[1], self.img_wh[0],
                                              self.focal, 1.0, rays_o, rays_d)
                nerf_depth = 1 / (1 - nerf_depth + 1e-6)

            K = np.array([[self.focal, 0, 0.5*self.img_wh[0]],
                          [0, -self.focal, 0.5*self.img_wh[1]],
                          [0, 0, 1]])
            i_idx, j_idx = np.meshgrid(np.arange(self.img_wh[0], dtype=np.float32) + 0.5,
                                       np.arange(self.img_wh[1], dtype=np.float32) + 0.5,
                                       indexing='xy')
            coords = np.stack([(i_idx - self.img_wh[0]/2)/self.focal * nerf_depth,
                               -(j_idx - self.img_wh[1]/2)/self.focal * nerf_depth,
                               -nerf_depth], -1)

            warped_img = torch.zeros_like(self.ref_rgbs)

            c2w = c2w.numpy()
            for k in range(coords.shape[0]):
                for l in range(coords.shape[1]):
                    coords[k,l] = c2w[:, :3] @ coords[k,l] + c2w[:, 3]
                    coords[k,l] = self.ref_w2c[:, :3] @ coords[k,l] + self.ref_w2c[:, 3]
                    coords[k,l] /= -coords[k,l,2]
                    coords[k,l,0] = int(coords[k,l,0] * self.focal + self.img_wh[0]/2)
                    coords[k,l,1] = int(coords[k,l,1] * (-self.focal) + self.img_wh[1]/2)

                    if 0 <= coords[k,l,0] < self.img_wh[0] and 0 <= coords[k,l,1] < self.img_wh[1]:
                        warped_img[:, k, l] = self.ref_rgbs[:, int(coords[k,l,1]), int(coords[k,l,0])]

            T.ToPILImage()(warped_img).save(os.path.join(self.result_dir, f'{i}-wrapped.png'))
            np.savez(os.path.join(self.result_dir, f'{i}_locs.npz'), coords)


# ----------------------------
# Example usage
# ----------------------------
width = 504
height = 378

for scene in ['fern']:
    print(scene)
    root_dir = f'D:/nerf_llff_data/{scene}'
    result_dir = f'/content/drive/MyDrive/NeRF-SR-o/checkpoints/nerf-sr/llff-{scene}-{height}x{width}-ni64-dp-ds2/30_test_vis'
    ds = LLFFDataset(root_dir, result_dir, width, height)
