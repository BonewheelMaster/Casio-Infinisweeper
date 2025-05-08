class Screen:
	def __init__(self, resolution_x: int, resolution_y: int):
		self.resolution_X = resolution_x
		self.resolution_y = resolution_y

		self.position_x = 0
		self.position_y = 0
		self.cursor_pos_x = 0
		self.cursor_pos_y = 0

	def print_screen(self):
		pass