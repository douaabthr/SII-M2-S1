import numpy as np
import cv2

filtre=np.array([[0,-1,0],
                 [-1,5,-1],
                 [0,-1,0]])

img=cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/Rehaussement contour/cameraman.png',cv2.IMREAD_GRAYSCALE)
cv2.imshow('image',img)
img= img.astype(np.float32)
imgGauss=cv2.filter2D(img,-1,filtre)
imgGauss= (imgGauss - imgGauss.min()) / (imgGauss.max() - imgGauss.min())*255 
imgGauss= imgGauss.astype(np.uint8)

cv2.imshow('rehaussement',imgGauss)
cv2.waitKey(0)
cv2.destroyAllWindows()
