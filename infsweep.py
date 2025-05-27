import screen
import usrinput
import board
import config

game_board = board.Board(
    config.SEED, config.BOMB_CHANCE, config.AUTO_UNCOVER_TILES
)

while True:
    screen.update(game_board)
    usrinput.take_input(game_board)
