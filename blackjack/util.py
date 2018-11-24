import itertools

def calc_score(cards):
    # エース（A）が1にも11にもなれることに注意する
    scores_per_card = list()
    for c in cards:
        num = c.get_number()
        if num == 1:
            scores_per_card.append([1, 11])
        elif num >= 10:
            scores_per_card.append([10])
        else:
            scores_per_card.append([num])

    iter_scores = iter(scores_per_card)
    product = list(itertools.product(*iter_scores))

    if len(product) == 1:
        return sum(product[0])
    else:
        best_score = sum(product[0])
        best_value = best_score if best_score <= 21 else -1
        for i in range(1, len(product)):
            score = sum(product[i])
            value = score if score <= 21 else -1
            if best_value < value:
                best_score = score
                best_value = value
        return best_score


def is_blackjack(cards):
    raise NotImplementedError


if __name__ == "__main__":
    from blackjack.card import Card

    cards = [Card(n) for n in [0, 6]]
    best_score = calc_score(cards)
    print(best_score)