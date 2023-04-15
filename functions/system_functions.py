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
        if type(name[-2]) == int:
            genre = int(name[-2]) + int(name[-1])
        else:
            genre = int(name[-1])
        card = name + '.png'
        cost = v.drop_info[rarity]['cost']
        if rarity == "common" or rarity == "uncommon":
            for i in range(genre):
                cost -= 1
        elif rarity == "rare":
            for i in range(genre):
                cost -= 2
        elif rarity == "epic" or rarity == "mythic":
            for i in range(genre):
                cost -= 5
        elif rarity == "legendary" or rarity == "secret":
            for i in range(genre):
                cost -= 15
        return card, cost, name