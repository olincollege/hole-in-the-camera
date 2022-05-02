import cv2 as cv

cap = cv.VideoCapture(0)
compare_mask = cv.imread("mask.png")
isTrue, frame = cap.read()
compare_mask = cv.resize(compare_mask, (frame.shape[1], frame.shape[0]))
while True:
    isTrue, frame = cap.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame, (0, 35, 0), (210, 255, 255))
    mask = cv.erode(mask, None, iterations=10)
    mask = cv.dilate(mask, None, iterations=10)
    cnts, hier = cv.findContours(mask.copy(), cv.RETR_EXTERNAL,
                                 cv.CHAIN_APPROX_SIMPLE)
    # frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
    cv.drawContours(mask, cnts, -1, (0, 255, 0), 3)
    dst = cv.bitwise_and(frame, mask)
    cv.imshow("video", dst)
    if cv.waitKey(1) & 0xFF == ord('d'):
        cv.imwrite("body_pose.png", frame)
        cv.imwrite("new_mask.png", mask)
        break

cap.release()
cv.destroyAllWindows()
