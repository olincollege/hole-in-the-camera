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
current_game_state = 'start_screen'

def game_start():
    game_view.display_background(0)
    game_view.display_introduction()
    if game_controller.next_screen():
        return "instruction_screen"
    return "start_screen"

def show_instructions():
    game_view.display_background(0)
    game_view.display_instructions()
    if game_controller.next_screen():
        return 'playing_game'
    return "instruction_screen"

def run_trial():
    hole_mask = game_model.get_mask()
    game_controller.start_timer()
    current_timer_value = game_controller.get_timer_string()
    while not game_controller.determine_end_timer():
        current_frame = game_controller.get_camera_frame()
        current_timer_value = game_controller.get_timer_string()
        game_view.display_frame(current_frame, current_timer_value, hole_mask)

game_states = {
    "start_screen": game_start,
    "instruction_screen": show_instructions,
    "playing_game": run_trial
}

while True:
    current_game_state = game_states[current_game_state]()
    if game_controller.quit_game():
        break