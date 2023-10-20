from __future__ import annotations
class Board:
	"""Stores the state of the board and has a few methods for interacting \
with it. \n
Attributes:
- `places` \n
	A 2d 3 by 8 list of integers representing the state of the board. Outer \
	index refers to ring, inner index refers to "notch", the position on the \
	ring.
- `players` \n
	A list of length 2 containing two `Player` objects
- `_current_player` \n
	An integer storing the index of the current player in `players`.
	This is not meant to be read from externally. Use method
	`get_current_player` to get the token of the current player.
"""
	def __init__(self, player_1_token: int, player_2_token: int):
		# three rings, 8 places each
		self.places = [	[0,0,0,0,0,0,0,0],
				 		[0,0,0,0,0,0,0,0],
						[0,0,0,0,0,0,0,0]]

		self.players = [Player(player_1_token), Player(player_2_token)]
		self._current_player: int = 0
		
	def get_current_player(self) -> int:
		"""Returns the token of the current player"""
		return self._get_current_player_object().token

	def _get_current_player_object(self) -> Player:
		"""Returns the player whos turn it is"""
		return self.players[self._current_player]
	
	def _get_other_player_object(self) -> Player:
		"""Returns the player whos turn it isn't"""
		return self.players[(self._current_player + 1) % 2]

	def change_current_player(self):
		"""Changes to current player to the other player"""
		self._current_player = (self._current_player + 1) % 2

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
	
	def take_turn(self, player_input: str):
		"""Handles the logic for 1 turn. Does not check whos turn it is."""
		move = convert_to_move(player_input,
						  self._get_current_player_object(),
						  self)
		move.apply(self.places)
		if self.mill_formed(move.new_ring, move.new_notch):
			move.player.mill_turn = True
		else:
			self.change_current_player()

	def mill_formed(self, ring: int, notch: int) -> bool:
		"""Checks if the place specified by the given ring and notch is a \
			part of a mill."""
		# if notch even
		if notch % 2 == 0:
			# check along both edges of that ring if there's three
			if self.places[ring][(notch-1)%8] == self.places[ring][notch] \
		   and self.places[ring][(notch-2)%8] == self.places[ring][notch] \
		   or (self.places[ring][(notch+1)%8] == self.places[ring][notch] \
		   and self.places[ring][(notch+2)%8] == self.places[ring][notch]):
				return True
		# else notch odd
		else:
			# check along edge of ring
			if self.places[ring][(notch-1)%8] == self.places[ring][notch] \
		   and self.places[ring][(notch+1)%8] == self.places[ring][notch]:
				return True
			
			# check along lines that connect rings
			elif self.places[(ring+1)%3][(notch)] == self.places[ring][notch] \
		     and self.places[(ring-1)%3][(notch)] == self.places[ring][notch]:
				return True

		# No conditions were met -> return False
		return False

class Player:
	"""Stores some information about a player"""
	def __init__(self, token: int):
		"""`token` is the number that will be \
		used to represent the player's pieces when the board is converted to \
		a string."""
		self.token = token
		# "token" just refers to the arbitrary number for the player
		self.men_unplayed = 9
		self.men_locations = []
		self.mill_turn = False

	@property
	def men_in_play(self) -> int:
		return len(self.men_locations)

class Move:
	"""Superclass for the particular move classes.\
 Not intended for direct use."""
	def __init__(self, player: Player, new_ring, new_notch):
		self.player = player
		self.new_ring = new_ring
		self.new_notch = new_notch

	def _check_validity(self, places: list[list[int]]):
		"""Checks that the new place is in range and is unoccupied, given the\
current board state."""
		# No need to check if indexes in range because that is already handled
		if places[self.new_ring][self.new_notch] != 0:
			raise ValueError("Destination place needs to be empty.")
	
	def apply(self, places: list[list[int]]):
		self._check_validity()
		places[self.new_ring][self.new_notch] = self.player.token
		self.player.men_locations.append([self.new_ring, self.new_notch])

class Remove(Move):
	def __init__(self, player: Player, new_ring, new_notch, board: Board):
		super().__init__()
		self.affected_player = board._get_other_player_object()
		self.board = board

	def _check_validity(self, places: list[list[int]]):
		if places[self.new_ring][self.new_notch] != self.affected_player.token:
			raise ValueError("Target place needs to be occupied by enemy man")
		
		all_mills = True
		for man_location in self.affected_player.men_locations:
			if not self.board.mill_formed(man_location[0], man_location[1]):
				all_mills = False

		if not all_mills:
			if self.board.mill_formed(self.new_ring, self.new_notch):
				raise ValueError("Can only remove enemy men from mills if \
all enemy men are in mills.")
			
	def apply(self, places: list[list[int]]):
		self._check_validity()
		places[self.new_ring][self.new_notch] = 0
		self.affected_player.men_locations.remove(
											[self.new_ring, self.new_notch])

class Place(Move):
	"""Describes a move type where a piece is placed on to the board"""
	def _check_validity(self, places: list[list[int]]):
		super()._check_validity()
	
	def apply(self, places):
		super().apply(places)
		self.player.men_unplayed -= 1

class Relocate(Move):
	"""Describes a move type where a piece is moved from one space to any\
 other space"""
	def __init__(self, player, new_ring, new_notch, old_ring, old_notch):
		super().__init__(self, player, new_ring, new_notch)
		self.old_ring = old_ring
		self.old_notch = old_notch

	def _check_validity(self, places: list[list[int]], current_player: Player):
		super()._check_validity()
		# `convert_to_move` only creates a `Relocate` object if the player has 3 men
		# so checking number of men is not required
		# which allows `Shift` to inherit without creating problems

	def apply(self, places):
		super().apply()
		places[self.old_ring][self.old_notch] = 0

		self.player.men_locations.append(([self.new_ring][self.new_notch]))
		self.player.men_locations.remove(([self.old_ring][self.old_notch]))

class Shift(Relocate):
	"""Describes a move where a piece is moved from one space to an \
adjacent space"""
	def __init__(self, player, new_ring, new_notch, old_ring, old_notch):
		super().__init__(self, player, new_ring, new_notch)
		self.old_ring = old_ring

	def _check_validity(self, places: list[list[int]], current_player: Player):
		super()._check_validity()


	def apply(self, places):
		return super().apply(places)


def convert_to_move(text_input: str, player: Player, board: Board) -> Move:
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
		if not player.mill_turn:
			return Place(player, ord(text_input[0][0]) -65, text_input[0][1])
		else:
			return Remove(player, ord(text_input[0][0]) -65, text_input[0][1],
				 board)
	
	elif player.men_in_play > 3:
		return Shift(player, ord(text_input[1][0]) -65, text_input[1][1],
			   				 ord(text_input[0][0]) -65, text_input[0][1])
	else:
		return Relocate(player, ord(text_input[1][0]) -65, text_input[1][1],
			   					ord(text_input[0][0]) -65, text_input[0][1])



b = Board(1, 2)
print(str(b))