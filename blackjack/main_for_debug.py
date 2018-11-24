from blackjack.deck import Deck
from blackjack.player import Player 
from blackjack.dealer import Dealer 

def main(is_debug):
    # カードとプレイヤー、ディーラーを用意する
    deck = Deck()
    deck.shuffle()

    if is_debug:
        print("deck info:", len(deck.deck))
        print("")

    player = Player()
    dealer = Dealer()

    # 1st round
    player.first_action(deck)
    dealer.first_action(deck)

    if is_debug:
        print("@@@ 1st round @@@")
        print("=== Player ===")
        out = list()
        for c in player.have_cards:
            out.append([c.get_mark(), c.get_number()])
        print(out)
        print("player score:", player.get_score())
        print("*** Dealer ***")
        out = list()
        for c in dealer.have_cards:
            out.append([c.get_mark(), c.get_number()])
        print(out)
        print("dealer score:", dealer.get_score())
        print("deck info:", len(deck.deck))
        print("")

    # 2nd round
    # プレイヤーはスタンドするか、バーストするまで自分のターンが続く
    while True:
        action = input("(hit or stand?) >> ")

        if action == "hit":
            player.hit(deck)
            if player.get_score() > 21:
                break
            else:
                print("=== Player ===")
                out = list()
                for c in player.have_cards:
                    out.append([c.get_mark(), c.get_number()])
                print(out)
                print("player score:", player.get_score())
        elif action == "stand":
            break
        else:
            print("one more please...")

    # dealer.second_action(deck)

    # if is_debug:
    #     print("@@@ 2nd round @@@")
    #     print("=== Player ===")
    #     out = list()
    #     for c in player.have_cards:
    #         out.append([c.get_mark(), c.get_number()])
    #     print(out)
    #     print("player score:", player.get_score())
    #     print("*** Dealer ***")
    #     out = list()
    #     for c in dealer.have_cards:
    #         out.append([c.get_mark(), c.get_number()])
    #     print(out)
    #     print("dealer score:", dealer.get_score())
    #     print("deck info:", len(deck.deck))



if __name__ == "__main__":
    main(is_debug=True)