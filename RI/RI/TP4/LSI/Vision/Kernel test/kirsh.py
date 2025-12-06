import cv2
import numpy as np


img = cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/Kernel test/elevation.png', cv2.IMREAD_GRAYSCALE)


kirsch_kernels = [
    np.array([[5, 5, 5], 
             [-3, 0, -3],
             [-3, -3, -3]]),  # N
    np.array([[5, 5, -3],
             [5, 0, -3],
             [-3, -3, -3]]),  # NW
    np.array([[5, -3, -3], 
              [5, 0, -3], 
              [5, -3, -3]]),  # W
    np.array([[-3, -3, -3], 
              [5, 0, -3], 
              [5, 5, -3]]),  # SW
    np.array([[-3, -3, -3],
              [-3, 0, -3], 
              [5, 5, 5]]),  # S
    np.array([[-3, -3, -3],
              [-3, 0, 5], 
              [-3, 5, 5]]),  # SE
    np.array([[-3, -3, 5], 
              [-3, 0, 5], 
              [-3, -3, 5]]),  # E
    np.array([[-3, 5, 5], 
              [-3, 0, 5], 
              [-3, -3, -3]])   # NE
]


edges = []
for i, k in enumerate(kirsch_kernels):
    edge = cv2.filter2D(img, cv2.CV_32F, k)
    edge = cv2.normalize(edge, None, 0, 255, cv2.NORM_MINMAX)
    edge = edge.astype(np.uint8)
    edges.append(edge)
    cv2.imshow(f"Kirsch Direction {i+1}", edge)

cv2.waitKey(0)
cv2.destroyAllWindows()
