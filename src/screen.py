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


def update(tile_grid: list, display_cursor: bool) -> None:
    """
    Update the screen.

    Args:
        tile_grid: The grid of tiles to display. Must contain a number of lists
            equal to this module's RESOLUTION_Y, and each list must be composed
            of a number of single characters equal to this module's RESOLUTION_X.
        display_cursor: Whether to display the cursor.
    """
    if display_cursor:
        tile_grid[cursor_position_y][cursor_position_x] = CURSOR_CHAR
    
    for i in range(RESOLUTION_Y):
        print(*tile_grid[i], sep="")
