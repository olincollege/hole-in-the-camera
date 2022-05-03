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
    hole_mask, joints_file = game_model.get_mask_and_joints()
    # pdb.set_trace()
    game_controller.start_timer()
    current_timer_value = game_controller.get_timer_string()
    # game_controller.start_camera()
    while True:
        current_frame = game_controller.get_camera_frame()
        current_timer_value = game_controller.get_timer_string()
        game_view.display_frame(current_frame, current_timer_value, hole_mask)
        if game_controller.determine_end_timer():
            final_frame = current_frame
            break
    game_model.analyze_frame(final_frame)
    game_model.parse_for_joint_positions()
    game_model.compute_accuracy(joints_file)
    game_view.display_win(game_model.check_win(), game_model.trial_score)
    if game_model.check_win():
        while not game_controller.next_screen():
            continue
        return "playing_game"
    return "player_lost"
    
def end_game():
    game_view.display_end_game(game_model.total_score)
    while not game_controller.next_screen():
        continue

game_states = {
    "start_screen": game_start,
    "instruction_screen": show_instructions,
    "playing_game": run_trial,
    "player_lost": end_game
}

while game_model.num_holes_remaining() > 0:
    current_game_state = game_states[current_game_state]()
    if game_controller.quit_game():
        break

game_controller.release_camera()
current_game_state = "player_lost"
game_states[current_game_state]()