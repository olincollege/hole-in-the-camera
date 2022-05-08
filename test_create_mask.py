"""
Test functions for the create_mask script.
"""

from create_mask import get_camera_frame, analyze_camera_frame
import numpy as np
import cv2

def test_get_camera_frame_shape():
    test_frame = get_camera_frame()
    test_shape = np.shape(test_frame)
    assert test_shape[0] != 0 and test_shape[1] != 0 and test_shape[2] == 3

def test_get_camera_frame_values():
    test_frame = get_camera_frame()
    assert np.mean(test_frame) > 0 and np.mean(test_frame) < 255

def test_analyze_camera_frame_mask_shape():
    test_frame = get_camera_frame()
    _, test_mask = analyze_camera_frame(test_frame)
    assert (np.shape(test_mask)[0], np.shape(test_mask)[1], 3) ==\
        np.shape(test_frame)

def test_analyze_camera_frame_mask_values():
    test_frame = get_camera_frame()
    _, test_mask = analyze_camera_frame(test_frame)
    for row in test_mask:
        for value in row:
            if value != 0 and value != 255:
                assert False
    assert True

def test_analyze_camera_frame_mask_shape_saved_image():
    test_frame = cv2.imread('images/poses/first_mask.png')
    _, test_mask = analyze_camera_frame(test_frame)
    assert (np.shape(test_mask)[0], np.shape(test_mask)[1], 3) ==\
        np.shape(test_frame)

def test_analyze_camera_frame_mask_values_saved_image():
    test_frame = cv2.imread('images/poses/first_mask.png')
    _, test_mask = analyze_camera_frame(test_frame)
    for row in test_mask:
        for value in row:
            if value != 0 and value != 255:
                assert False
    assert True