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
	
	def turn(self, move: Move):
		"""Handles the logic for 1 turn. Does not check whos turn it is"""
		if move.is_valid():
			move.apply(self.places)
			if self.mill_formed(move.new_ring, move.new_notch):
				self.do_mill_stuff()

	def mill_formed(self, ring: int, notch: int) -> bool: # changed to "mill_formed" for conciseness, can change back if preferred
		# if notch even
		if notch % 2 == 0:
			# check along both edges of that ring if there's three
			# i split the if statement over 2 lines
			if self.places[ring][(notch-1)%8] == self.places[ring][notch] \
		   and self.places[ring][(notch+1)%8] == self.places[ring][notch]:
				return True
		# else notch odd
		else:
			# check along edge of ring
			if self.places[ring][(notch-1)%8] == self.places[ring][notch] \
		   and self.places[ring][(notch+1)%8] == self.places[ring][notch]:
				return True
			
			# check along lines that connect rings
			if self.places[(ring+1)%3][(notch)] == self.places[ring][notch] \
		   and self.places[(ring-1)%3][(notch)] == self.places[ring][notch]:
				return True

		# No conditions were met -> return False
		return False

	def do_mill_stuff():
		"""Does mill stuff"""
		pass

	'''		
	def add(self, ring: int, notch: int, player: int) -> None: 
		"""Updates the value of places[ring][notch] to the value `player`"""
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
	'''

# I'm adding a bunch of OOP stuff because hehe
class Player:
	def __init__(self, token: int):
		self.token = token
		# "token" just refers to the arbitrary number for the player
		self.men_unplayed = 9
		self.men_in_play = 0
		self.men_locations = []

class Move:
	"""Superclass for the particular move classes.\
 Not intended for direct use"""
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
		self.player.men_locations.append([self.new_ring, self.new_notch])

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

def convert_to_move(text_input: str, player: Player) -> Move:
	"""Parses a text (string) input into a move."""

	text_input = text_input.split()
	if len(text_input) > 2:
		raise ValueError(f"Expected maximum of two position arguments,\
				    {len(text_input)} were given: {text_input}")
	
	for index, word in enumerate(text_input):
		if len(word) not in (2, 3):
			raise ValueError(f"Expected each argument to be 2 or 3 characters \
long: {word} was given at index {index}, which is of length {len(word)}")
		
		if not word[0].isalpha():
			raise ValueError("Expected first character to be a letter. \
{word[0]} was recieved.")
		
		word = word.upper().split(",")
		text_input[index] = word

		if word[0] not in ("A", "B", "C"):
			raise ValueError("Expected first character to be either \
A, B, or C. {word[0]} was recieved")

		if not word[1].isdigit():
			raise ValueError("Expected second character to be a digit.\
{word[1]} was recieved.")
		if word[1] < 0 or word[1] > 7:
			raise ValueError(f"Expected second digit to be in range 0:7 \
inclusive. Value of {word[0]} was recieved.")

	if len(text_input) == 1:
		return Place(player, ord(text_input[0][0]) -65, text_input[0][1])
	
	elif player.men_in_play > 3:
		return Shift(player, ord(text_input[1][0]) -65, text_input[1][1],
			   				 ord(text_input[0][0]) -65, text_input[0][1])
	else:
		return Relocate(player, ord(text_input[1][0]) -65, text_input[1][1],
			   					ord(text_input[0][0]) -65, text_input[0][1])



b = Board()
print(str(b))