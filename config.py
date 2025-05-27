"""Configuration options"""
# [SCREEN]
# Number of characters to be displayed per line.
RESOLUTION_X = 21
# Number of lines to be displayed.
RESOLUTION_Y = 6
# Which characters should be mapped to which states. Each state should only be
# mapped to one character.
DISPLAY_MAP = {
	"flagged": "F",
	"hidden": "?",
	"bomb": "@",
	"safe": " ",
}
DISPLAY_MAP.update({"checked: {}".format(i): str(i) for i in range(1, 10)})
# Character to display for the cursor. This replaces whatever character the
# cursor is over.
CURSOR_CHAR = "#"


# [BOARD]
# Seed to use for the map. Changing the seed changes where bombs are placed.
SEED = 12345
# Chance [0-100] for any given tile to be a bomb.
BOMB_CHANCE = 5
# Whether to automatically uncover all tiles around a tile with no bombs
# around it.
AUTO_UNCOVER_TILES = True


# [INPUT]
# The mapping of key commands to functions. These functions are defined
# in usrinput.py.
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
