"""
Hole in the wall game view.
"""
from abc import ABC, abstractmethod
import pygame
from pygame.locals import *
from pygame import mixer
import cv2 as cv


class HoleInTheWallView(ABC):
    """
    Create abstract class for game view.
    """

    def __init__(self, display_size):
        """
        Initialize the game view object.

        Args:
            display_size (tuple): Size of the display.
        """
        self._display_size = display_size

    @abstractmethod
    def initialize_view(self):
        """
        Initialize the game view.
        """
        pass

    @abstractmethod
    def display_introduction(self):
        """
        Display the introduction screen.
        """
        pass

    @abstractmethod
    def display_instructions(self):
        """
        Display the instructions screen.
        """
        pass

    @abstractmethod
    def display_frame(self, frame, timer_text, camera_mask):
        """
        Display the current frame.

        Args:
            frame (numpy.ndarray): Current frame to display.
            timer_text (str): Current timer value.
            camera_mask (numpy.ndarray): Current camera mask.
        """
        pass

    @abstractmethod
    def display_win(self, win_state, score):
        """
        Display the win screen.

        Args:
            win_state (str): Win state.
            score (int): Current score.
        """
        pass

    @abstractmethod
    def display_end_game(self, score):
        """
        Display the end game screen.

        Args:
            score (int): Final player score.
        """
        pass


class PygameViewer(HoleInTheWallView):
    """
    Initializing game window view.

    Attributes:
        BLACK (tuple): RGB value for black.
        RED (tuple): RGB value for red.
        GRAY (tuple): RGB value for gray.
        WHITE (tuple): RGB value for white.
        BLUE (tuple): RGB value for blue.
        FONT (str): Font name.
        FONT_SIZE (int): Font size.
        BACKGROUND_PATHS (list): The paths of the background images.
        _screen (pygame.Surface): The game window.
        font (pygame.font.SysFont): The font used to display text.
    """
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GRAY = (200, 200, 200)
    WHITE = (255, 255, 255)
    BLUE = (50, 50, 200)
    FONT_NAME = "Helvetica"
    FONT_SIZE = 40
    BACKGROUND_PATHS = ["images/assets/background.jpg",
                        "images/assets/lost_background.jpg",
                        "images/assets/win_background.jpg"
                        ]

    def __init__(self, display_size):
        """
        Initialize the game view and music.

        Args:
            display_size (tuple): The size of the display.
        """
        super().__init__(display_size)
        pygame.font.init()
        self._screen = pygame.display.set_mode(
            self._display_size, pygame.RESIZABLE)
        self.font = pygame.font.SysFont(self.FONT_NAME, self.FONT_SIZE)

        mixer.init()
        mixer.music.load("Sound/No Doubt - Yung Logos.wav")
        mixer.music.play()

    @property
    def screen(self):
        """
        Return the game window.

        Returns:
            pygame.Surface: The game window.
        """
        return self._screen

    def initialize_view(self):
        """
        Initialize the game view by creating game window title, icon, and
        font style.
        """
        pygame.init()
        pygame.display.set_caption("Hole in the Camera")
        icon = pygame.image.load('images/assets/gameicon.jpg')
        pygame.display.set_icon(icon)

    def _display_background(self, background_num):
        """
        Display background image.

        Args:
            background_path (str): The path of a png file as the background
            of the game window
        """
        background = pygame.image.load(self.BACKGROUND_PATHS[background_num])
        background = pygame.transform.scale(background, (640, 480))
        self._screen.blit(background, (0, 0))

    def _display_text(self, texts):
        """
        Display text on the game window with background image.

        Args:
            texts (list): The text to be displayed.
        """
        y_offset = 0
        for text in texts:
            _, font_height = self.font.size(text)
            image = self.font.render(text, True, self.WHITE, self.BLACK)
            self._screen.blit(image, (55, 210+y_offset))
            y_offset += font_height
        pygame.display.update()

    def display_introduction(self):
        """
        Display the introduction text.
        """
        welcome_text = ["Welcome to Hole in the Camera!",
                        "Press any key to continue",
                        "Or press esc to exit (Bye!)"]
        self._display_background(0)
        self._display_text(welcome_text)

    def display_instructions(self):
        """
        Display the instructions text.
        """
        instruction_text = ["Instructions"]
        self._display_background(0)
        self._display_text(instruction_text)

    def display_instructions_content(self):
        """
        Display the detailed content of instructions.
        """
        instruction_content = ["Adjust your pose (or camera) to \
                                fit into the holes",
                               "You have 10 seconds each round"]

    def display_frame(self, frame, timer_text, camera_mask):
        """
        Display the frame on the game window.

        Args:
            frame (numpy.ndarray): The frame to be displayed.
            timer_text (str): The timer text to be displayed.
            mask (numpy.ndarray): The mask to be overlaid on the frame.
        """
        frame = cv.bitwise_and(frame, camera_mask)
        frame = pygame.transform.rotate(
            pygame.surfarray.make_surface(frame), -90)
        self._screen.blit(frame, (0, 0))
        counting_text = self.font.render(timer_text, 1, self.WHITE)
        counting_rect = counting_text.get_rect(
            bottomright=self._screen.get_rect().bottomright)
        self._screen.blit(counting_text, counting_rect)
        pygame.display.update()

    def display_win(self, win_state, score):
        """
        Check if the user has won or lost and display text in
        pygame window corresponds to the result.

        Arg:
            score (float): A float between 0 and 1 (inclusive) that represents
            the accuracy of how well player fits through the hole.
            win (bool): True if the user has won, False otherwise.
        """
        if win_state:
            mixer.music.stop()
            win_sound = mixer.Sound(
                "Sound/mixkit-fantasy-game-success-notification-270.wav")
            win_sound.play()
            won_text = [f"Your score is: {int(score)}"]
            self._display_background(2)
            self._display_text(won_text)
        else:
            mixer.music.stop()
            crash_sound = mixer.Sound("Sound/Crash .wav")
            crash_sound.play()
            lost_text = ["You lost!", f"Your score is {int(score)}"]
            self._display_background(1)
            self._display_text(lost_text)

    def display_end_game(self, score):
        """
        Display the end game text.

        Args:
            score (float): A float that represents the accuracy of
            how well player fits through the hole.
        """
        self._display_background(2)
        self._display_text(["Game Over!", f"Final Score: {int(score)}/700"])
