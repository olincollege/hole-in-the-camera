"""
Main runner code for hole in the camera game.
"""
import sys
from hole_in_the_camera_controller import OpenCVController
from hole_in_the_camera_view import PygameViewer
from hole_in_the_camera_model import HoleInTheCameraGame

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
CURRENT_GAME_STATE = 'start_screen'


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


def run_game():
    """
    Run each round of the game.

    Returns:
        (str): The next game state.
    """
    total_trials = game_model.num_holes_remaining()
    num_trials_remaining = game_model.num_holes_remaining()
    while num_trials_remaining > 0:
        game_view.display_round_screen(total_trials-num_trials_remaining + 1)
        next_screen_state = game_controller.next_screen()
        while next_screen_state == "stay":
            next_screen_state = game_controller.next_screen()
        hole_mask, joints_file = game_model.get_mask_and_joints()
        game_controller.start_timer()
        current_timer_value = game_controller.get_timer_string()
        while True:
            current_frame = game_controller.get_display_frame()
            current_timer_value = game_controller.get_timer_string()
            game_view.display_frame(
                current_frame, current_timer_value, hole_mask)
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
        num_trials_remaining = game_model.num_holes_remaining()
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
    "playing_game": run_game,
    "game_complete": end_game
}

# Run the game until the user quits.
while True:
    CURRENT_GAME_STATE = GAME_STATES[CURRENT_GAME_STATE]()
    if CURRENT_GAME_STATE == "game_complete":
        break

# Close the game.
CURRENT_GAME_STATE = "game_complete"
game_controller.release_camera()
GAME_STATES[CURRENT_GAME_STATE]()
