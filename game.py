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

	def __str__(self):
		return f'''{self.places[0][0]} - - {self.places[0][1]} - - {self.places[0][2]}
| {self.places[1][0]} - {self.places[1][1]} - {self.places[1][2]} |
| | {self.places[2][0]} {self.places[2][1]} {self.places[2][2]} | |
{self.places[0][7]} {self.places[1][7]} {self.places[2][7]}   {self.places[0][3]} {self.places[1][3]} {self.places[2][3]}
| | {self.places[2][6]} {self.places[2][5]} {self.places[2][4]} | |
| {self.places[1][6]} - {self.places[1][5]} - {self.places[1][4]} |
{self.places[0][6]} - - {self.places[0][5]} - - {self.places[0][4]}'''
	
	def place(self, ring: int, notch: int, player: int) -> None:
		"""Updates the value of places[ring][notch] to the value `player`"""
		self.places[ring][notch] = player
	
	def move(self, oldring: int, oldnotch: int, newring: int, newnotch: int) -> None:
		"""Checks if the move is valid, then moves piece from old position to new position"""
		player = self.places[oldring][oldnotch]
		self.places[oldring][oldnotch] = 0
		self.places[newring][newnotch] = player
	
	def checkvalidmove(self, oldring, oldnotch, newring, newnotch):
		# check on board
		if not(newring in [0,1,2] and newnotch in [0,1,2,3,4,5,6,7]):
			return False
		# check is empty
		if self.places[newring][newnotch] != 0:
			return False
		# checks for same ring
		if newring == oldring:
			if newnotch != (oldnotch+1)%8 and newnotch != (oldnotch-1)%8:
				return False
		# checks for changing ring
		if oldnotch%2 == 1 and oldnotch == newnotch:
			if newring != oldring+1 and newring != oldring-1:
				return False
		return True

	def check_if_in_mill(self, ring, notch):
		pass
		#if notch even
			# check along both edges of that ring if there's three
		#elif notch odd
			# check along edge of ring but also the line that cuts thru rings

class piece:
	def __init__(self):
		pass

b = Board()
print(b.display())