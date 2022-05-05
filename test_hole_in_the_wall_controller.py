"""
untested functions:
release_camera
next_screen
quit_game
"""
from hole_in_the_wall_controller import OpenCVController
import cv2
import numpy as np
from hole_in_the_wall_view import PygameViewer
import time
import pygame
import pdb


def test_camera_index_initialization_zero():
    camera_index = 0
    test_controller = OpenCVController(camera_index)

    assert test_controller._camera_index == camera_index

def test_camera_index_initialization_positive():
    camera_index = 1
    test_controller = OpenCVController(camera_index)

    assert test_controller._camera_index == camera_index

def test_camera_index_initialization_negative():
    camera_index = -1
    test_controller = OpenCVController(camera_index)

    assert test_controller._camera_index == camera_index

def test_camera_capture_initialization():
    camera_index = 0
    test_controller = OpenCVController(camera_index)

    assert type(test_controller._camera_capture) == cv2.VideoCapture

def test_next_screen_letter_press():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    posted = pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
    time.sleep(.5)
    state = test_controller.next_screen()
    pygame.quit()
    pdb.set_trace()
    assert state == True

def test_non_started_timer():
    test_controller = OpenCVController(0)

    assert test_controller._start_time == 0

def test_started_timer():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_controller.start_timer()
    pygame.quit()
    assert test_controller._start_time != 0

def test_get_camera_frame_shape():
    test_controller = OpenCVController(0)
    test_frame = test_controller.get_camera_frame()
    assert np.shape(test_frame) != (640, 480, 3)

def test_get_camera_frame_values():
    test_controller = OpenCVController(0)
    test_frame = test_controller.get_camera_frame()
    if np.min(test_frame) < 0 or np.max(test_frame) > 255:
        assert False
    assert True

def test_get_timer_string_type():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()
    assert type(test_timer_string) == str

def test_get_timer_string_no_wait():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()

    assert test_timer_string == "10"

def test_get_timer_string_two_second_wait():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(2)
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()

    assert test_timer_string == "6"

def test_get_timer_string_end_timer():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(5)
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()

    assert test_timer_string == "0"

def test_get_timer_string_negative():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(7)
    test_timer_string = test_controller.get_timer_string()
    pygame.quit()

    assert test_timer_string == "-4"

def test_determine_end_timer_not_end():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(2)
    test_controller.get_timer_string()
    test_end_state = test_controller.determine_end_timer()
    pygame.quit()
    assert test_end_state == False

def test_determine_end_timer_end():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(5)
    test_controller.get_timer_string()
    test_end_state = test_controller.determine_end_timer()
    pygame.quit()
    assert test_end_state == True

def test_determine_end_timer_beyond_end():
    test_controller = OpenCVController(0)
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    time.sleep(7)
    test_controller.get_timer_string()
    test_end_state = test_controller.determine_end_timer()
    pygame.quit()
    assert test_end_state == True