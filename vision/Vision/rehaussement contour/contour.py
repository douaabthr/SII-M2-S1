# Flat zones (no brightness change): Laplacian ≈ 0

# Edges / contours: Large positive or negative values

# Positive = dark → bright transition

# Negative = bright → dark transition 
# 
import cv2
import numpy as np

voisinage = 3  # taille du masque (3x3)



def rehaussement_contour(img):
    h, w = img.shape
    imgReh = np.zeros(img.shape, np.float32)

    # masque de rehaussement (sharpening)
    masque = np.array([[0, -1, 0],
                       [-1,  5, -1],
                       [0,-1, 0]], dtype=np.float32)

    # Parcourir chaque pixel
    for y in range(voisinage // 2, h - voisinage // 2):
        for x in range(voisinage // 2, w - voisinage // 2):
            region = img[y - 1:y + 2, x - 1:x + 2]
            valeur = np.sum(region * masque)
            imgReh[y, x] = valeur 

    # === Normalisation pour éviter le noircissement ===
    # but makes image grayiish and values close to each other
    imgReh = (imgReh - imgReh.min()) / (imgReh.max() - imgReh.min()) * 255
    imgReh = imgReh.astype(np.uint8)


    #OR CLIPPING ?????????????
    # BUT neg become black big 255 become 0


    # imgReh =  np.clip(imgReh, 0, 255).astype(np.uint8)

    # changing tyoe i think mod ex -10 mod 255 = 246

    return imgReh


# === MAIN ===
img = cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/rehaussement contour/cameraman.png', cv2.IMREAD_GRAYSCALE)

cv2.imshow('Image Source', img)

# === Normalisation image source===
# img = (img - img.min()) / (img.max() - img.min())*255 
# img= img.astype(np.uint8)

imgReh = rehaussement_contour(img)

# ALLOW RESIZING
cv2.namedWindow('Rehaussement de Contour (normalisé)', cv2.WINDOW_NORMAL)
cv2.imshow('Rehaussement de Contour (normalisé)', imgReh)

cv2.waitKey(0)
cv2.destroyAllWindows()
