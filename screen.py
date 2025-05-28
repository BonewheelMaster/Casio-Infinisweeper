"""
Display to the screen.

Attributes:
    Defined in config:
        RESOLUTION_X: The amount of characters on a line.
        RESOLUTION_Y: The amount of lines.
        CURSOR_CHAR: The character used to display the cursor. This replaces
            whatever tile the cursor is on.
        DISPLAY_MAP: The map of states to characters.

    screen_position_x: The x coordinate of the top-left tile of the screen.
    screen_position_y: The y coordinate of the top-left tile of the screen.
    cursor_position_x: The x coordinate of the cursor.
    cursor_position_y: The y coordinate of the cursor.
"""
import config

RESOLUTION_X = config.RESOLUTION_X
RESOLUTION_Y = config.RESOLUTION_Y
CURSOR_CHAR = config.CURSOR_CHAR
DISPLAY_MAP = config.DISPLAY_MAP

screen_position_x = 0
screen_position_y = 0
cursor_position_x = 0
cursor_position_y = 0


def update(board) -> None:
    """
    Update the screen.

    Args:
        board: The board object to get tiles from. Must have a get_tile_grid function. 
    """
    tile_grid = board.get_tile_grid(
        screen_position_x, screen_position_y, RESOLUTION_X, RESOLUTION_Y,
        DISPLAY_MAP
    )
    tile_grid[cursor_position_y][cursor_position_x] = CURSOR_CHAR
    
    for i in range(RESOLUTION_Y):
        print(tile_grid[i])
