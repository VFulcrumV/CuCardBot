work_income = [
  1, 2, 3, 4, 5, 0, 1, 1, 2, 3,
]

common_cards = ["bucky_o_hare_1", "dune2000_1", "metroid_1", "prince_of_persia_1", "tempest_1"]

uncommon_cards = ["contra_1", "defender_1", "elite_1", "maniac_mansion_1"]

rare_cards = ["pitfall_1", "street_fighter_1", "tekken_1"]

epic_cards = ["donkey_kong_1", "mega_man2_1", "zero_tolerance_1"]

mythic_cards = ["pac_man_1", "the_legend_of_zelda_1"]

legendary_cards = ["mortal_kombat_1", "super_mario_bros_1"]

secret_cards = ["battle_city_1"]

all_cards = common_cards + uncommon_cards + rare_cards + epic_cards + mythic_cards + legendary_cards + secret_cards

time_limits_per_drop = {}

drop_info = {
    'common': {
        'drop_chance': 50,
        'cost': 25,
        'cards': common_cards},
    'uncommon': {
        'drop_chance': 19,
        'cost': 55,
        'cards': uncommon_cards},
    'rare': {
        'drop_chance': 12,
        'cost': 80,
        'cards': rare_cards},
    'epic': {
        'drop_chance': 6,
        'cost': 170,
        'cards': epic_cards},
    'mythic': {
        'drop_chance': 2.5,
        'cost': 270,
        'cards': mythic_cards},
    'legendary': {
        'drop_chance': 0.7,
        'cost': 600,
        'cards': legendary_cards},
    'secret': {
        'drop_chance': 0.3,
        'cost': 1300,
        'cards': secret_cards},
    'coins': {
        'drop_chance': 9.5,
        'coins': {
            80: 0.316,
            125: 0.242,
            200: 0.179,
            260: 0.158,
            404: 0.105
        }
    }
}