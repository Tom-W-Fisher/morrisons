class Board:
	def __init__(self):
		# three rings, 8 places each
		self.places = [	[0,0,0,0,0,0,0,0],
				 		[0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0]]
		# I prefer using ints here, because they are slightly smaller (28 vs 49 bytes)
		# Also prefer to align 2d arrays like that during declaration (unless declaring using inline for loop syntax)
		# i.e.
		# self.places = [[0 for _ in range(8)] for _ in range(3)]

		# I'll going to be bad and say

	def display(self):
		text = (
		f"{self.places[0][0]} - - - {self.places[0][1]} - - - {self.places[0][2]}\n"
		f"| {self.places[1][0]} - - {self.places[1][1]} - - {self.places[1][2]} |\n"
		f"| | {self.places[2][0]} - {self.places[2][1]} - {self.places[2][2]} | |\n"
		)
		# needs like 5 more lines
		return text


class piece:
	def __init__(self):
		pass

b = Board()
print(b.display())