"""
Main runner code for hole in the camera game.
"""
from hole_in_the_wall_controller import OpenCVController
from hole_in_the_wall_view import PygameViewer
from hole_in_the_wall_model import HoleInTheCameraGame
import sys

# Set up view constants
CAMERA_INDEX = 0
DISPLAY_SIZE = (640, 480)

# Create controller, model, and view objects.
game_controller = OpenCVController(CAMERA_INDEX)
game_view = PygameViewer(DISPLAY_SIZE)
game_model = HoleInTheCameraGame()

# Start the game and initialize pygame
game_view.initialize_view()
# set current game state to start screen
current_game_state = 'start_screen'


def game_start():
    """
    Display the introduction screen and wait for the user to continue
    or quit the game.

    Returns:
        (str): The next game state.
    """
    game_view.display_introduction()
    next_screen_state = game_controller.next_screen()
    if next_screen_state == "continue":
        return "instruction_screen"
    if next_screen_state == "quit":
        sys.exit()
    return "start_screen"


def show_instructions():
    """
    Display the instructions screen and wait for the user to continue
    or quit the game.

    Returns:
        (str): The next game state.
    """
    game_view.display_instructions()
    next_screen_state = game_controller.next_screen()
    if next_screen_state == "continue":
        return 'playing_game'
    if next_screen_state == "quit":
        sys.exit()
    return "instruction_screen"


def run_trial():
    """
    Run a single trial of the game.

    Returns:
        (str): The next game state.
    """
    hole_mask, joints_file = game_model.get_mask_and_joints()
    game_controller.start_timer()
    current_timer_value = game_controller.get_timer_string()
    while True:
        current_frame = game_controller.get_display_frame()
        current_timer_value = game_controller.get_timer_string()
        game_view.display_frame(current_frame, current_timer_value, hole_mask)
        if game_controller.next_screen() == "quit":
            sys.exit()
        if game_controller.determine_end_timer():
            final_frame = current_frame
            break
    game_model.analyze_frame(final_frame)
    game_model.parse_for_joint_positions()
    game_model.compute_accuracy(joints_file)
    game_view.display_win(game_model.check_win(), game_model.trial_score)
    next_screen_state = game_controller.next_screen()
    while next_screen_state == "stay":
        next_screen_state = game_controller.next_screen()
    if next_screen_state == "quit":
        sys.exit()
    if game_model.check_win():
        return "playing_game"
    return "game_complete"


def end_game():
    """
    Display the end game screen and wait for the user to quit the game.

    Returns:
        (str): The next game state.
    """
    game_view.display_end_game(game_model.total_score)
    next_screen_state = game_controller.next_screen()
    while next_screen_state == "stay":
        if next_screen_state == "quit":
            sys.exit()
        next_screen_state = game_controller.next_screen()
    return "game_complete"


# Dictionary of game states and their corresponding functions.
GAME_STATES = {
    "start_screen": game_start,
    "instruction_screen": show_instructions,
    "playing_game": run_trial,
    "game_complete": end_game
}

# Run the game until the user quits.
while game_model.num_holes_remaining() > 0:
    current_game_state = GAME_STATES[current_game_state]()
    if current_game_state == "game_complete":
        break

# Close the game.
current_game_state = "game_complete"
game_controller.release_camera()
GAME_STATES[current_game_state]()
