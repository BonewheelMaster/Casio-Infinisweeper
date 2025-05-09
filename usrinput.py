"""
"""

input_map = { # TODO: Turn these into lambda funcs so they don't run here.
	"4": move_cursor(-1, 0),
	"8": move_cursor(0, -1),
	"6": move_cursor(1, 0),
	"2": move_cursor(0, -1),
	"1": move_cursor(-1, -1),
	"7": move_cursor(-1, 1),
	"9": move_cursor(1, 1),
	"3": move_cursor(1, -1),
	"5": flag_tile(),
	"0": check_tile(),
	".": toggle_movement_mode(),
}

def take_input():
	input_map[input(">")]()

def move_cursor(offset_x: int, offset_y: int) -> None:
	print("Move cursor {} x and {} y.".format(offset_x, offset_y))

def flag_tile():
	print("flag tile")

def check_tile():
	print("check tile")

def toggle_movement_mode():
	print("Toggle movement mode.")
