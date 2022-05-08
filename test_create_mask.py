"""
Test functions for the create_mask script.
"""

import cv2
import numpy as np
from create_mask import get_camera_frame, analyze_camera_frame

def test_get_camera_frame_shape():
    """
    Tests to make sure that the shape of the camera output is a 3-D array.
    """
    test_frame = get_camera_frame()
    test_shape = np.shape(test_frame)
    assert test_shape[0] != 0 and test_shape[1] != 0 and test_shape[2] == 3

def test_get_camera_frame_values():
    """
    Tests to make sure that the camera output isn't all 0s (black image) or all
    255s (white iamge)
    """
    test_frame = get_camera_frame()
    assert np.mean(test_frame) > 0 and np.mean(test_frame) < 255

def test_analyze_camera_frame_mask_shape():
    """
    Tests to make sure the base dimensions of the mask and frame are the same
    after the mask is created from a camera frame.
    """
    test_frame = get_camera_frame()
    _, test_mask = analyze_camera_frame(test_frame)
    assert (np.shape(test_mask)[0], np.shape(test_mask)[1], 3) ==\
        np.shape(test_frame)

def test_analyze_camera_frame_mask_values():
    """
    Tests to make sure that the values of the mask are all either 0 or 255 to
    make sure it is a binary mask.
    """
    test_frame = get_camera_frame()
    _, test_mask = analyze_camera_frame(test_frame)
    for row in test_mask:
        for value in row:
            # all values should be 0 or 255 as the mask is a black and white
            # grayscaled image
            if value not in (0, 255):
                assert False
    assert True

def test_analyze_camera_frame_mask_shape_saved_image():
    """
    Tests to make sure that the mask size is properly generated from a saved
    image.
    """
    test_frame = cv2.imread('images/poses/first_mask.png')
    _, test_mask = analyze_camera_frame(test_frame)
    assert (np.shape(test_mask)[0], np.shape(test_mask)[1], 3) ==\
        np.shape(test_frame)

def test_analyze_camera_frame_mask_values_saved_image():
    """
    Tests to make sure that the mask values are all 0 or 255 when generated from
    a saved image.
    """
    test_frame = cv2.imread('images/poses/first_mask.png')
    _, test_mask = analyze_camera_frame(test_frame)
    for row in test_mask:
        for value in row:
            # all values should be 0 or 255 as the mask is a black and white
            # grayscaled image
            if value not in (0, 255):
                assert False
    assert True
