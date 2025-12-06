import cv2
import numpy as np
import time

cap=cv2.VideoCapture(0)

frame_width=int(cap.get(3))
frame_height=int(cap.get(4))

fourcc=cv2.VideoWriter_fourcc('X','V','I','D')
out=cv2.VideoWriter('output_out.avi',fourcc,25,(frame_width,frame_height))
if not cap.isOpened():
    print("error capture")
    exit(0)


while(cap.isOpened()):
    debut=time.time()
    ret,frame=cap.read()
   
    if not ret:
        print("error reading frame")
        break
    frame=cv2.flip(frame,1)
    # 1--> pa rapport a y  
    out.write(frame)
    cv2.imshow('image',frame)
    
    
    
    while(1/(time.time()-debut)>25):
        ...
    if cv2.waitKey(1) & 0xFF==ord('q'): #1 ou plus n est pas bloquant 
        break  
    # gives real fps 
    print(1/(time.time()-debut))

    
out.release()
out.release()
cv2.destroyAllWindows()