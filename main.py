class board:
	def __init__(self):
		# three rings, 8 places each
		self.places = [[' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ']]
	def display(self):
		text = ''
		text += f'{self.places[0][0]} - - {self.places[0][1]} - - {self.places[0][2]}\n'
		text += f'| {self.places[1][0]} - {self.places[1][1]} - {self.places[1][2]} |\n'
		text += f'| | {self.places[2][0]} {self.places[2][1]} {self.places[2][2]} | |\n'
		# needs like 5 more lines
		return text


class piece:
	def __init__(self):
		pass

b = board()
print(b.display())