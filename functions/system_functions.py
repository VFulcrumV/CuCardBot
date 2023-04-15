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
        if rarity == "common" or "uncommon":
            for i in range(genre):
                cost -= 1
        elif rarity == "rare":
            for i in range(genre):
                cost -= 2
        elif rarity == "epic" or "mythic":
            for i in range(genre):
                cost -= 5
        elif rarity == "legendary" or "secret":
            for i in range(genre):
                cost -= 10
        return card, cost, name