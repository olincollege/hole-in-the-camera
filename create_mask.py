"""
"""
import cv2 as cv

# Open a camera for video capturing.
CAMERA = cv.VideoCapture(0)

while True:
    # Capture frame-by-frame
    isTrue, frame = CAMERA.read()
    # convert to HSV colorspace and apply threshold
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame, (0, 35, 0), (210, 255, 255))
    # apply image erosion and dilation to sharpen edges
    mask = cv.erode(mask, None, iterations=10)
    mask = cv.dilate(mask, None, iterations=10)
    cv.imshow("video", mask)
    # break if user presses 'd'
    if cv.waitKey(1) & 0xFF == ord('d'):
        # save the current frame and the mask applied on it
        cv.imwrite("images/poses/body_pose.png", frame)
        cv.imwrite("images/masks/new_mask.png", mask)
        break

# close video and destroy all windows
cap.release()
cv.destroyAllWindows()
