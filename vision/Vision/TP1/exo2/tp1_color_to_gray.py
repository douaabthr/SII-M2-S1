import cv2
import numpy as np
img =cv2.imread('img2.png',cv2.IMREAD_COLOR)
h,w,c=img.shape
imgRes=np.zeros(img.shape,img.dtype)
imgRes2=np.zeros(img.shape,img.dtype)
if img is None:
    print('image vide')
else:
    print('image chargee')

b=img[:,:,0]
g=img[:,:,1]
r=img[:,:,2]
# imgRes2=(b+g+r)/3
# change le type a float
#la somme b g r can be > 8 bits so it chanegs the value 
#on peut forcer sur 16 bits
imgRes2=np.uint8((np.uint16(b)+g+r)/3)
# or create new var imgRes2[:] with no cast done directly
#or


cv2.imshow('image 1',img)
cv2.imshow('image 2',imgRes2)
cv2.waitKey(0)
cv2.destroyAllWindows()
