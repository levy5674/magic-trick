from itertools import product
from sys import stdin

VALUES = '23456789JQKA'

SUITS = 'CDHS'

CARDS = [value + suit for (value, suit) in product(VALUES, SUITS)]

INVERSE_CARDS = {card: index for (index, card) in enumerate(CARDS)}

ORDERS = [None, (0, 1, 2), (0, 2, 1),
         (1, 0, 2), (1, 2, 0),
         (2, 0, 1), (2, 1, 0)]

INVERSE_ORDER = { order: j for j, order in enumerate(ORDERS) if order}

def encode(cards):
    if len(cards) != 5:
        raise Exception("cards must be a list of 5 cards")
    card_set = set(cards)
    suit_values = {suit: [] for suit in SUITS}
    for (value, suit) in cards:
        suit_values[suit].append(value)
    suit, values = next(_ for _ in suit_values.items() if len(_[1]) > 1)
    i0, i1 = [VALUES.index(v) for v in values[:2]]
    if ((i1 - i0) % 13) > 6:
        i0, i1 = i1, i0
    hidden = VALUES[i1] + suit
    encoding = [VALUES[i0] + suit]
    card_set = card_set.difference(encoding + [hidden])
    sorted_cards = sorted(card_set)
    encoding += [sorted_cards[j] for j in ORDERS[(i1 - i0) % 13]]
    return (hidden, encoding)

def decode(cards):
    if len(cards) != 4:
        raise Exception("cards must be a list of 4 cards")
    suit = cards[0][1]
    i_base = VALUES.index(cards[0][0])
    with_index = zip(cards[1:], range(3))
    rank = [r for card, r in sorted(with_index)]
    arg_sort = tuple([index for r, index in sorted(zip(rank, range(3)))])
    offset = INVERSE_ORDER[arg_sort]
    i_hidden = (i_base + offset) % 13
    return VALUES[i_hidden] + suit

if __name__ == '__main__':
    # example = ['5H', '7D', '3C', 'JS', '5D']
    cards = stdin.readline().strip().split(' ')
    hidden, encoding = encode(cards)
    print("*** Encoding ***")
    print('hiding: ' + hidden)
    print("encoding: " + ' '.join(encoding))
    decoded = decode(encoding)
    print("*** Decoding ***")
    print("input: " + ' '.join(encoding))
    print(decoded)


# print('\n'.join(CARDS))
