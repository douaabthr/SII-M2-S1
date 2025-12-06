import cv2
import numpy as np 


img=cv2.imread('C:/Users/Imane/OneDrive/Bureau/vision/TP/TP6/image.png',cv2.IMREAD_GRAYSCALE)
cv2.threshold(img,128,255,0,img)

erodeSize=1
def erode_func():
    size=erodeSize*2+1
    kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(size,size))
    img_erode=cv2.erode(img,kernel,iterations=1)
    cv2.imshow("erode",img_erode)
def changeErodeSize(x):
    global erodeSize
    erodeSize=x
    erode_func()

#fenetre vide

cv2.namedWindow("erode")
erode_func()




dilateSize=1
def dilate_func():
    size=dilateSize*2+1
    kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(size,size))
    img_dilate=cv2.dilate(img,kernel,iterations=1)
    cv2.imshow("dilate",img_dilate)
def changeDilateSize(x):
    global dilateSize
    dilateSize=x
    dilate_func()

#fenetre vide

cv2.namedWindow("dilate")
dilate_func()


#any morph kernel


morphSize=1
morphFunction=2
def morph_func():
    size=morphSize*2+1
    kernel=cv2.getStructuringElement(cv2.MORPH_CROSS,(size,size))
    img_morph=cv2.morphologyEx(img,morphFunction,kernel,iterations=1)
    cv2.imshow("morph",img_morph)
def changeMorphSize(x):
    global morphSize
    morphSize=x
    morph_func()

def changeMorphFunction(x):
    global morphFunction
    morphFunction=x
    morph_func()

#fenetre vide

cv2.namedWindow("morph")
morph_func()



cv2.createTrackbar("Size Erode","erode",0,30,changeErodeSize)
cv2.createTrackbar("Size Dilate","dilate",0,30,changeDilateSize)

cv2.createTrackbar("Fonction Morph","morph",2,6,changeMorphFunction)
cv2.createTrackbar("Size Morph","morph",0,30,changeMorphSize)

cv2.imshow("image source",img)
cv2.waitKey(0)
cv2.destroyAllWindows()

