import board

game_board = board.board(21, 6)

for i in range(game_board.size_y):
    for v in range(game_board.size_x):
        print(game_board.get_tile(v, i).display_char, end="")

    print()
    
input()

game_board.set_tile(5, 5, "checked: 3")
game_board.check(2, 6)
