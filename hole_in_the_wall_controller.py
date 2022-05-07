"""
Hole in the wall game controller.
"""
import pygame
from abc import ABC, abstractmethod
import cv2


class HoleInTheWallController(ABC):
    """
    Create abstract class for the game controller.

    Attributes:
        _camera_index (int): Index of the camera.
        _camera_capture (numpy.ndarray): Current caputured video frame.
        _start_time (float): Start time of the game.
        end_time (float): End time of the game.
    """

    def __init__(self):
        """
        """

    @abstractmethod
    def next_screen(self):
        """
        """

    @abstractmethod
    def start_timer(self):
        """
        """

    @abstractmethod
    def get_display_frame(self):
        """
        """

    @abstractmethod
    def get_timer_string(self):
        """
        """

    @abstractmethod
    def determine_end_timer(self):
        """
        """


class OpenCVController(HoleInTheWallController):
    def __init__(self, camera_index):
        """
        Initialize the OpenCV controller.

        Args:
            _camera_index (int): Index of the camera to use.
        """
        self._camera_index = camera_index
        self._camera_capture = cv2.VideoCapture(self._camera_index)
        self._start_time = 0
        self._current_time = 0

    def release_camera(self):
        self._camera_capture.release()

    def next_screen(self):
        """
        Listen for key press to start the game.

        Returns:
            bool: True if user presses a key and the game is
            started, False otherwise.
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                return "continue"
        return "stay"

    def start_timer(self):
        """
        Start the game window timer.
        """
        self._start_time = pygame.time.get_ticks()

    def get_display_frame(self):
        """
        Get the camera frame and covert it to RGB.

        Returns:
            frame (numpy.ndarray): RGB image frame from the camera.
        """
        _, frame = self._camera_capture.read()
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def get_timer_string(self):
        """
        Get the current time in the countdown timer.

        Returns:
            counting_string (str): Current time in the countdown timer.
        """
        self._current_time = pygame.time.get_ticks() - self._start_time
        counting_string = f'{10-self._current_time//500}'
        return counting_string

    def determine_end_timer(self):
        """
        Determine if the timer is up.

        Returns:
            bool: True if the timer is up, False otherwise.
        """
        if 5000 - self._current_time < 0:
            return True
        return False
