import screen
import usrinput
import board
import config

game_board = board.Board(
    config.SEED, config.BOMB_CHANCE, config.AUTO_UNCOVER_TILES
)

while True:
    tile_grid = game_board.get_tile_grid(
        screen.screen_position_x, screen.screen_position_y, screen.RESOLUTION_X,
        screen.RESOLUTION_Y, screen.DISPLAY_MAP
    )
    screen.update(tile_grid)
    usrinput.take_input(game_board)
