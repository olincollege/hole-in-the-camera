# cv.rectangle(frame,(400,200),(800,600),(0,255,0),thickness=2)
#cv.putText(frame, "123", (540,190), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,255,0), thickness=2)
# frame[100:200,500:600,:] = 0,255,0     ---> changing array of image pixels
#frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
# frame = cv.GaussianBlur(frame,(1,1),cv.BORDER_DEFAULT)     ---> blur
#ret, frame = cv.threshold(frame,100,155, cv.THRESH_BINARY)
# frame = cv.Canny(frame,100,150)    #---> edge detection
# (0, 0, 200), (145, 60, 255)
from itertools import count
import cv2 as cv
from cv2 import compare
import numpy as np
import pygame

cap = cv.VideoCapture(0)
# pygame.init()
compare_mask = cv.imread("mask.png")
while True:
    isTrue, frame = cap.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame, (0, 35, 0), (210, 255, 255))
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=2)
    # cnts, hier = cv.findContours(mask.copy(), cv.RETR_EXTERNAL,
    #                              cv.CHAIN_APPROX_SIMPLE)
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # cv.drawContours(frame, cnts, -1, (0, 255, 0), 3)
    frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)
    dst = cv.bitwise_and(frame, compare_mask)
    cv.imshow("video", dst)
    # screen = pygame.display.set_mode((mask.shape[1], mask.shape[0]))
    # new_surf = pygame.transform.rotate(
    #     pygame.surfarray.make_surface(mask), -90)
    # screen.blit(new_surf, (0, 0))
    # pygame.display.update()
    if cv.waitKey(20) & 0xFF == ord('d'):
        compare_mask = cv.cvtColor(compare_mask, cv.COLOR_BGR2GRAY)
        count = 0
        for i in range(0, mask.shape[0]):
            for j in range(0, mask.shape[1]):
                if mask[i][j] == compare_mask[i][j]:
                    count += 1
        print((count/(mask.shape[0]*mask.shape[1]))*100)
        break

cap.release()
cv.destroyAllWindows()
