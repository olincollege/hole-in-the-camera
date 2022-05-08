"""
This script is used to make holes for users to fit into and saves the original
frame and the hole to images/poses and images/masks respectively.
"""
import cv2 as cv

# Open a camera for video capturing.
CAMERA = cv.VideoCapture(0)
# Image name to be analyzed.
MASK_NAME = "eighth_mask"

def get_camera_frame():
    """
    This function returns the user's camera frame.

    Returns:
        frame (numpy.ndarray): A 3-D numpy array of RGB values representing
            the user's camera output.
    """
    # Capture frame-by-frame
    _, frame = CAMERA.read()
    return frame

def analyze_camera_frame(frame):
    """
    This function analyzes a given camera frame to make a mask to be displayed
    during the actual game.

    Args:
        frame (numpy.ndarray): A 3-D numpy array of RGB values representing
            the user's camera output.
    Returns:
        frame (numpy.ndarray): A 3-D numpy array of HSV values representing
            the user's camera output.
        mask (numpy.ndarray): A 2-D numpy array representing black and white
            pixel values (gray scaled) that should either be 0 or 255 and is
            the mask to be overlaid over the user's screen.
    """
    # convert to HSV colorspace and apply threshold
    frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(frame, (0, 14, 0), (180, 255, 255))
    # apply image erosion and dilation to sharpen edges
    mask = cv.erode(mask, None, iterations=5)
    mask = cv.dilate(mask, None, iterations=5)
    cv.imshow("video", mask)
    return frame, mask

def release_camera():
    """
    Release the camera at the end of the script to ensure that the camera is
    no longer being called.
    """
    CAMERA.release()
    cv.destroyAllWindows()

def main():
    """
    This is the runner function to create and save masks.
    """

    while True:
        frame = get_camera_frame()
        frame, mask = analyze_camera_frame(frame)
        # break if user presses 'd'
        if cv.waitKey(1) & 0xFF == ord("d"):
            # save the current frame and the mask applied on it
            frame = cv.cvtColor(frame, cv.COLOR_HSV2BGR)
            cv.imwrite(f"images/poses/{MASK_NAME}.png", frame)
            cv.imwrite(f"images/masks/{MASK_NAME}.png", mask)
            break

    release_camera()

if __name__ == "__main__":
    main()
