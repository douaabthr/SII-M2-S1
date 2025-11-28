#if max is already 255 and min 0 it wont owrk 
# ex min 20 max 200
# formule: x-min: min-min nous odnne 0 already (decalina a gauche bach ja3adna) et max -min
# diviser max-min 0 yb9a 0  autre 1 (will become 255)
# *255 to get hem back


#sometimes it converts apres division to int automaticall yy u can muklt *255.

# elements du tab hist uint16 cuz it contians count which can be  big not pixels like the image
import cv2
import numpy as np

img=cv2.imread("image.png",cv2.IMREAD_GRAYSCALE)

img[:]=img[:]/2     #to make it more sombre
cv2.imwrite("image.png",img)


if img is None:
    print("erreur de chargemrent")
    exit(0)
h,w=img.shape
min,max=255,0

h,w=img.shape
for y in range(h):
    for x in range(w):
        if(img[y,x]>max):
            max=img[y,x]
        if(img[y,x]<min):
            min=img[y,x]

image_apres=np.zeros(img.shape,img.dtype)
for y in range(h):
    for x in range(w):
        image_apres[y,x]=((img[y,x]-min)/(max-min))*255

print("min: ",min,"max: ",max)
cv2.imshow("image avant",img)
cv2.imshow("image apres",image_apres)

import matplotlib.pyplot as plt
hist_avant = np.zeros((256,1),np.uint16)
for y in range(h):
    for x in range(w):
       hist_avant[img[y,x]]+=1
hist_apres=cv2.calcHist([image_apres],[0],None,[256],[0,255])
# plt.figure()
# plt.title("image normalisée")
# plt.xlabel("niveau gris")
# plt.ylabel("nb_pixels")
# plt.plot(hist_avant)
# plt.plot(hist_apres)
# plt.xlim([0,255])
# plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows ( )
