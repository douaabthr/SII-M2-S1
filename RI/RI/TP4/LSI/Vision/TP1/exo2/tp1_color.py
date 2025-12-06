import cv2
import numpy as np
img =cv2.imread('img2.png',cv2.IMREAD_COLOR)
h,w,c=img.shape
imgRes=np.zeros(img.shape,np.uint16)
imgRes[:]=img[:]*256 #normalisation
# cv2.resize()
imgRes2=img[0:150,0:200,:]

if img is None:
    print('image vide')
else:
    print('image chargee')

for y in range (h):
    for x in range (w):
        imgRes[y,x]= 255 - img[y,x]

cv2.imwrite('img2.png',imgRes)
cv2.imshow('image 1',img)
cv2.imshow('image 2',imgRes2)
cv2.waitKey(0)
cv2.destroyAllWindows()


#si on divise img/255 makes it float -->try debugging
#try dividion /1

#img was uint8 division /1 -->float64 valeurse entre 0 et 1 
#ex it was 128/1=128>1 so its considered 1 --> blanc only noir thats 0 stays

#si imRes tyoe is uint16 we affect img to it les valeurs ex 255 is too small so they look black
#-->normaliser -->


#imgRes=np.zeros(img.shape,np.uint16)
#imgRes[:]=img[:]*256   si quoi ca and why is it out of bounds
#if imgRes directit creates a new image