import cv2
import numpy as np

voisinage = 3  #dimension masque ?
def filtreMoyenNVG(img):
    h, w = img.shape
    imgMoy = np.zeros(img.shape, np.uint8)  #nouvelle image

    for y in range(h):
        for x in range(w):

            # tjr diviser par 2 car our pixel is in the middle so we move by middle
            # print(voisinage/2)
            if x < voisinage/2 or x > w - voisinage/2 or y < voisinage/2 \
               or y > h - voisinage/2:
                imgMoy[y, x] = img[y, x] #keep borders
            else:
                imgV = img[int(y - voisinage/2):int(y + voisinage/2) ,
                           int(x - voisinage/2):int(x + voisinage/2) ]
               
                #manuellemnt
                #moy = 0
                #for yv in range(voisinage):
                #    for xv in range(voisinage):
                #        moy += imgV[yv, xv]
                #moy /= voisinage * voisinage
                imgMoy[y, x] = np.mean(imgV)   # AUTOMATIC CONVERSIONNNNNN
    return imgMoy
def filtreMedianNVG(img):
    h, w = img.shape
    imgMed = np.zeros(img.shape, np.uint8)
    for y in range(h):
        for x in range(w):
            if x < voisinage/2 or x > w - voisinage/2 or y < voisinage/2 \
               or y > h - voisinage/2:
                imgMed[y, x] = img[y, x]
            else:
                imgV = img[int(y - voisinage/2):int(y + voisinage/2) + 1,
                           int(x - voisinage/2):int(x + voisinage/2) + 1]
                #t = np.zeros((voisinage * voisinage), np.uint8)
                #for yv in range(voisinage):
                #    for xv in range(voisinage):
                #        t[yv * voisinage + xv] = imgV[yv, xv]
                #t.sort()
                #imgMed[y, x] = t[(voisinage * voisinage - 1) / 2]
                imgMed[y, x] = np.median(imgV)
    return imgMed


img = cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/TP3/image2.png', cv2.IMREAD_GRAYSCALE)
cv2.imshow('image source', img)
imgMoy = filtreMoyenNVG(img)
imgMed = filtreMedianNVG(img)
cv2.imshow('image source', img)
cv2.imshow('image moy', imgMoy)
cv2.imshow('image med', imgMed)
cv2.waitKey(0)
cv2.destroyAllWindows()
