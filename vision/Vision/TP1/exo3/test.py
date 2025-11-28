import cv2
import numpy as np

# Create a blank image
img = np.zeros((200, 200, 3), np.uint8)
cv2.imshow("test", img)

# Wait for a key
q = cv2.waitKeyEx(0)
print("Key code:", q)

cv2.destroyAllWindows()
