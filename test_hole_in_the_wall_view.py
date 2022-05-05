"""

"""

from hole_in_the_wall_view import PygameViewer
import pygame
import pdb
import numpy as np


def test_pygame_display_size_default():
    display_size = (640, 480)
    _ = PygameViewer(display_size)
    test_size = pygame.display.get_window_size()
    pygame.quit()
    assert display_size == test_size

def test_pygame_display_size_negative():
    display_size = (-1, -1)
    try:
        _ = PygameViewer(display_size)
        test_size = pygame.display.get_window_size()
        pygame.quit()
        assert False
    except pygame.error:
        assert True

def test_pygame_display_size_square():
    display_size = (640, 640)
    _ = PygameViewer(display_size)
    test_size = pygame.display.get_window_size()
    pygame.quit()
    assert display_size == test_size

def test_initialize_view_pygame_before_initialization():
    _ = PygameViewer((640, 480))
    display_state = pygame.get_init()
    pygame.quit()
    assert display_state == False

def test_initialize_view_pygame_after_initialization():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    display_state = pygame.get_init()
    pygame.quit()
    assert display_state == True

def test_initialize_view_correct_caption():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_caption = pygame.display.get_caption()[0]
    expected_caption = "Hole in the Camera"
    pygame.quit()
    assert test_caption == expected_caption

def test_initialize_view_caption_before_initialization():
    _ = PygameViewer((640, 480))
    test_caption = pygame.display.get_caption()[0]
    expected_caption = "pygame window"
    pygame.quit()
    assert test_caption == expected_caption

def test_initialize_view_correct_icon_title():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_icon_title = pygame.display.get_caption()[1]
    expected_caption = "Hole in the Camera"
    pygame.quit()
    assert test_icon_title == expected_caption

def test_initialize_view_icon_before_initialization():
    _ = PygameViewer((640, 480))
    test_icon_title = pygame.display.get_caption()[1]
    expected_caption = "pygame window"
    pygame.quit()
    assert test_icon_title == expected_caption

def test_display_introduction_screen_type():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    test_screen_type = type(test_view._screen)
    pygame.quit()
    assert test_screen_type == pygame.Surface

def test_display_introduction_screen_width():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    test_screen_width = test_view._screen.get_width()
    pygame.quit()
    assert test_screen_width == 640

def test_display_introduction_screen_height():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    test_screen_height = test_view._screen.get_height()
    pygame.quit()
    assert test_screen_height == 480

def test_display_introduction_screen_pixel_shape():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pixel_values = pygame.surfarray.array3d(test_view._screen)
    pygame.quit()
    assert np.shape(pixel_values) == (640, 480, 3)

def test_display_introduction_screen_pixel_values():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pixel_values = pygame.surfarray.array3d(test_view._screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255

def test_display_instructions_screen_type():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    test_screen_type = type(test_view._screen)
    pygame.quit()
    assert test_screen_type == pygame.Surface

def test_display_instructions_screen_width():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    test_screen_width = test_view._screen.get_width()
    pygame.quit()
    assert test_screen_width == 640

def test_display_instructions_screen_height():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    test_screen_height = test_view._screen.get_height()
    pygame.quit()
    assert test_screen_height == 480

def test_display_instructions_screen_pixel_shape():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    pixel_values = pygame.surfarray.array3d(test_view._screen)
    pygame.quit()
    assert np.shape(pixel_values) == (640, 480, 3)

def test_display_instructions_screen_pixel_values():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    pixel_values = pygame.surfarray.array3d(test_view._screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255