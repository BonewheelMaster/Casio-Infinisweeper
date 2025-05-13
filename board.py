"""
The entire worldspace.

The only data that are stored are the tiles that have been flagged
and the tiles that have been revealed. All other data (whether a
tile is a bomb, how many bombs are around a tile, etc.) are reproducibly
calculated via the seed.

Attributes:
"""
import random
import config

SEED = config.SEED
BOMB_CHANCE = config.BOMB_CHANCE 

checked_tiles = set()
flagged_tiles = set()

debug_revealed = False # !debug

def get_tile_state(position_x: int, position_y: int) -> str:
	"""
	Get the state of a tile for the purpose of displaying on screen.

	Returns: 
		string: One of the following:
			- "checked: i", where i is an int [0-9]
			- "flagged"
			- "hidden"
	"""
	if (position_x, position_y) in checked_tiles or debug_revealed: # !debug
		if is_bomb(position_x, position_y):
			return "bomb"
			
		return "checked: {}".format(
			get_adjacent_tile_counts(position_x, position_y)["bombs"]
		)

	elif (position_x, position_y) in flagged_tiles:
		return "flagged"

	else:
		return "hidden"


def flag_tile(position_x: int, position_y: int) -> None:
	"""
	Flag or unflag a tile. Revealed tiles cannot be flagged.

	Args:
		position_x (int): Position of the tile on the x axis. Higher values
			go right.
			
		position_y (int): Position of the title on the y axis. Higher values
			go down.
	
	Side effects:
		Reads:
			- checked_tiles
			_ flagged_tiles

		Modifies:
			- flagged_tiles
	"""
	if (position_x, position_y) not in checked_tiles:
		if (position_x, position_y) not in flagged_tiles:
			flagged_tiles.add( (position_x, position_y) )

		else:
			flagged_tiles.discard( (position_x, position_y) )


def check_tile(position_x: int, position_y: int) -> None:
	"""
	Set tile as checked, ending the game if it is a bomb.

	Args:
		position_x (int): Position of the tile on the x axis. Higher values
			go right.
			
		position_y (int): Position of the title on the y axis. Higher values
			go down.

	Side effects:
		Reads:
			- flagged_tiles

		Modifies:
			- checked_tiles
	"""
	if (position_x, position_y) not in flagged_tiles:
		checked_tiles.add( (position_x, position_y) )

	if is_bomb(position_x, position_y):
		end_game()


def is_bomb(position_x: int, position_y: int) -> bool:
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
	random.seed( SEED + hash( (position_x, position_y) ) )

	roll = random.randint(1, 100)
	return BOMB_CHANCE >= roll


def get_adjacent_tile_counts(position_x: int, position_y: int) -> dict:
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

			if (position_x + i, position_y + v) in flagged_tiles:
				count_flags += 1

	return {"bombs": count_bombs, "flags": count_flags}


def end_game() -> None:
	"""
	End the game as a result of revealing a bomb.
	"""
	pass
				
