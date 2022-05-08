"""
Tests for the PygameViewer class that is used to visualize the hole in the
camera game.
"""

import pygame
import numpy as np
from cv2 import cv2
from hole_in_the_camera_view import PygameViewer


def test_pygame_display_size_default():
    """
    Test that the default display size of the pygame window is 640x480.
    """
    display_size = (640, 480)
    _ = PygameViewer(display_size)
    test_size = pygame.display.get_window_size()
    pygame.quit()
    assert display_size == test_size


def test_pygame_display_size_negative():
    """
    Test that the pygame window size cannot be negative.
    """
    display_size = (-1, -1)
    try:
        _ = PygameViewer(display_size)
        _ = pygame.display.get_window_size()
        pygame.quit()
        assert False
    except pygame.error:
        assert True


def test_pygame_display_size_square():
    """
    Test that the pygame window size can be square.
    """
    display_size = (640, 640)
    _ = PygameViewer(display_size)
    test_size = pygame.display.get_window_size()
    pygame.quit()
    assert display_size == test_size


def test_initialize_view_pygame_before_initialization():
    """
    Test that pygame in not currently initialized before the pygame
    module is initialized.
    """
    _ = PygameViewer((640, 480))
    display_state = pygame.get_init()
    pygame.quit()
    assert not display_state


def test_initialize_view_pygame_after_initialization():
    """
    Test that pygame is currently initialized after the pygame module
    is initialized.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    display_state = pygame.get_init()
    pygame.quit()
    assert display_state

def test_initialize_view_music_before_initialization():
    _ = PygameViewer((640, 480))
    music_state = pygame.mixer.music.get_busy()
    pygame.quit()
    assert not music_state

def test_initialize_view_music_after_initialization():
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    music_state = pygame.mixer.music.get_busy()
    pygame.quit()
    assert music_state

def test_initialize_view_correct_caption():
    """
    Test that the pygame window caption is correct.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_caption = pygame.display.get_caption()[0]
    expected_caption = "Hole in the Camera"
    pygame.quit()
    assert test_caption == expected_caption


def test_initialize_view_caption_before_initialization():
    """
    Test that the pygame window has default caption before
    the initialize_view method is called.
    """
    _ = PygameViewer((640, 480))
    test_caption = pygame.display.get_caption()[0]
    expected_caption = "pygame window"
    pygame.quit()
    assert test_caption == expected_caption


def test_initialize_view_correct_icon_title():
    """
    Test that the pygame window icon title is correct.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_icon_title = pygame.display.get_caption()[1]
    expected_caption = "Hole in the Camera"
    pygame.quit()
    assert test_icon_title == expected_caption


def test_initialize_view_icon_before_initialization():
    """
    Test that the pygame window has the default icon title before
    the initialize_view method is called.
    """
    _ = PygameViewer((640, 480))
    test_icon_title = pygame.display.get_caption()[1]
    expected_caption = "pygame window"
    pygame.quit()
    assert test_icon_title == expected_caption


def test_display_introduction_screen_type():
    """
    Test that the pygame window is of the correct type.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    test_screen_type = type(test_view.screen)
    pygame.quit()
    assert test_screen_type == pygame.Surface


def test_display_introduction_screen_width():
    """
    Test that the "display introduction" screen has the correct width.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    test_screen_width = test_view.screen.get_width()
    pygame.quit()
    assert test_screen_width == 640


def test_display_introduction_screen_height():
    """
    Test that the "display introduction" screen has the correct height.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    test_screen_height = test_view.screen.get_height()
    pygame.quit()
    assert test_screen_height == 480


def test_display_introduction_screen_pixel_shape():
    """
    Test that the "display introduction" screen's pixel values
    have correct dimensions.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.shape(pixel_values) == (640, 480, 3)


def test_display_introduction_screen_pixel_values():
    """
    Test that the "display introduction" screen's pixels
    have correct RGB values.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_introduction()
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_instructions_screen_type():
    """
    Test that the "display instructions" window is of the correct type.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    test_screen_type = type(test_view.screen)
    pygame.quit()
    assert test_screen_type == pygame.Surface


def test_display_instructions_screen_width():
    """
    Test that the "display instructions" screen has the correct width.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    test_screen_width = test_view.screen.get_width()
    pygame.quit()
    assert test_screen_width == 640


def test_display_instructions_screen_height():
    """
    Test that the "display instructions" screen has the correct height.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    test_screen_height = test_view.screen.get_height()
    pygame.quit()
    assert test_screen_height == 480


def test_display_instructions_screen_pixel_shape():
    """
    Test that the "display instructions" screen's has correct
    pixel dimensions.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.shape(pixel_values) == (640, 480, 3)


def test_display_instructions_screen_pixel_values():
    """
    Test that the "display instructions" screen's pixels
    have correct RGB values.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_view.display_instructions()
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_disp_screen_width():
    """
    Test that the game screen with mask overlaid has the correct width.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_frame = cv2.imread("images/poses/first_mask.png")
    test_timer = "10"
    test_mask = cv2.imread("images/masks/first_mask.png")
    test_view.display_frame(test_frame, test_timer, test_mask)
    test_width = test_view.screen.get_width()
    pygame.quit()
    assert test_width == 640


def test_display_frame_screen_height():
    """
    Test that the game screen with mask overlaid has the correct width.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_frame = cv2.imread("images/poses/first_mask.png")
    test_timer = "10"
    test_mask = cv2.imread("images/masks/first_mask.png")
    test_view.display_frame(test_frame, test_timer, test_mask)
    test_width = test_view.screen.get_height()
    pygame.quit()
    assert test_width == 480


def test_display_frame_screen_pixel_shape():
    """
    Test that the game screen with mask overlaid has correct
    pixel dimensions.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_frame = cv2.imread("images/poses/first_mask.png")
    test_timer = "10"
    test_mask = cv2.imread("images/masks/first_mask.png")
    test_view.display_frame(test_frame, test_timer, test_mask)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.shape(pixel_values) == (640, 480, 3)


def test_display_frame_screen_pixel_values():
    """
    Test that the game screen with mask overlaid has correct
    pixel values.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_frame = cv2.imread("images/poses/first_mask.png")
    test_timer = "10"
    test_mask = cv2.imread("images/masks/first_mask.png")
    test_view.display_frame(test_frame, test_timer, test_mask)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_win_screen_width():
    """
    Test that the win game screen has correct width.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_win_state = True
    test_score = 100
    test_view.display_win(test_win_state, test_score)
    test_width = test_view.screen.get_width()
    pygame.quit()
    assert test_width == 640


def test_display_win_screen_height():
    """
    Test that the win game screen has correct height.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_win_state = True
    test_score = 100
    test_view.display_win(test_win_state, test_score)
    test_width = test_view.screen.get_height()
    pygame.quit()
    assert test_width == 480


def test_display_win_screen_pixel_shape():
    """
    Test that the win game screen has correct pixel dimensions.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_win_state = True
    test_score = 100
    test_view.display_win(test_win_state, test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.shape(pixel_values) == (640, 480, 3)


def test_display_win_screen_pixel_values_win():
    """
    Test that the win game screen has correct pixel values.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_win_state = True
    test_score = 100
    test_view.display_win(test_win_state, test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_win_screen_pixel_values_loss():
    """
    Test that the losing game screen has correct pixel values.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_win_state = False
    test_score = 100
    test_view.display_win(test_win_state, test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_win_screen_pixel_values_zero_score():
    """
    Test that the win game screen has correct pixel values.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_win_state = True
    test_score = 0
    test_view.display_win(test_win_state, test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_win_screen_pixel_values_negative_score():
    """
    Test that the win game screen has correct pixel values
    when the score is negative.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_win_state = True
    test_score = -100
    test_view.display_win(test_win_state, test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_end_game_screen_width():
    """
    Test that the end game screen has correct width.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_score = 100
    test_view.display_end_game(test_score)
    test_width = test_view.screen.get_width()
    pygame.quit()
    assert test_width == 640


def test_display_end_game_screen_height():
    """
    Test that the end game screen has correct height.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_score = 100
    test_view.display_end_game(test_score)
    test_width = test_view.screen.get_height()
    pygame.quit()
    assert test_width == 480


def test_display_end_game_screen_pixel_shape():
    """
    Test that the end game screen has correct pixel dimensions.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_score = 100
    test_view.display_end_game(test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.shape(pixel_values) == (640, 480, 3)


def test_display_end_game_screen_pixel_values_positive_score():
    """
    Test that the end game screen has correct pixel values.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_score = 100
    test_view.display_end_game(test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_end_game_screen_pixel_values_negative_score():
    """
    Test that the end game screen has correct pixel values
    when the score is negative.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_score = -100
    test_view.display_end_game(test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255


def test_display_end_game_screen_pixel_values_zero_score():
    """
    Test that the end game screen has correct pixel values
    when the score is zero.
    """
    test_view = PygameViewer((640, 480))
    test_view.initialize_view()
    test_score = 0
    test_view.display_end_game(test_score)
    pixel_values = pygame.surfarray.array3d(test_view.screen)
    pygame.quit()
    assert np.mean(pixel_values) > 0 and np.mean(pixel_values) < 255
