from blackjack.person import Person
from blackjack.util import calc_score

'''
ディーラーはカードの合計が17以上になるまでカードを引かなければならない。
また、17以上になったらそれ以上カードを引くことはできない。
'''
class Dealer(Person):
    def __init__(self):
        super().__init__()

    def get_score(self):
        return calc_score(self.have_cards)

    def get_score_only_first_one(self):
        return calc_score(self.have_cards[:1])

    def first_action(self, deck):
        # カードを2枚引く
        self.pull_cards(deck, n_pulls=2)
        return calc_score(self.have_cards[:1])  # 1枚だけオープンする

    def second_action(self, deck):
        is_finish = False
        while True:
            dealer_score = self.get_score()
            if dealer_score < 17:
                yield dealer_score, is_finish
                self.pull_cards(deck, n_pulls=1)
            else:
                is_finish = True
                break
        yield dealer_score, is_finish

    
if __name__ == "__main__":
    from blackjack.deck import Deck

    deck = Deck()
    deck.shuffle()

    dealer = Dealer()
    dealer.first_action(deck)

    for c in dealer.have_cards:
        print(c.get_mark(), c.get_number())
        
    print(len(deck.deck), dealer.get_score())

    dealer_score = dealer.second_action(deck)
    for c in dealer.have_cards:
        print(c.get_mark(), c.get_number())

    print(len(deck.deck), dealer.get_score())