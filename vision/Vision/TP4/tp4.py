import numpy as np
import cv2


#======GRADIENT=====

def filtregradient(img):
    h, w = img.shape
    gradX=gradY = np.zeros_like(img)
    gradX[:,1:] = img[:,1:]-img[:,:-1]
    gradY[1:,:] = img[1:,:]-img[:-1,:]
    # grad = np.zeros(img.shape, np.float32)

    # for y in range(h):
    #     for x in range(w):
    #         if y==0:
    #             gradY[y,x]=0
    #         else:
    #             # print(img[y,x]-img[y-1,x])

    #             gradY[y,x]=img[y,x]-img[y-1,x]
    #         if x==0:
    #             gradX[y,x]=0
    #         else:
    #             gradX[y,x]=img[y,x]-img[y,x-1]
  
    

    
    return np.uint8( np.sqrt(gradX**2+ gradY**2))

            

        
th=0
type_th=0

img=cv2.imread("TP4/img.png",cv2.IMREAD_GRAYSCALE)
grad=filtregradient(img)
cv2.imshow("img",grad)
def afficher():
    imgRes=np.zeros_like(grad)
    cv2.threshold(grad,th,255,type_th,imgRes)
    cv2.imshow("img",imgRes)


def change_th(x):
    global th
    th=x
    afficher()

def change_type(x):
    global type_th
    type_th=x
    afficher()


cv2.createTrackbar('th','img',0,255,change_th)
cv2.createTrackbar('type','img',0,4,change_type)
afficher()
cv2.waitKey(0)
cv2.destroyAllWindows()



# appliquer ce seuillage sur le gradient pour detecter les contours