from bakara.person import Person

class Banker(Person):
	def __init__(self):
		super().__init__()

	def _get_score(self):
		sum_score = 0
		for c in self.have_cards:
			num = c.get_number()
			num = 0 if num >= 10 else num
			sum_score += num
		return sum_score % 10


	def first_action(self, deck):
		self.pull_cards(deck, n_pulls=2)


	# 3枚目のカードを引くかどうかを決める
	# BankerはPlayerの行動によって自身の行動も変わる
	def second_action(self, deck, player):
		if len(player.have_cards) == 2:
			player_pull_more = False
		elif len(player.have_cards) == 3:
			player_pull_more = True
			player_3rd_card = player.have_cards[2]
			_number = player_3rd_card.get_number()
			player_3rd_number = 0 if _number >= 10 else _number
		else:
			raise ValueError()

		current_score = self._get_score()

		if 0 <= current_score <= 2:
			self.pull_cards(deck, n_pulls=1)
			next_score = self._get_score()
		elif current_score == 3:
			if player_pull_more and (player_3rd_number == 8):
				next_score = current_score
			else:
				self.pull_cards(deck, n_pulls=1)
				next_score = self._get_score()
		elif current_score == 4:
			if player_pull_more and (player_3rd_number in [0, 1, 8, 9]):
				next_score = current_score
			else:
				self.pull_cards(deck, n_pulls=1)
				next_score = self._get_score()
		elif current_score == 5:
			if player_pull_more and (player_3rd_number in [4, 5, 6, 7]):
				next_score = current_score
			else:
				self.pull_cards(deck, n_pulls=1)
				next_score = self._get_score()
		elif current_score == 6:
			if player_pull_more and (player_3rd_number in [6, 7]):
				next_score = current_score
			else:
				self.pull_cards(deck, n_pulls=1)
				next_score = self._get_score()
		elif 7 <= current_score <= 9:
			next_score = current_score
		else:
			raise ValueError()

		return next_score

if __name__ == "__main__":
	from bakara.deck import Deck

	deck = Deck()
	deck.shuffle()

	print(len(deck.deck))
	
	banker = Banker()
	banker.first_action(deck)

	for c in banker.have_cards:
		print(c.get_mark(), c.get_number())

	print(len(deck.deck), banker._get_score())