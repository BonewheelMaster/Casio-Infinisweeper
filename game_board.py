# TODO: consider whether tiles should know their pos and display the right number,
# or if higher levels should manage that.
class tile:
    def __init__(self, is_bomb: bool, display_char: str):
        self.is_bomb = is_bomb
        self.display_char = display_char


class board:
    def __init__(self, resolution_x: int, resolution_y: int, tile_display_states: dict = None) -> None:
        if tile_display_states is None:
            self.tile_display_states = {
               #"checked: " + str(i): str(i) for i in range(10)
               "unknown": "?"
            }

        self.size_x = resolution_x
        self.size_y = resolution_y

        self.board = [
            [ tile(False, self.tile_display_states["unknown"]) ] * self.size_x
        ] * self.size_y

    # TODO: fix or remove me
    def set_tile(self, pos_x: int, pos_y: int, state: str) -> None:
        # Argument Validation
        if any([
                (0 > pos_x or pos_x > len(board[0])),
                (0 > pos_y or pos_y > len(board)),
                state not in self.tile_display_states.keys()
            ]):
            raise ValueError(
                "pos_x must be an integer between 0 and {}, ".format(len(board[0]))
                + "pos_y must be an integer between 0 and {}, and ".format(len(board))
                + "state must be a str whose value is in {}.".format(list(tile_states.keys()))
            )

        pass

    def get_tile(self, pos_x: int, pos_y: int) -> tile:
        return self.board[pos_y][pos_x]

