"""
Create masks to use in the game.
"""
from cv2 import cv2 as cv

# Open a camera for video capturing.
CAMERA = cv.VideoCapture(0)
MASK_NAME = "sixth_mask"

while True:
    # Capture frame-by-frame
    isTrue, frame = CAMERA.read()
    # convert to HSV colorspace and apply threshold
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame, (0, 14, 0), (180, 255, 255))
    # apply image erosion and dilation to sharpen edges
    mask = cv.erode(mask, None, iterations=5)
    mask = cv.dilate(mask, None, iterations=5)
    cv.imshow("video", mask)
    # break if user presses 'd'
    if cv.waitKey(1) & 0xFF == ord('d'):
        # save the current frame and the mask applied on it
        frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)
        cv.imwrite(f"images/poses/{MASK_NAME}.png", frame)
        cv.imwrite(f"images/masks/{MASK_NAME}.png", mask)
        break

# close video and destroy all windows
CAMERA.release()
cv.destroyAllWindows()
