"""
Hole in the wall game controller.
"""
import cv2
import pygame
from abc import ABC, abstractmethod

class HoleInTheWallController(ABC):
    """
    Create abstract class for the game controller.
    """
    def __init__(self):
        pass
    def start_game(self):
        """
        Start the game.
        """
        pass
    
class OpenCVController(HoleInTheWallController):
    def __init__(self, camera_index):
        super.__init__()
        self.camera_index = camera_index
        self.camera_capture = cv2.VideoCapture(self.camera_index)

    def start_game(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                return True
            else:
                return False

    def quit_game(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
    
    