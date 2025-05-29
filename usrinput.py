"""
Receive input and interpret it.

Attributes:
    Defined in config:
        INPUT_MAP: The map of input characters to functions.
"""
import screen
import utils

INPUT_MAP = {
    "4": lambda board: move(-1, 0),
    "8": lambda board: move(0, -1),
    "6": lambda board: move(1, 0),
    "2": lambda board: move(0, 1),
    "1": lambda board: move(-1, 1),
    "7": lambda board: move(-1, -1),
    "9": lambda board: move(1, -1),
    "3": lambda board: move(1, 1),
    "5": lambda board: board.flag_tile(
        screen.screen_position_x + screen.cursor_position_x,
        screen.screen_position_y + screen.cursor_position_y
    ),
    "0": lambda board: board.check_tile(
        screen.screen_position_x + screen.cursor_position_x,
        screen.screen_position_y + screen.cursor_position_y
    ),
    ".": lambda board: toggle_movement_mode(),
}

# Move the screen instead of the cursor if True. Modified
# by the toggle_movement_mode function.
_screen_move = False


def take_input(board) -> None:
    """
    Wait for input and run the according function/s.

    If the user inputs multiple commands, all will be run in order.
    
    Args:
        board: The board object to modify. Must have flag_tile and check_tile functions.
    """
    for char in input(generate_prompt()):
        if char not in INPUT_MAP:
            continue

        INPUT_MAP[char](board)


def generate_prompt() -> str:
    """
    Create the context-dependant input prompt.

    Information displayed includes
        - Mode of movement (cursor or screen)

    Returns:
        The prompt.
    """
    prompt = "CUR" if not _screen_move else "SCR"
    prompt += "> "

    return prompt


def move(offset_x: int, offset_y: int) -> None:
    """
    Move the cursor or the screen.

    Decides between cursor or screen using internal state.

    Args:
        offset_x: Amount to move the cursor or screen on the x-axis. Positive
            values move them right, while negative values move them left.

        offset_y: Amount to move the cursor or screen on the y-axis. Positive
            values move them down, while negative values move them up.
    """
    if _screen_move:
        screen.screen_position_x += offset_x
        screen.screen_position_y += offset_y
    
    else:
        screen.cursor_position_x += offset_x
        screen.cursor_position_y += offset_y

        # Prevent cursor from going off screen.
        screen.cursor_position_x = utils.clamp(
            screen.cursor_position_x,
            0,
            screen.RESOLUTION_X - 1
        )
        screen.cursor_position_y = utils.clamp(
            screen.cursor_position_y,
            0,
            screen.RESOLUTION_Y - 1
        )


def toggle_movement_mode() -> None:
    """Switch between moving the screen and moving the cursor."""
    global _screen_move
    
    _screen_move = not _screen_move
