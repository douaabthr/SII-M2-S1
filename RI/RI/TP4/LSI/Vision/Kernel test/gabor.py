import cv2
import numpy as np
import matplotlib.pyplot as plt   


# gabor detect patterns and textures i na specific orientation and frequcy 


# Gauss is for smoothing 

# FONCTION sinusoïdale (with z) part is what detects textures and edges alongside a specific DIRECTION and FREQUENCY 


# sinus is continious and goes forever, so we use gaussian to localize it 
# it doesnt tell where it happens 

# Notice that without the Gaussian, the filter affects the entire image globally,
#  so the output looks “repetitive” and ---------doesn’t highlight local texture-----!!!!!.




# pi = 180
# pi/90

# Parameters
ksize = 21       # size of the kernel
sigma = 5        # standard deviation of Gaussian
theta = np.pi /2 # 45 degrees orientation
lambd = 10       # wavelength
gamma = 0.5      # aspect ratio
psi = 0          # phase offset

# Create Gabor kernel
gabor_kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)

# Load grayscale image
img = cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/Kernel test/cameraman.png', cv2.IMREAD_GRAYSCALE)

# Apply kernel
filtered = cv2.filter2D(img, cv2.CV_32F, gabor_kernel)

# Normalize for display
filtered_disp = cv2.normalize(filtered, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# Show
plt.figure(figsize=(12,4))
plt.subplot(1,3,1); plt.imshow(img, cmap='gray'); plt.title('Original')
plt.subplot(1,3,2); plt.imshow(gabor_kernel, cmap='gray'); plt.title('Gabor Kernel')
plt.subplot(1,3,3); plt.imshow(filtered_disp, cmap='gray'); plt.title('Gabor Filtered')
plt.show()
