"""
Hole in the wall game view.
"""
import pygame
from abc import ABC, abstractmethod

class HoleInTheWallView(ABC):
    """
    Create abstract class for game view.
    """

    def __init__(self):
        pass

    @abstractmethod
    def initialize_view(self):
        pass
        
    @abstractmethod
    def display_text(self, texts):
        pass
    
    @abstractmethod
    def display_introduction(self):
        pass


class PygameViewer(HoleInTheWallView):
    """
    Initializing game window view.

    Attributes:
        BLACK (tuple): RGB value for black. 
        WHITE (tuple): RGB value for white.
        GRAY (tuple): RGB value for gray.
        BLUE (tuple): RGB value for blue.
        BLUE_BACKGROUND (tuple): RGB value for blue background.
        FONT (str): Font name.
        FONT_SIZE (int): Font size.
        _display_size (tuple): The size of the display.
        _screen (pygame.Surface): The surface of the game window.
    """
    BLACK = (0,0,0)
    RED = (255,0,0)
    GRAY = (200,200,200)
    WHITE = (255,255,255)
    BLUE = (50,50,200)
    BLUE_BACKGROUND = (153,204,255)
    FONT = "Helvetica"
    FONT_SIZE = 40

    def __init__(self, display_size):
        """
        Initialize the game view.
        
        Args:
            display_size (tuple): The size of the display.
        """
        super.__init__()
        self._display_size = display_size
        self._screen = pygame.display.set_mode(self._display_size, pygame.RESIZEABLE)
        screen = pygame.display.set_mode((display_size[1], display_size[0]))

    def initialize_view(self):
        """
        Initialize the game view.
        """
        pygame.init()
        pygame.set_caption("Hole in the Camera")
        icon = pygame.image.load('images/assets/gameicon.png')
        pygame.display.set_icon(icon)
        font = pygame.font.Sysfont(self.FONT, self.FONT_SIZE)
    
    def display_text(self, texts):
        """
        Display text on the game window.

        Args:
            texts (list): The text to be displayed.
        """
        y_offset = 0
        background = pygame.image.load('background.png')
        self._screen.blit(background, (0,0))
        for text in texts:
            _, font_height = self.font.size(text)
            image = self.font.render(text, True, self.WHITE, self.BLACK)
            self._screen.blit(image, (20, 200+y_offset))
            y_offset += font_height
        pygame.display.update()

    def display_introduction(self):
        """
        Display the introduction text.
        """
        welcome_text = ["Welcome to Hole in the Camera!", "Press any key to continue."]
        self.display_text(welcome_text)
    
    def display_instructions(self):
        """
        Display the instructions text.
        """
        instruction_text = ["Instructions"]
        self.display_text(instruction_text)
        
    def display_frame(self, frame, timer_text):
        """
        Display the frame on the game window.

        Args:
            frame (numpy.ndarray): The frame to be displayed.
            timer_text (str): The timer text to be displayed.
        """
        self._screen.blit(frame, (0,0))
        counting_text = self.font.render(timer_text, 1, self.WHITE)
        counting_rect = counting_text.get_rect(bottomright=self._screen.get_rect().bottomright)
        self._screen.blit(counting_text, counting_rect)
        pygame.display.update()

    def display_win(self, win, score):
        """
        Check if the user has won or lost and display text in
        pygame window corresponds to the result.

        Arg:
            score (float): A float between 0 and 1 (inclusive) that represents the
            accuracy of how well player fits through the hole.
            win (bool): True if the user has won, False otherwise.
        """
        if win:
            lost_text = [f"You lost! Your score is {score*100}"]
            self.display_text(lost_text)
        else:
            won_text = [f"You won! You fit through the hole!"]
            self.display_text(won_text)