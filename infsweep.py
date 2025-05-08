import game_board

board = game_board.board(21, 6)

for i in range(board.size_y):
    for v in range(board.size_x):
        print(board.get_tile(v, i).display_char, end="")

    print()
    
input()

board.set_tile(5, 5, "checked: 3")
board.check(2, 6)
