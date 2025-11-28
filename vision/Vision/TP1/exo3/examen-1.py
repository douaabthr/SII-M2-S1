import cv2
import numpy as np
from random import randrange


# 1-creating image with a random black point
def createImgWithPointRand(h,w) :
    img= np.ones ( (heigthImg , widthImg) ,np.float32)


    #randrange (x) return une valeur aléatoire entre 0 et x
    randPointY,RandPointX = randrange (heigthImg) , randrange (widthImg)
    img [randPointY,RandPointX] =0
    return img


heigthImg=200
widthImg =400

img = createImgWithPointRand (heigthImg , widthImg)

cv2.imshow( 'random point',img)

'''la fonction waitKey return le code ASCII d un caractere dans
la variable q. Le code ASCII de '0'=48, '1'=49, ....etc '''
q= cv2.waitKey(0) & 0xFF
print(q)
cv2.destroyAllWindows ( )


# 2-deplacement du pixel
