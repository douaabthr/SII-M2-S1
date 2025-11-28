import cv2
import numpy as np
from random import randrange
print(ord('→'))

# 1-creating image with a random black point
def createImgWithPointRand(h,w) :
    img= np.ones ( (heigthImg , widthImg) ,np.float32)
    #randrange (x) return une valeur aléatoire entre 0 et x
    randPointY,RandPointX = randrange (heigthImg) , randrange (widthImg)
    img [randPointY,RandPointX] =0
    return img

def findBlackPixel(img) :
    h, w = img.shape
    for y in range (h):
       for x in range (w):
           if img[y,x]==0:
                return ( y , x)
           
heigthImg=200
widthImg =400

img = createImgWithPointRand (heigthImg , widthImg)
q='a'
pas=3
(py,px)=findBlackPixel(img)
while(True):
    if 2621440==q and py+pas<heigthImg:    #bas
        img[py,px]=1
        img[py+pas,px]=0
        py=py+pas
    if 2490368==q and py-pas >=0:   #haut
        img[py,px]=1
        img[py-pas,px]=0
        py=py-pas
    if 2424832==q and px-pas >=0:  #gauche
        img[py,px]=1
        img[py,px-pas]=0
        px=px-pas
    if 2555904==q and px+pas < widthImg: #droite
        img[py,px]=1
        img[py,px+pas]=0
        px=px+pas


    imgRes=img.copy()
    imgRes[py-2:py+2,px-2:px+2]=0      # affichage sans boucle !!!!!!!!
    cv2 .imshow( 'image vide',imgRes)
    q= cv2.waitKeyEx(0) # returns ascii code, so for tother catracters it returns a specilal code, had to test first 
                          
    print(q)
    if ord('0')==q:
        break

cv2.destroyAllWindows ( )

