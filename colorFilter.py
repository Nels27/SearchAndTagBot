import numpy as np
import cv2
import cv_bridge

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Conversting BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    #Denoting upper and lower Blue
    lower_blue = np.array([100,55,80])
    upper_blue = np.array([130,255,255])

    #Denoting upper and lower Red
    #lower_red = np.array([255,0,0])
    #upper_red = np.array([255,0,64])

    #Denoting upper and lower Green
    #lower_green = np.array([0,77,37])
    #upper_green = np.array([51,255,150])

    #Creating the mask img of the filtered out the color
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    #Creating the bitwise-and mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Display the resulting frames
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
