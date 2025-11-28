import cv2
import numpy as np

#embossing : creates a 3d effect , detects intensity change over diagonal or horizontally (here its iver a diagonal)
# highlight positive areas and shadow negative areas

img = cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/Kernel test/cameraman.png', cv2.IMREAD_GRAYSCALE)
img = img.astype(np.float32)


cv2.imshow("Original Elevation", img.astype(np.uint8)) 


hillshade_kernel = np.array([
    [2, 1, 0],
    [1, 1, -1],
    [0, -1, -2]
], dtype=np.float32)


#cv2.CV_32F: output is float32
hillshade = cv2.filter2D(img, cv2.CV_32F, hillshade_kernel)

# normalize for display
hillshade_display = cv2.normalize(hillshade, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)


cv2.imshow("Embossing", hillshade_display)

cv2.waitKey(0)
cv2.destroyAllWindows()

