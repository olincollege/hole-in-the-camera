# cv.rectangle(frame,(400,200),(800,600),(0,255,0),thickness=2)
#cv.putText(frame, "123", (540,190), cv.FONT_HERSHEY_TRIPLEX, 1.0, (0,255,0), thickness=2)
# frame[100:200,500:600,:] = 0,255,0     ---> changing array of image pixels
#frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
# frame = cv.GaussianBlur(frame,(1,1),cv.BORDER_DEFAULT)     ---> blur
#ret, frame = cv.threshold(frame,100,155, cv.THRESH_BINARY)
# frame = cv.Canny(frame,100,150)    #---> edge detection
import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
while True:
    isTrue, frame = cap.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # frame = cv.GaussianBlur(frame, (5, 5), cv.BORDER_DEFAULT)
    ret, thresh = cv.threshold(frame, 50, 100, cv.THRESH_BINARY)
    blank = np.zeros(frame.shape[:2], dtype="uint8")
    countours, hierarchies = cv.findContours(
        thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(blank, countours, -1, (0, 255, 0), 1)
    frame = cv.Canny(frame, 200, 250)
    cv.imshow("video", frame)
    if cv.waitKey(20) & 0xFF == ord('d'):
        break

cap.release()
cv.destroyAllWindows()
