import board
import screen
import usrinput

game_board = board.Board(12345, 5)
game_screen = screen.Screen(21, 6)

#for i in range(game_board.size_y):
#	for v in range(game_board.size_x):
#		print(game_board.get_tile(v, i).display_char, end="")

#	print()

while True:
	usrinput.take_input()

#game_board.set_tile(5, 5, "checked: 3")
game_board.check_tile(2, 6)
