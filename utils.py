"""Various useful utility functions."""
def clamp(value, minimum, maximum):
	"""
	Clamp a value between a minimum and maximum value.

	All args must be of the same type, though they do not need to be numbers.
	"""
	return sorted( (minimum, value, maximum) )[1]


def mix_seed(seed: int, *args) -> int:
	"""
	Given a seed and some other data, generate a new, unique seed.

	Args:
		seed: The seed before mixing.
		*args: Any amount of data.

	Returns:
		The new mixed seed.
	"""
	
	seed_str = str(seed) + str(args)
	
	return hash(seed_str)
	
