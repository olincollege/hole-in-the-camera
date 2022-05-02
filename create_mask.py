import cv2 as cv

# Open a camera for video capturing.
cap = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    isTrue, frame = cap.read()
    # convert to HSV colorspace and apply threshold
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame, (0, 35, 0), (210, 255, 255))
    # apply image erosion and dilation to sharpen edges
    mask = cv.erode(mask, None, iterations=10)
    mask = cv.dilate(mask, None, iterations=10)
    cv.imshow("video", mask)
    if cv.waitKey(1) & 0xFF == ord('d'):
        cv.imwrite("body_pose.png", frame)
        cv.imwrite("new_mask.png", mask)
        break

# close video and destroy all windows
cap.release()
cv.destroyAllWindows()
