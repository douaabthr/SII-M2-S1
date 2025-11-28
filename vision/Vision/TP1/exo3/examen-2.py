import cv2
import numpy as np
from random import randrange


# 1-creating image with a random black point
def createImgWithPointRand(h,w) :
    # only 2 dimensions --> grayscale 
    # else if channel 1 (bgr) is 1 others 0 it means pure blue
    img= np.ones ( (heigthImg , widthImg) ,np.float32) # entre 0 et 1 1 white
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
    if 50==q and py+pas<heigthImg:  #2--> bas
        img[py,px]=1
        img[py+pas,px]=0
        py=py+pas
    if 56==q and py-pas >=0:     #8-->haut
        img[py,px]=1
        img[py-pas,px]=0
        py=py-pas
    if 52==q and px-pas >=0:      #4-->guche
        img[py,px]=1
        img[py,px-pas]=0
        px=px-pas
    if 54==q and px+pas < widthImg:   #6-->droite
        img[py,px]=1
        img[py,px+pas]=0
        px=px+pas


    imgRes=img.copy()    # to make a 3x3 point, thats why le pas is 3
    imgRes[py-2:py+2,px-2:px+2]=0
    cv2.imshow( 'image vide',imgRes)

    # you have to use this as it works in the window
    q= cv2.waitKey(0) & 0xFF    # 0--> wait indefinetly until a key is pressed (while an image is open !!!!), retoune un entier --> ascii/unicode
                                # 0XFF = 00.. 11111111 so it forces it to be 8 bits --> we only get ascii code cuz sometimes can be big depending on the OS
    # its an opencv function waits for a precised amounfo milliseconds 0 means indefinitely
    if ord('0')==q: #unicode (or ascii if classical caracter)
        break

cv2.destroyAllWindows ( )

# unicodeis modern and vast almost all languages emojis..
# ascii older 128 alphabets (7bits) (letter,numbers,punct)