import random
from random import choice
import os.path
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


def crafting_cards(name):
    if name[-2].isdigit() and name[-1].isdigit():
        genre = int(name[-2]) + int(name[-1])
    else:
        genre = int(name[-1])

    rarity = "nothing"
    rarity_after_crafting = ""
    fullname = name + '.png'
    end_card = ""
    variants_of_end_cards = []
    cost = 0

    for i in v.all_rarities:
        if rarity_after_crafting == "":
            if rarity != "nothing":
                rarity_after_crafting = i
            if os.path.exists(f"./cards/{i}/{fullname}"):
                rarity = i
        else:
            pass
    if rarity == "nothing" and rarity_after_crafting == "":
        return ["wrong card"]
    elif rarity == "legendary" or rarity_after_crafting == "secret":
        return ["wrong rarity", rarity]

    if rarity_after_crafting == "uncommon":
        cost = 100
        for i in v.uncommon_cards:
            if i[-2:] == f"_{genre}" or i[-3:] == f"_{genre}":
                variants_of_end_cards.append(i)
    elif rarity_after_crafting == "rare":
        cost = 200
        for i in v.rare_cards:
            if i[-2:] == f"_{genre}" or i[-3:] == f"_{genre}":
                variants_of_end_cards.append(i)
    elif rarity_after_crafting == "epic":
        cost = 400
        for i in v.epic_cards:
            if i[-2:] == f"_{genre}" or i[-3:] == f"_{genre}":
                variants_of_end_cards.append(i)
    elif rarity_after_crafting == "mythic":
        cost = 700
        for i in v.mythic_cards:
            if i[-2:] == f"_{genre}" or i[-3:] == f"_{genre}":
                variants_of_end_cards.append(i)
    else:
        cost = 1800
        for i in v.legendary_cards:
            if i[-2:] == f"_{genre}" or i[-3:] == f"_{genre}":
                variants_of_end_cards.append(i)
    end_card = choice(variants_of_end_cards)
    return [name, end_card, cost, rarity_after_crafting]


