from bakara.deck import Deck
from bakara.player import Player 
from bakara.banker import Banker 

def main(is_debug):
	# カードとプレイヤー、バンカーを用意する
	deck = Deck()
	deck.shuffle()

	if is_debug:
		print("deck info:", len(deck.deck))
		print("")

	player = Player()
	banker = Banker()

	# 1st round
	player.first_action(deck)
	banker.first_action(deck)

	if is_debug:
		print("@@@ 1st round @@@")
		print("=== Player ===")
		out = list()
		for c in player.have_cards:
			out.append([c.get_mark(), c.get_number()])
		print(out)
		print("player score:", player._get_score())
		print("*** Banker ***")
		out = list()
		for c in banker.have_cards:
			out.append([c.get_mark(), c.get_number()])
		print(out)
		print("banker score:", banker._get_score())
		print("deck info:", len(deck.deck))
		print("")

	# 2nd round
	player.second_action(deck)
	banker.second_action(deck, player=player)

	if is_debug:
		print("@@@ 2nd round @@@")
		print("=== Player ===")
		out = list()
		for c in player.have_cards:
			out.append([c.get_mark(), c.get_number()])
		print(out)
		print("player score:", player._get_score())
		print("*** Banker ***")
		out = list()
		for c in banker.have_cards:
			out.append([c.get_mark(), c.get_number()])
		print(out)
		print("banker score:", banker._get_score())
		print("deck info:", len(deck.deck))



if __name__ == "__main__":
	main(is_debug=True)