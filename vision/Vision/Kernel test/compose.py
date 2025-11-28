import cv2
import numpy as np

# Parameters
ksize = 31          # size of the filter
sigma = 4.0         # Gaussian sigma
theta = np.pi / 2   # orientation: 45 degrees
lambd = 10.0        # wavelength
gamma = 0.5         # aspect ratio
psi = 0             # phase offset

# Create Gabor kernel
gabor_kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)

# Load grayscale image
img = cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/Kernel test/image.png', cv2.IMREAD_GRAYSCALE)

# Apply Gabor filter
filtered_img = cv2.filter2D(img, cv2.CV_8UC3, gabor_kernel)

# Show
cv2.imshow('Gabor Filtered', filtered_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
