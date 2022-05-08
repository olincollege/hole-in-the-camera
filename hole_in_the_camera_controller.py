"""
Hole in the wall game controller.
"""
from abc import ABC, abstractmethod
import pygame
import cv2


class HoleInTheCameraController(ABC):
    """
    Create abstract class for the game controller.

    Attributes:
        _start_time (float): Start time of the game.
        _current_time (float): Current time in the countdown timer.
    """

    def __init__(self):
        """
        Initialize the game controller object with two time objects set to 0.
        """
        self._start_time = 0
        self._current_time = 0

    @property
    def start_time(self):
        """
        Return the start_timer value.
        """
        return self._start_time

    @abstractmethod
    def next_screen(self):
        """
        Get the next screen to display.
        """

    @abstractmethod
    def start_timer(self):
        """
        Start the countdown timer for each round.
        """

    @abstractmethod
    def get_display_frame(self):
        """
        Get the current frame to display.
        """

    @abstractmethod
    def get_timer_string(self):
        """
        Get the current timer string.
        """

    @abstractmethod
    def determine_end_timer(self):
        """
        Determine when the countdown has ended.
        """


class OpenCVController(HoleInTheCameraController):
    """
    OpenCV implementation of the HoleInTheWallController class.

    Attributes:
        _camera_index (int): Index of the camera to use.
        _camera_capture (numpy.ndarray): Current caputured video frame.
    """

    def __init__(self, camera_index):
        """
        Initialize the OpenCV controller.

        Args:
            _camera_index (int): Index of the camera to use.
        """
        super().__init__()
        self._camera_index = camera_index
        self._camera_capture = cv2.VideoCapture(self._camera_index)

    @property
    def camera_capture(self):
        """
        Return the camera capture object.
        """
        return self._camera_capture

    @property
    def camera_index(self):
        """
        Return the camera index.
        """
        return self._camera_index

    def release_camera(self):
        """
        Release the camera.
        """
        self._camera_capture.release()

    def next_screen(self):
        """
        This function listens for user keypresses. If ESCAPE or the window X is
        clicked, the function returns "quit" to signify termination of the
        game. If any other key is clicked, function returns "continue" to call
        the next screen to be displayed and if no valid event is detected,
        "stay is returned to ensure that the current screen is maintained.

        Returns:
            (str): A string representing that action to be taken next relative
                to the current screen. Three potential outputs are "quit",
                "continue", and "stay".
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE\
                or event.type == pygame.QUIT:
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
        # camera frame resized to ensure it fits onto pygame display.
        frame = cv2.resize(frame, (640, 480))
        # frame recolored as pygame displays RGB formats, whereas OpenCV
        # returns BGR formats.
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def get_timer_string(self):
        """
        Get the current time in the countdown timer.

        Returns:
            counting_string (str): Current time in the countdown timer.
        """
        self._current_time = pygame.time.get_ticks() - self._start_time
        # 500 chosen to divide time by instead of 1000 to create a faster
        # timer that isn't exactly related to seconds.
        counting_string = f"{10-self._current_time//500}"
        return counting_string

    def determine_end_timer(self):
        """
        Determine if time is up.

        Returns:
            bool: True if the time is up, False otherwise.
        """
        # 5000 used to keep consistent with the timer click every 500 ms as
        # defined by get_timer_string.
        if 5000 - self._current_time < 0:
            return True
        return False
