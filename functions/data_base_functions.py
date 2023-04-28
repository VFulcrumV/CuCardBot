import sqlite3
import disnake
import os
from CuCardBot.functions import variables as v
connection = sqlite3.connect('server.db')


def create_start_database(self):
    # self.cursor.execute("""DROP TABLE users""")
    self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    name TEXT,
                    id INT,
                    cash BIGINT,
                    mem_cards INT,
                    mem_opened INT,
                    common INT,
                    uncommon INT,
                    rare INT,
                    epic INT,
                    mythic INT,
                    legendary INT,
                    secret INT,
                    craftable INT,
                    bucky_o_hare_1 INT,
                    dune2000_1 INT,
                    metroid_1 INT,
                    prince_of_persia_1 INT,
                    tempest_1 INT,
                    contra_1 INT,
                    defender_1 INT,
                    elite_1 INT,
                    maniac_mansion_1 INT,
                    pitfall_1 INT,
                    street_fighter_1 INT,
                    tekken_1 INT,
                    donkey_kong_1 INT,
                    mega_man2_1 INT,
                    zero_tolerance_1 INT,
                    pac_man_1 INT,
                    the_legend_of_zelda_1 INT,
                    mortal_kombat_1 INT,
                    super_mario_bros_1 INT,
                    battle_city_1 INT,
                    aaron_2 INT,
                    froggit_2 INT,
                    ice_cap_2 INT,
                    loox_2 INT,
                    migosp_2 INT,
                    moldsmal_2 INT,
                    snowdrake_2 INT,
                    tsunderplane_2 INT,
                    parsnik_2 INT,
                    vegetoid_2 INT,
                    vulkin_2 INT,
                    whimsun_2 INT,
                    woshua_2 INT,
                    astigmatism_2 INT,
                    final_froggit_2 INT,
                    frisk_2 INT,
                    gyftrot_2 INT,
                    knight_knight_2 INT,
                    migospel_2 INT,
                    moldbygg_2 INT,
                    moldessa_2 INT,
                    pyrope_2 INT,
                    whimsalot_2 INT,
                    dogamy_and_dogaressa_2 INT,
                    doggo_2 INT,
                    dummy_2 INT,
                    glyde_2 INT,
                    mad_dummy_2 INT,
                    madjick_2 INT,
                    shyren_2 INT,
                    so_sorry_2 INT,
                    greater_dog_2 INT,
                    jerry_2 INT,
                    lesser_dog_2 INT,
                    mettaton_2 INT,
                    muffet_2 INT,
                    napstablook_2 INT,
                    toriel_2 INT,
                    undyne_2 INT,
                    alphys_2 INT,
                    asgore_2 INT,
                    flowey_2 INT,
                    mad_mew_mew_2 INT,
                    mettaton_ex_2 INT,
                    papyrus_2 INT,
                    sans_2 INT,
                    temmie_2 INT,
                    undine_the_undying_2 INT,
                    asriel_dreemurr_2 INT,
                    bad_time_sans_2 INT,
                    chara_dreemurr INT,
                    frisk INT,
                    mad_mew_mew INT,
                    mettaton_neo INT,
                    gaster_2 INT,
                    zhenya_3 INT,
                    pioner_3 INT,
                    genda_3 INT,
                    yliana_3 INT,
                    viola_3 INT,
                    olga_dmitrievna_3 INT,
                    samanta_3 INT,
                    shurik_3 INT,
                    electronik_3 INT,
                    slavya_3 INT,
                    lena_3 INT,
                    miku_3 INT,
                    ulia_3 INT,
                    alice_3 INT,
                    ikuno_4 INT,
                    futoshi_4 INT,
                    nana_4 INT,
                    bim_5 INT,
                    fox_devil_5 INT,
                    garugari_5 INT,
                    katana_man_5 INT,
                    nyako_5 INT,
                    reze_5 INT,
                    tomato_devil_5 INT,
                    mitsuru_4 INT,
                    goro_4 INT,
                    kishibe_5 INT,
                    kwanshi_5 INT,
                    tendo_michiko_5 INT,
                    hero_4 INT,
                    zorome_4 INT,
                    angel_5 INT,
                    nayuta_5 INT,
                    kokoro_4 INT,
                    miku_4 INT,
                    himeno_5 INT,
                    kobeni_5 INT,
                    pochita_5 INT,
                    zero_zero_one_4 INT,
                    ichigo_4 INT,
                    denji_5 INT,
                    hayakawa_aki_5 INT,
                    power_5, INT,
                    zero_two_4 INT,
                    makima_5 INT,
                    chainsaw_man_5 INT
                );""")
    for guild in self.bot.guilds:
        for member in guild.members:
            add_new_member(self, member)
    self.connection.commit()


def add_new_member(self, member):
    if self.cursor.execute(f"SELECT id FROM users WHERE id = ?", (member.id, )).fetchone() is None:
        self.cursor.execute(f"INSERT INTO users VALUES (?, ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "
                            "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "
                            "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "
                            "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "
                            "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "
                            "0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "
                            "0, 0, 0, 0, 0)",
                            (str(member), member.id))
        self.connection.commit()


def see_card(self, card, author):
    author = str(author)
    full_name = card + ".png"
    for i in list(v.drop_info.keys()):
        if os.path.exists(f"./cards/{i}/{full_name}"):
            have_card = self.cursor.execute(f"""SELECT {card} from users WHERE id = {author}""").fetchall()
            if have_card[0][0] > 0:
                a = f"./cards/{i}/{full_name}"
                return a

    return "no"


def sell_card(self):
    give_take_money(self, self.cost, self.author, '+')
    self.cursor.execute("UPDATE users SET mem_opened = mem_opened + {} WHERE id = {}".format(1, self.author))
    self.connection.commit()


def take_card(self):
    self.cursor.execute(f"UPDATE users SET {self.name} = {self.name} + {1} WHERE id = {self.author}")
    self.cursor.execute(f"UPDATE users SET {self.rarity} = {self.rarity} + {1} WHERE id = {self.author}")
    self.connection.commit()


def give_take_money(self, amount, user_id, operand):
    self.cursor.execute("UPDATE users SET cash = cash {} {} WHERE id = {}".format(operand, int(amount), user_id))
    self.connection.commit()


def number_of_cards_in_inv(self):
    num_of_cards = self.cursor.execute(f'SELECT {self.name} FROM users WHERE id = {self.author}').fetchone()[0]
    return num_of_cards


def member_money(self):
    money = self.cursor.execute(f'SELECT cash FROM users WHERE id = {self.author}').fetchone()[0]
    return money


def take_away_card(self, author, card, num):
    self.cursor.execute(f"UPDATE users SET {self.name} = {self.name} - {num} WHERE id = {author}")
    self.connection.commit()