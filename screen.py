"""
The screen.

Attributes:
"""
import config
import board

RESOLUTION_X = config.RESOLUTION_X
RESOLUTION_Y = config.RESOLUTION_Y

DISPLAY_MAP = config.DISPLAY_MAP

CURSOR_CHAR = config.CURSOR_CHAR

screen_position_x = 0
screen_position_y = 0

cursor_position_x = 0
cursor_position_y = 0


def update() -> None:
	for i in range(RESOLUTION_Y):
		for v in range(RESOLUTION_X):
			if v == cursor_position_x and i == cursor_position_y:
				print(CURSOR_CHAR, end="")
				continue

			print(DISPLAY_MAP[board.get_tile_state(
				screen_position_x + v,
				screen_position_y + i
			)], end="")

		print()
