import random

class Board:
	"""
	The entire worldspace.

	The only data that are stored are the tiles that have been flagged
	and the tiles that have been revealed. All other data (whether a
	tile is a bomb, how many bombs are around a tile, etc.) are reproducibly
	calculated via the seed.
	"""
	def __init__(self, seed: int, bomb_chance: float) -> None:
		"""
		Args:
			seed (int): Initial seed to use. This of course determines
				where all bombs are.

			bomb_chance (float): The chance (from 0-1) for each tile to
				be a bomb.
		"""
		self.seed = seed
		self.bomb_chance = bomb_chance

		self.checked_tiles = []
		self.flagged_tiles = []

	def check_tile(self, position_x: int, position_y: int) -> None:
		"""
		Set tile as checked, ending the game if it is a bomb.

		Args:
			position_x (int): Position of the tile on the x axis. Higher values
				go right.
				
			position_y (int): Position of the title on the y axis. Higher values
				go down.
		"""
		self.checked_tiles.append((position_x, position_y))

		if self.is_bomb(position_x, position_y):
			self.end_game()

	def get_tile_state(self, position_x: int, position_y: int) -> string:
		"""
		Get the state of a tile for the purpose of displaying on screen.

		Returns: 
			string: One of the following:
			- "checked: i", where i is an int [0-9]
			- "flagged"
			- "hidden"
		"""
		if (position_x, position_y) in self.checked_tiles:
			return "checked: {}".format(
				get_adjacent_tile_counts(position_x, position_y)["bombs"]
			)

		elif (position_x, position_y) in self.flagged_tiles:
			return "flagged"

		else:
			return "hidden"

	def is_bomb(self, position_x: int, position_y: int):
		"""
		Check if given tile is a bomb.

		Generates a random number from 0-1 using the seed mixed with the tile's
		positions. This is then compared with the bomb chance, and, if the chance
		is higher, the tile is a bomb.

		Args:
			position_x (int): Position of the tile on the x axis. Higher values
				go right.
				
			position_y (int): Position of the title on the y axis. Higher values
				go down.

		Return
			bool: True if given tile is a bomb, False otherwise.
		"""
		random.seed(self.seed + position_x + position_y)

		roll = random.randint(1, 100)
		return self.bomb_chance >= roll

	def get_adjacent_tile_counts(self, position_x: int, position_y: int):
		"""
		Get the counts of the eight adjacent tiles to the tile specified.

		Counts retrieved are: number of flags and number of bombs in adjacent tiles.

		Args:
			position_x (int): Position of the tile on the x axis. Higher values
				go right.

			position_y (int): Position of the tile on the y axis. Higher values
				go down.

		Returns:
			dict: The keys (strings) are "bombs" and "flags" and the values (ints)
				are the counts of each.
		"""
		count_bombs = 0
		count_flags = 0

		for i in range(-1, 2): # Range end is exclusive.
			for v in range(-1, 2):
				# TODO: verify this works correctly.
				if i == 0 and v == 0:
					continue

				if is_bomb(position_x + i, position_y + v):	
					count_bombs += 1

				if (position_x + i, position_y + v) in self.flagged_tiles:
					count_flags += 1

		return {"bombs": count_bombs, "flags": count_flags}

	def end_game(self):
		"""
		End the game as a result of revealing a bomb.
		"""
		pass
					
