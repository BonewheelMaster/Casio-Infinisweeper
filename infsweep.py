import casioplot as p


def main() -> None:
	p.show_screen()
	# Note: A character is 3x5px (HxV). This becomes 5x7px with a 1 px border. 
	# However, the border is not present on the edges, as it is unnecessary. 
	# This means that the screen resolution (128x64px) can be considered 130x66px.
	for i in range(11):
		for v in range(26):
			p.draw_string(v*5, i*6, "2", )


main()