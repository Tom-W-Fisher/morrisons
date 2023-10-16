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

#	def playerconfig(self, player1='r', player2='b'):
#		self.players = [player1,player2]

	def display(self):
		return f'''{self.places[0][0]} - - {self.places[0][1]} - - {self.places[0][2]}
| {self.places[1][0]} - {self.places[1][1]} - {self.places[1][2]} |
| | {self.places[2][0]} {self.places[2][1]} {self.places[2][2]} | |
{self.places[0][7]} {self.places[1][7]} {self.places[2][7]}   {self.places[0][3]} {self.places[1][3]} {self.places[2][3]}
| | {self.places[2][6]} {self.places[2][5]} {self.places[2][4]} | |
| {self.places[1][6]} - {self.places[1][5]} - {self.places[1][4]} |
{self.places[0][6]} - - {self.places[0][5]} - - {self.places[0][4]}'''
	
	def place(self, ring, notch, player):
		self.places[ring][notch] = player
	
	def move(self, oldring, oldnotch, newring, newnotch):
		player = self.places[oldring][oldnotch]
		self.places[oldring][oldnotch] = 0
		self.places[newring][newnotch] = player


class piece:
	def __init__(self):
		pass

b = Board()
print(b.display())