"""
Main runner code for hole in the camera game.
"""
from hole_in_the_wall_controller import OpenCVController
from hole_in_the_wall_view import PygameViewer
from hole_in_the_wall_model import HoleInTheWallGame
import cv2
import pdb
import pygame

camera_index = 0
display_size = (640, 480)

game_controller = OpenCVController(camera_index)
game_view = PygameViewer(display_size)
game_model = HoleInTheWallGame()

game_view.initialize_view()
game_view.display_background(0)
playing_game = True
start_state = True
while True:
    game_view.display_introduction()
    if game_controller.quit_game():
        break
game_controller.start_timer()
