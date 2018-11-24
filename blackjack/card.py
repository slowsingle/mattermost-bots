# a * 13 + b
# a:マーク, b:数字

n_card_per_mark = 13
marks = ['H', 'D', 'C', 'S']

class Card(object):
	def __init__(self, _id):
		self.id = _id

	def get_mark(self):
		return marks[self.id // n_card_per_mark]

	def get_number(self):
		return self.id % n_card_per_mark + 1


def num2symbol(num):
	if num == 1:
		return 'A'
	elif num == 11:
		return 'J'
	elif num == 12:
		return 'Q'
	elif num == 13:
		return 'K'
	else:
		return str(num)
		

if __name__ == "__main__":
	for i in range(n_card_per_mark * 4):
		card = Card(i)
		print(card.get_mark(), card.get_number())