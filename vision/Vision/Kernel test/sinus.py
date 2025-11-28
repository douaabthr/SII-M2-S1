import numpy as np
import matplotlib.pyplot as plt
import cv2 

# Load your image
img = cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/Kernel test/cameraman.png', cv2.IMREAD_GRAYSCALE)

# ---------- Define sinusoidal-only kernel ----------
ksize = 21        # size of the kernel
theta = np.pi/4   # 45 degrees
lambd = 5         # wavelength
psi = 0           # phase

x = np.linspace(-10, 10, ksize)
y = np.linspace(-10, 10, ksize)
X, Y = np.meshgrid(x, y)
X_theta = X * np.cos(theta) + Y * np.sin(theta)
sin_kernel = np.cos(2 * np.pi * X_theta / lambd + psi).astype(np.float32)

# ---------- Apply kernel ----------
filtered = cv2.filter2D(img.astype(np.float32), cv2.CV_32F, sin_kernel)
filtered_disp = cv2.normalize(filtered, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

# ---------- Plot original image, kernel, and filtered image ----------
plt.figure(figsize=(15,5))

plt.subplot(1,3,1)
plt.imshow(img, cmap='gray')
plt.title("Original Image")
plt.axis('off')

plt.subplot(1,3,2)
plt.imshow(sin_kernel, cmap='gray')
plt.title("Sinusoidal Kernel (No Gaussian)")
plt.colorbar(fraction=0.046, pad=0.04)

plt.subplot(1,3,3)
plt.imshow(filtered_disp, cmap='gray')
plt.title("Filtered with Sinusoidal Kernel")
plt.axis('off')

plt.show()
