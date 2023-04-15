
work_income = [
  1, 2, 3, 4, 5, 0, 1, 1, 2, 3,
]

common_cards = ["bucky_o_hare_1", "dune2000_1", "metroid_1", "prince_of_persia_1", "tempest_1", "aaron_2", "froggit_2",
                "ice_cap_2", "loox_2", "migosp_2", "moldsmal_2", "snowdrake_2", "tsunderplane_2", "vegetoid_2",
                "vulkin_2", "whimsun_2", "woshua_2"]


uncommon_cards = ["contra_1", "defender_1", "elite_1", "maniac_mansion_1", "astigmatism_2", "final_froggit_2",
                  "frisk_2", "gyftrot_2", "knight_knight_2", "migospel_2", "moldbygg_2",
                  "moldessa_2", "parsnik_2", "pyrope_2", "whimsalot_2"]

rare_cards = ["pitfall_1", "street_fighter_1", "tekken_1", "dogamy_and_dogaressa_2", "doggo_2", "glyde_2",
              "mad_dummy_2", "madjick_2", "shyren_2", "so_sorry_2"]

epic_cards = ["donkey_kong_1", "mega_man2_1", "zero_tolerance_1", "greater_dog_2", "jerry_2", "lesser_dog_2",
              "mettaton_2", "muffet_2", "napstablook_2", "toriel_2", "undyne_2"]

mythic_cards = ["pac_man_1", "the_legend_of_zelda_1", "alphys_2", "asgore_2", "flowey_2", "mad_mew_mew_2",
                "nettaton_ex_2", "papyrus_2", "sans_2", "temmie_2", "undine_the_undying_2"]

legendary_cards = ["mortal_kombat_1", "super_mario_bros_1", "asriel_dreemurr_2", "bad_time_sans_2"]

secret_cards = ["battle_city_1", "gaster_2"]

craftable_cards = ["chara_dreemurr", "frisk", "mad_mew_mew", "mettaton_neo"]

all_cards = common_cards + uncommon_cards + rare_cards + epic_cards + mythic_cards +\
            legendary_cards + secret_cards + craftable_cards

time_limits_per_drop = {}

drop_info = {
    "craftable": {
        'drop_chance': 0,
        'cost': 500,
        'cards': craftable_cards},
    'common': {
        'drop_chance': 49,
        'cost': 26,
        'cards': common_cards},
    'uncommon': {
        'drop_chance': 20,
        'cost': 56,
        'cards': uncommon_cards},
    'rare': {
        'drop_chance': 12.4,
        'cost': 82,
        'cards': rare_cards},
    'epic': {
        'drop_chance': 7,
        'cost': 175,
        'cards': epic_cards},
    'mythic': {
        'drop_chance': 3.25,
        'cost': 275,
        'cards': mythic_cards},
    'legendary': {
        'drop_chance': 0.9,
        'cost': 610,
        'cards': legendary_cards},
    'secret': {
        'drop_chance': 0.35,
        'cost': 1310,
        'cards': secret_cards},
    'coins': {
        'drop_chance': 7,
        'coins': {
            80: 0.316,
            125: 0.242,
            200: 0.179,
            260: 0.158,
            404: 0.105
        }
    }
}