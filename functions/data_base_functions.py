import sqlite3

connection = sqlite3.connect('server.db')


def create_start_database(self):
    self.cursor.execute("""DROP TABLE USERS""")
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
                    battle_city_1 INT
                );""")
    for guild in self.bot.guilds:
        for member in guild.members:
            if self.cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                self.cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0"
                                    f"0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                self.connection.commit()
            else:
                pass
    self.connection.commit()


def add_new_member(self, member):
    if self.cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        self.cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
        self.connection.commit()


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