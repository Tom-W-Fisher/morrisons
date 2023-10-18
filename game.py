from __future__ import annotations
class Board:
	def __init__(self):
		# three rings, 8 places each
		self.places = [	[0,0,0,0,0,0,0,0],
				 		[0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0]]

		self.players = [Player(1), Player(2)]
		self.current_player = 0
		

#	def playerconfig(self, player1='r', player2='b'):
#		self.players = [player1,player2]

	def __str__(self):
		return """\
{} - - {} - - {}
| {} - {} - {} |
| | {} {} {} | |
{} {} {}   {} {} {}
| | {} {} {} | |
| {} - {} - {} |
{} - - {} - - {}
 """.format(self.places[0][0], self.places[0][1], self.places[0][2],
			self.places[1][0], self.places[1][1], self.places[1][2],
			self.places[2][0], self.places[2][1], self.places[2][2], 
			self.places[0][7], self.places[1][7], self.places[2][7], self.places[0][3], self.places[1][3], self.places[2][3],
			self.places[2][6], self.places[2][5], self.places[2][4], 
			self.places[1][6], self.places[1][5], self.places[1][4],
			self.places[0][6], self.places[0][5], self.places[0][4])
	
	def place(self, ring: int, notch: int, player: int) -> None:
		"""Assigns the value `player` to the designated place"""
		self.places[ring][notch] = player
	
	def move(self, old_ring: int, old_notch: int, new_ring: int, new_notch: int) -> bool:
		"""Checks if the move is valid, then moves piece from old position to new position.
Returns a True/False depending on whether the move was successful"""
		if not self.check_valid_move(old_ring, old_notch, new_ring, new_notch):
			return False
		
		player = self.places[old_ring][old_notch]
		self.places[old_ring][old_notch] = 0
		self.places[new_ring][new_notch] = player
		return True
	
	def check_valid_move(self, old_ring, old_notch, new_ring, new_notch):
		# check on board
		if not(new_ring in [0,1,2] and new_notch in [0,1,2,3,4,5,6,7]):
			return False
		# check is empt
		if self.places[new_ring][new_notch] != 0:
			return False
		# checks for same ring
		if new_ring == old_ring:
			if new_notch != (old_notch+1)%8 and new_notch != (old_notch-1)%8:
				return False
		# checks for changing ring
		if old_notch%2 == 1 and old_notch == new_notch:
			if new_ring != old_ring+1 and new_ring != old_ring-1:
				return False
		return True
	
	def turn(self, move: Move):
		"""Handles the logic for 1 turn. Does not check whos turn it is"""
		if move.is_valid():
			move.apply(self.places)
			if self.forms_mill(move.new_ring, move.new_notch):
				self.do_mill_stuff()

	def forms_mill(self, ring: int, notch: int) -> bool:
		"""Checks if the piece at the given position is part of a mill"""
		pass

	def do_mill_stuff():
		"""Does mill stuff"""
		pass
	

# I'm adding a bunch of OOP stuff because hehe
class Player:
	def __init__(self, token: int):
		self.token = token
		self.men_unplayed = 9
		self.men_in_play = 0
		self.locations = []

class Move:
	"""Superclass for the particular move classes"""
	def __init__(self, player: Player, new_ring, new_notch):
		self.player = player
		self.new_ring = new_ring
		self.new_notch = new_notch

	def is_valid(self, places: list[list[int]]) -> bool:
		"""Checks that the new place is in range and is unoccupied, given the\
current board state."""
		if self.new_ring > 2 or self.new_ring < 0 \
		or self.new_notch > 7 or self.new_notch < 0:
			return False
		
		if places[self.new_ring][self.new_notch] != 0:
			return False
		
		return True
	
	def apply(self, places: list[list[int]]):
		places[self.new_ring][self.new_notch] = self.player.token

class Place(Move):
	"""Describes a move type where a piece is placed on to the board"""
	def is_valid(self, places: list[list[int]]) -> bool:
		if not super().is_valid(places):
			return False
		
		if self.player.men_unplayed < 1:
			return False
		
		return True
	
	def apply(self, places):
		super().apply(places)
		self.player.men_unplayed -= 1

class Shift(Move):
	"""Describes a move where a piece is moved from one space to an \
adjacent space"""
	def __init__(self, player, new_ring, new_notch, old_ring, old_notch):
		super().__init__(self, player, new_ring, new_notch)
		self.old_ring = old_ring
		self.old_notch = old_notch

	# TODO
	def is_valid(self, places: list[list[int]], current_player: Player) -> bool:
		pass

class Relocate(Move):
	"""Describes a move type where a piece is moved from one space to any\
 other space"""
	def __init__(self, player, new_ring, new_notch, old_ring, old_notch):
		super().__init__(self, player, new_ring, new_notch)
		self.old_ring = old_ring
		self.old_notch = old_notch





b = Board()
print(str(b))