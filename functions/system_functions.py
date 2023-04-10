import random
from random import choice

from CuCardBot.functions import variables as v


def choose_card_for_drop(rarity):
    if rarity == 'coins':
        return random.choices(
            list(v.drop_info[rarity]['coins'].keys()),
            weights=list(v.drop_info[rarity]['coins'].values()),
            k=1)[0]
    else:
        name = choice(v.drop_info[rarity]['cards'])
        genre = int(name[-1])
        card = name + '.png'
        cost = v.drop_info[rarity]['cost']
        for i in range(genre):
            cost -= 1
        return card, cost, name
