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
		screen_position_x: int, screen_position_y: int, resolution_x: int,
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
			[display_map[("hidden")] * resolution_x] * resolution_y
		]
		bombs = self._get_bombs_on_screen(
			screen_position_x, screen_position_y, resolution_x, resolution_y
		)
		nonzero_tiles = self_get_all_adjacent_bomb_counts(bombs)

		for tile in self._checked_tiles:
			if tile in nonzero_tiles:
				tile_grid[tile[1]][tile[0]] = display_map[
					"checked: {}".format(nonzero_tiles[tile])
				]

			elif tile in bombs:
				tile_grid[tile[1]][tile[0]] = display_map["bomb"]

			else:
				tile_grid[tile[1]][tile[0]] = display_map["safe"]

		for tile in self._flagged_tiles:
			tile_grid[tile[1]][tile[0]] = display_map["flagged"]

		if self.game_ended:
			# Reveal all bombs, regardless of if they have been checked.
			for tile in bombs:
				tile_grid[tile[1]][tile[0]] = display_map["bomb"]

		tile_grid = self_auto_check_tiles(tile_grid, nonzero_tiles, display_map)

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

		if (position_x, position_y) in self._bomb_cache:
			self.end_game()


	# def _auto_check_tiles(self, position_x: int, position_y: int) -> None:
	# 	"""
	# 	Uncover every tile adjacent to a safe tile.

	# 	Called when a tile is checked by the user and has 0 bombs around it.
	# 	"""
	# 	if not self.AUTO_UNCOVER_TILES:
	# 		return

	# 	for i in range(-1, 2):
	# 		for v in range(-1, 2):
	# 			if (position_x + i, position_y + v) in self._checked_tiles:
	# 				continue
					
	# 			self._checked_tiles.add(position_x + i, position_y + v)


	def _auto_check_tiles(
			self, tile_grid: list, nonzero_tiles: list, display_map: dict
	) -> list:
		"""
		Automatically uncover all tiles around an uncovered safe tile.

		Args:
			tile_grid: The tile grid to modify.
			nonzero_tiles: All tiles on the grid that aren't safe (not including bombs).
			display_map: The map of states to characters.

		Returns:
			The new tile grid.
		"""
		# TODO: Consider using recursion.
		done = False

		# This is horrid. TODO: Make this better.
		# TODO: Check performance.
		while not done:
			done = True
			
			for row in tile_grid:
				for tile in row:
					if tile != display_map["safe"]:
						continue
						
					for i in range(-1, 2):
						for v in range(-1, 2):
							# TODO: Confirm functionality.
							if tile_grid[row][tile] == display_map["hidden"]:
								tile_grid[row][tile] = display_map["safe"]
								done = False

		return tile_grid


	def _get_bombs_on_screen(
		screen_position_x: int, screen_position_y: int, resolution_x: int,
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
		if all(
			screen_position_x == self._last_screen_position_x,
			screen_position_y == self._last_screen_position_y,
			resolution_x == self._last_screen_resolution_x,
			resolution_y == self._last_screen_resolution_y
		):
			return self._bomb_cache
		
		bombs = set()

		for i in range(resolution_y):
			for v in range(resolution_x):
				if _is_bomb(screen_position_x + v, screen_position_y + i):
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
		self, position_x: int, position_y: int, bombs: set
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

				if (position_x + i, position_y + v) in bombs:
					bomb_count += 1
		
		return bomb_count


	def end_game(self) -> None:
		"""End the game as a result of revealing a bomb."""
		pass
