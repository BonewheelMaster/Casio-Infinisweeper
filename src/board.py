import random
import utils

class Board:
    """
    The entire worldspace.

    The only data that are stored are the tiles that have been flagged
    and the tiles that have been revealed. All other data (whether a
    tile is a bomb, how many bombs are around a tile, etc.) are reproducibly
    calculated via the seed.

    A cache is used to store the positions of bombs currently on the screen.
    Each bomb costs a little more than 32 bytes. The parameters (position 
    and size) of the last screen are also stored, so that the cache is 
    only recalculated when it changes.

    Attributes:
        SEED (int): The seed the board was initialized with.
        BOMB_CHANCE (int): The chance for any given tile to be a bomb.
        AUTO_UNCOVER_TILES (bool): Whether the board automatically uncovers
            all tiles around a tile with no adjacent bombs.
        game_ended (bool): If the game has ended. If True, all tiles
            are revealed.
    """
    def __init__(
        self, seed: int, bomb_chance: int, auto_uncover_tiles: bool
    ) -> None:
        """
        Args:
            seed: Seed to use. Different seeds produce different maps.
            bomb_chance: The chance for any given tile to be a bomb. Value
                should be in [1-100].
            auto_uncover_tiles: Whether to automatically uncover all tiles around a
                tile with no adjacent bombs.
        """
        self.SEED = seed
        self.BOMB_CHANCE = bomb_chance
        self.AUTO_UNCOVER_TILES = auto_uncover_tiles

        self.game_ended = False

        # Tiles are stored in all of these as a tuple of their positions: (x, y).
        self._checked_tiles = set()
        self._flagged_tiles = set()
        # Stores all bombs on the screen that last called the get_tiles function.
        self._bomb_cache = set()

        # If these do not match the screen parameters in get_tiles, the cache is
        # recalculated and these are updated.
        self._last_screen_position_x = 0
        self._last_screen_position_y = 0
        self._last_screen_resolution_x = 0
        self._last_screen_resolution_y = 0


    def get_tile_grid(
        self, screen_position_x: int, screen_position_y: int, resolution_x: int,
        resolution_y: int, display_map: dict
    ) -> list:
        """
        Construct the tile grid for the purpose of displaying to a screen.

        Args:
            resolution_x: Amount of characters per line.
            resolution_y: Amount of lines on the screen.
            display_map: A mapping of states to displayable characters.
                The keys are the states and the values are the characters.

        Returns:
            The tile grid. The lists it contains are the rows (y); the characters
                on those rows are the columns (x). This means that to access
                the tile (x, y), use something like `tile_grid[y][x]`.
        """
        tile_grid = [
            [display_map["hidden"] for _ in range(resolution_x)]
                for _ in range(resolution_y)
        ]
        bombs = self._get_bombs_on_screen(
            screen_position_x, screen_position_y, resolution_x, resolution_y
        )
        nonzero_tiles = self._get_all_adjacent_bomb_counts(bombs)

        for v in range(resolution_y):
            for i in range(resolution_x):
                tile = (screen_position_x + i, screen_position_y + v)

                if tile in self._flagged_tiles:
                    # If tile is in flagged tiles, it is not in checked tiles.
                    tile_grid[v][i] = display_map["flagged"]
                    continue

                if tile not in self._checked_tiles and not self.game_ended:
                    continue

                if tile in nonzero_tiles:
                    tile_grid[v][i] = display_map[
                        "checked: {}".format(nonzero_tiles[tile])
                    ]
                    continue

                if tile not in bombs:
                    tile_grid[v][i] = display_map["safe"]
                    continue

                tile_grid[v][i] = display_map["bomb"]

        return tile_grid


    def flag_tile(self, position_x: int, position_y: int) -> None:
        """Flag or unflag a tile. Revealed tiles cannot be flagged."""
        if (position_x, position_y) in self._checked_tiles:
            return

        if (position_x, position_y) not in self._flagged_tiles:
            self._flagged_tiles.add( (position_x, position_y) )

        else:
            self._flagged_tiles.discard( (position_x, position_y) )


    def check_tile(self, position_x: int, position_y: int) -> None:
        """
        Set tile as checked. Flagged tiles cannot be revealed.

        Ends the game if the revealed tile is a bomb.
        """
        if (position_x, position_y) in self._flagged_tiles:
            return

        self._checked_tiles.add( (position_x, position_y) )

        if self._is_bomb(position_x, position_y):
            self.end_game()
            return

        if self._get_adjacent_bomb_count(position_x, position_y) == 0:
            self._auto_check_tiles(position_x, position_y)


    def _auto_check_tiles(self, position_x: int, position_y: int) -> None:
        return


    def _get_bombs_on_screen(
        self, screen_position_x: int, screen_position_y: int, resolution_x: int,
        resolution_y: int
    ) -> set:
        """
        Get all bombs currently on screen.

        This can be an intensive calculation, as it checks each tile if it is
        a bomb, which requires a random number for each tile. If the screen
        parameters have not changed since last call, simply returns a cache.

        Returns
            All the bombs on screen, with each bomb represented with the 
                tuple `(x, y)`. It does not matter if the bomb is covered.
        """
        if all([
            screen_position_x == self._last_screen_position_x,
            screen_position_y == self._last_screen_position_y,
            resolution_x == self._last_screen_resolution_x,
            resolution_y == self._last_screen_resolution_y
        ]):
            return self._bomb_cache
        
        bombs = set()

        for i in range(resolution_y):
            for v in range(resolution_x):
                if self._is_bomb(screen_position_x + v, screen_position_y + i):
                    bombs.add( (screen_position_x + v, screen_position_y + i) )

        self._bomb_cache = bombs
        self._last_screen_position_x = screen_position_x
        self._last_screen_position_y = screen_position_y
        self._last_screen_resolution_x = resolution_x
        self._last_screen_resolution_y = resolution_y

        return bombs


    def _is_bomb(self, position_x: int, position_y: int) -> bool:
        """
        Check if given tile is a bomb.

        Generates a random number in [0-100] using the seed mixed with the tile's
        positions. This is then compared with the bomb chance, and, if the chance
        is higher, the tile is a bomb.

        Returns
            Whether the tile is a bomb.
        """
        random.seed(utils.mix_seed(self.SEED, position_x, position_y))

        roll = random.randint(1, 100)
        return self.BOMB_CHANCE >= roll


    def _get_all_adjacent_bomb_counts(self, bombs: set) -> dict:
        """
        Get all tiles with bombs adjacent to them.

        Instead of running on every tile, this runs on every bomb given. This
        provides a considerable speed increase, especially with a low bomb chance.

        Args:
            bombs: The bombs to use. Each bomb is represented with its position
                as a tuple: (x, y).

        Returns:
            The keys are tiles with at least one adjacent bomb and the values
                are the amount of adjacent bombs.
        """
        bomb_counts = {}

        for bomb in bombs:
            for i in range(-1, 2):
                for v in range(-1, 2):
                    if (bomb[0] + i, bomb[1] + v) in bombs:
                        continue

                    try:
                        bomb_counts[ (bomb[0] + i, bomb[1] + v) ] += 1

                    except KeyError:
                        bomb_counts[ (bomb[0] + i, bomb[1] + v) ] = 1

        return bomb_counts


    def _get_adjacent_bomb_count(
        self, position_x: int, position_y: int
    ) -> int:
        """
        Get the number of adjacent bombs to one tile.

        Returns:
            The amount of bombs that are adjacent to the given tile.
        """
        bomb_count = 0

        for i in range(-1, 2):
            for v in range(-1, 2):
                if i == 0 and v == 0:
                    continue

                if self._is_bomb(position_x + i, position_y + v):
                    bomb_count += 1
        
        return bomb_count


    def end_game(self) -> None:
        """End the game as a result of revealing a bomb."""
        pass
