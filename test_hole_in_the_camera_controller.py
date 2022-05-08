"""
Tests for the OpenCVController class.
"""
import time
import pygame
import cv2
import numpy as np
from hole_in_the_camera_view import PygameViewer
from hole_in_the_camera_controller import OpenCVController


def test_camera_index_initialization_zero():
    """
    Test to ensure that the camera index is correctly intialized to zero.
    """
    camera_index = 0
    test_controller = OpenCVController(camera_index)

    assert test_controller.camera_index == camera_index


def test_camera_index_initialization_positive():
    """
    Test to ensure that the camera index is correctly intialized to one.
    """
    camera_index = 1
    test_controller = OpenCVController(camera_index)

    assert test_controller.camera_index == camera_index


def test_camera_index_initialization_negative():
    """
    Test to ensure that the camera index is correctly
    intialized to negative one.
    """
    camera_index = -1
    test_controller = OpenCVController(camera_index)

    assert test_controller.camera_index == camera_index


def test_camera_capture_initialization():
    """
    Test to ensure that the camera capture is correctly initialized.
    """
    camera_index = 0
    test_controller = OpenCVController(camera_index)

    assert isinstance(test_controller.camera_capture, cv2.VideoCapture)


def test_next_screen_space_press():
    """
    Test to ensure that the next screen function returns the "continue"
    state when the space bar is pressed.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    state = test_controller.next_screen()
    pygame.quit()
    assert state == "continue"


def test_next_screen_letter_press():
    """
    Test to ensure that the next screen function returns the "continue"
    state when a letter key is pressed.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
    state = test_controller.next_screen()
    pygame.quit()
    assert state == "continue"


def test_next_screen_no_press():
    """
    Test to ensure that the next screen function returns the "stay"
    state when no key is pressed.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    state = test_controller.next_screen()
    pygame.quit()
    assert state == "stay"


def test_next_screen_escape_press():
    """
    Test to ensure that the next screen function returns the "quit"
    state when the escape key is pressed.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    state = test_controller.next_screen()
    pygame.quit()
    assert state == "quit"


def test_next_screen_escape_and_letter_press():
    """
    Test to ensure that the next screen function still returns the "quit"
    state when a letter key is pressed after the escape key.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    time.sleep(0.2)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
    state = test_controller.next_screen()
    pygame.quit()
    assert state == "quit"


def test_next_screen_escape_and_space_press():
    """
    Test to ensure that the next screen function still returns the "quit"
    state when the space bar is pressed after the escape key.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    time.sleep(0.2)
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    state = test_controller.next_screen()
    pygame.quit()
    assert state == "quit"


def test_release_camera():
    """
    Test to ensure that the camera stops capturing frames when the
    release_camera function is called.
    """
    test_controller = OpenCVController(0)
    test_controller.release_camera()

    try:
        test_controller.get_display_frame()
        assert False
    except cv2.error:
        assert True


def test_non_started_timer():
    """
    Test to ensure that the start time remains zero before the start_timer
    function is called.
    """
    test_controller = OpenCVController(0)

    assert test_controller.start_time == 0


def test_started_timer():
    """
    Test to ensure that the start time is non-zero after the start_timer
    function is called.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_controller.start_timer()
    pygame.quit()
    assert test_controller.start_time != 0


def test_get_display_frame_shape():
    """
    Test to ensure that the get_display_frame function returns a frame
    with the correct shape.
    """
    test_controller = OpenCVController(0)
    test_frame = test_controller.get_display_frame()
    assert np.shape(test_frame) == (480, 640, 3)


def test_get_display_frame_values():
    """
    Test to ensure that the get_display_frame function returns a frame
    with the correct RGB values.
    """
    test_controller = OpenCVController(0)
    test_frame = test_controller.get_display_frame()
    if np.min(test_frame) < 0 or np.max(test_frame) > 255:
        assert False
    assert True


def test_get_timer_string_type():
    """
    Test to ensure that the get_timer_string function
    returns the timer as a string.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()
    assert isinstance(test_timer_string, str)


def test_get_timer_string_no_wait():
    """
    Test to ensure that the get_timer_string function
    returns the correct countdown string when no wait is required.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()

    assert test_timer_string == "10"


def test_get_timer_string_two_second_wait():
    """
    Test to ensure that the get_timer_string function
    decrements the half-second timer by 4 when the wait is 2 seconds.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(2)
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()

    assert test_timer_string == "6"


def test_get_timer_string_end_timer():
    """
    Test to ensure that the get_timer_string function
    decrements the half-second timer by 10 when the wait is 5 seconds.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(5)
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()

    assert test_timer_string == "0"


def test_get_timer_string_negative():
    """
    Test to ensure that the get_timer_string function
    returns negative values when the wait is more than the
    countdown.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(7)
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()

    assert test_timer_string == "-4"


def test_determine_end_timer_not_end():
    """
    Test to ensure that the determine_end_timer function
    returns False when the timer is not at 0.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(2)
    test_controller.get_timer_string()
    test_end_state = test_controller.determine_end_timer()
    pygame.quit()
    assert not test_end_state


def test_determine_end_timer_end():
    """
    Test to ensure that the determine_end_timer function
    returns True when the timer is at 0.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(5)
    test_controller.get_timer_string()
    test_end_state = test_controller.determine_end_timer()
    pygame.quit()
    assert test_end_state


def test_determine_end_timer_beyond_end():
    """
    Test to ensure that the determine_end_timer function
    returns True when the timer is complete.
    """
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(7)
    test_controller.get_timer_string()
    test_end_state = test_controller.determine_end_timer()
    pygame.quit()
    assert test_end_state
