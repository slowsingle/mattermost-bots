import time
import random
import numpy as np
from blackjack.card import Card

class Deck(object):
	def __init__(self, have_joker=False):
		self.have_joker = have_joker
		if self.have_joker:
			raise NotImplementedError

		self._set_deck()


	def shuffle(self):
		random.shuffle(self.deck)

	def pull_cards(self, n_pulls):
		ret_cards = list()
		for _ in range(n_pulls):
			ret_cards.append(self.deck.pop())

		return ret_cards

	def re_initialize(self):
		self._set_deck()

	def _set_deck(self):
		self.deck = list()
		for i in range(4 * 13):
			self.deck.append(Card(i))


if __name__ == "__main__":
	deck = Deck()
	deck.shuffle()
	cards = deck.pull_cards(n_pulls=5)
	for c in cards:
		print(c.get_mark(), c.get_number())