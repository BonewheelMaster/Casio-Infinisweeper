"""
Receive input and interpret it.

Attributes:
"""
import screen
import board
import utils
import config

# Move to config
input_map = {
	"4": lambda: move(-1, 0),
	"8": lambda: move(0, -1),
	"6": lambda: move(1, 0),
	"2": lambda: move(0, 1),
	"1": lambda: move(-1, 1),
	"7": lambda: move(-1, -1),
	"9": lambda: move(1, -1),
	"3": lambda: move(1, 1),
	"5": lambda: board.flag_tile(
		screen.screen_position_x + screen.cursor_position_x,
		screen.screen_position_y + screen.cursor_position_y
	),
	"0": lambda: board.check_tile(
		screen.screen_position_x + screen.cursor_position_x,
		screen.screen_position_y + screen.cursor_position_y
	),
	".": lambda: toggle_movement_mode(),
	"/": lambda: debug_reveal_all()
}

# Move the screen instead of the cursor if True. Modified
# by the toggle_movement_mode function.
screen_move = False


def take_input() -> None:
	"""
	Wait for input and run the according function/s.

	If the user inputs multiple commands, all will be run.
	"""
	for char in input(generate_prompt()):
		if char not in input_map.keys():
			continue

		input_map[char]()


def generate_prompt() -> str:
	"""
	Create the context-dependant input prompt.

	Information displayed includes
		- Mode of movement (cursor or screen)

	Returns:
		string: The prompt.
	"""
	prompt = "CUR" if not screen_move else "SCR"
	prompt += "> "

	return prompt


def move(offset_x: int, offset_y: int) -> None:
	"""
	Move the cursor or the screen.

	Args:
		offset_x (int): Amount to move the cursor or screen on the x-axis. Positive
			values move them right, while negative values move them left.

		offset_y (int): Amount to move the cursor or screen on the y-axis. Positive
			values move them down, while negative values move them up.
	"""
	if screen_move:
		screen.screen_position_x += offset_x
		screen.screen_position_y += offset_y
	
	else:
		screen.cursor_position_x += offset_x
		screen.cursor_position_y += offset_y

		screen.cursor_position_x = utils.clamp(
			screen.cursor_position_x,
			0,
			screen.RESOLUTION_X-1
		)
		screen.cursor_position_y = utils.clamp(
			screen.cursor_position_y,
			0,
			screen.RESOLUTION_Y-1
		)


def flag_tile() -> None:
	"""
	Flag or unflag current tile. Revealed tiles cannot be flagged.
	"""
	board.flag_tile(
		screen.screen_position_x + screen.cursor_position_x,
		screen.screen_position_y + screen.cursor_position_y
	)


def check_tile() -> None:
	board.check_tile(
		screen.screen_position_x + screen.cursor_position_x,
		screen.screen_position_y + screen.cursor_position_y
	)


def toggle_movement_mode() -> None:
	global screen_move
	
	screen_move = not screen_move


def debug_reveal_all() -> None:
	board.debug_revealed = not board.debug_revealed