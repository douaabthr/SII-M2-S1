import numpy as np
import cv2
def gaussian_kernel(size, sigma):

    

    # coordinates + center is 0

    #1d array of equally spaced numbers
    ax = np.arange(-(size // 2), size // 2 + 1)
    xx, yy = np.meshgrid(ax, ax)

    # squaresevery element of the arrys at once
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    kernel /= (2 * np.pi * sigma**2)
    

   
    

    return kernel

voisinage=5
G = gaussian_kernel(voisinage, 1.4)
print(G)
print("Sum =", G.sum())
img=cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/Filtre de Gauss/cameraman.png',cv2.IMREAD_GRAYSCALE)
imgGauss=cv2.filter2D(img,-1,G)
cv2.imshow('image',img)
cv2.imshow('gauss',imgGauss)
cv2.waitKey(0)
cv2.destroyAllWindows()
