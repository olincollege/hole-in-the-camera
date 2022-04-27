import cv2 as cv
from cv2 import compare
import numpy
import pygame
from itertools import count

# Open a camera for video capturing. 
cap = cv.VideoCapture(0)
# import hole in the wall image
compare_mask = cv.imread("mask.png")

while True:
    isTrue, frame = cap.read()
    # apply HSV color space
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # 
    mask = cv.inRange(frame, (0,35,0), (210, 255, 255))
    # apply image erosion and dilation (why!)
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)
    # return to BGR color
    frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)
    # stack up current frame and hole in the wall image
    dst = cv.bitwise_and(frame, compare_mask)
    # show BGR color frame of user with "hole" on top
    cv.imshow("video", dst)

    if cv.waitKey(20) & 0xFF == ord('d'):
        # gray scale of hole in the wall
        compare_mask = cv.cvtColor(compare_mask, cv.COLOR_BGR2GRAY)
        # count pixel by pixel for similarity between frame and hole
        count = 0
        for i in range(0,mask.shape[0]):
            for j in range(0,mask.shape[1]):
                if mask[i][j] == compare_mask[i][j]:
                    count += 1
        # print out the score of how well fit through hole
        print((count/(mask.shape[0]*mask.shape[1]))*100)
        break
    # close video and destroy all windows
    cap.release()
    cv.destroyAllWindows()