class Person(object):
	def __init__(self):
		self.have_cards = list()

	def pull_cards(self, deck, n_pulls):
		self.have_cards.extend(deck.pull_cards(n_pulls))

	def re_initialize(self):
		self.have_cards = list()


if __name__ == "__main__":
	from bakara.deck import Deck

	deck = Deck()
	deck.shuffle()

	print(len(deck.deck))
	
	person = Person()
	person.pull_cards(deck, n_pulls=5)

	for c in person.have_cards:
		print(c.get_mark(), c.get_number())

	print(len(deck.deck))