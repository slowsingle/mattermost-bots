from blackjack.person import Person
from blackjack.util import calc_score


class Player(Person):
    def __init__(self):
        super().__init__()

    def get_score(self):
        return calc_score(self.have_cards)

    def first_action(self, deck):
        # カードを2枚引く
        self.pull_cards(deck, n_pulls=2)
        return self.get_score()

    def hit(self, deck):
        self.pull_cards(deck, n_pulls=1)
        return self.get_score()

