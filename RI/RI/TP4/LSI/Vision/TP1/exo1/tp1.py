import cv2
import numpy as np
img =cv2.imread('img.png',cv2.IMREAD_GRAYSCALE)
if img is None :
    print('image vide')
    exit(0)
else:
    h,w=img.shape
    imgRes=np.zeros((h,w),np.uint8)
    for y in range(h):
        for x in range(w):
            imgRes[y,x]=255-img[y,x]
    print(imgRes)
    cv2.imwrite('test.png',imgRes)
    cv2.imshow('image gray',img)
    cv2.imshow('imane grayRes',imgRes)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
