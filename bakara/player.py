from bakara.person import Person

class Player(Person):
	def __init__(self):
		super().__init__()

	def _get_score(self):
		sum_score = 0
		for c in self.have_cards:
			num = c.get_number()
			num = 10 if num > 10 else num
			sum_score += num
		return sum_score % 10


	def first_action(self, deck):
		self.pull_cards(deck, n_pulls=2)


	# 3枚目のカードを引くかどうかを決める
	def second_action(self, deck):
		current_score = self._get_score()

		if 0 <= current_score <= 5:
			self.pull_cards(deck, n_pulls=1)
			next_score = self._get_score()
		elif 6 <= current_score <= 9:
			next_score = current_score
		else:
			raise ValueError()

		return next_score

if __name__ == "__main__":
	from bakara.deck import Deck

	deck = Deck()
	deck.shuffle()

	print(len(deck.deck))
	
	player = Player()
	player.first_action(deck)

	for c in player.have_cards:
		print(c.get_mark(), c.get_number())

	print(len(deck.deck), player._get_score())