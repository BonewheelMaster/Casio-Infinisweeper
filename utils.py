def clamp(value, minimum, maximum):
	"""
	Clamp a value between a minimum and maximum value.

	Args:
		value: Value to be clamped.
		minimum: Minimum value allowed.
		maximum: Maximum value allowed.
	"""
	return sorted( (minimum, value, maximum) )[1]

def mix_seed_with_tile(seed: int, position_x: int, position_y: int) -> int:
	"""
	Given a seed and a tile's positions, generate a new, unique seed.

	Args:
		seed (int): The seed before mixing.
		position_x (int): The position of the tile on the x-axis.
		position_y (int): The position of the tile on the y-axis.

	Returns:
		int: The new mixed seed.
	"""
	
	seed_str = str(seed) + str(position_x) + str(position_y)
	
	return hash(seed_str)
	
