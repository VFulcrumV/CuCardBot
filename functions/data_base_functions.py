import sqlite3
import os
from CuCardBot.functions import variables as v
connection = sqlite3.connect('server.db')


def create_start_database(self):
    self.cursor.execute(v.bd_table_create)
    for guild in self.bot.guilds:
        for member in guild.members:
            add_new_member(self, member)
    self.connection.commit()


def add_new_member(self, member):
    a = [0 for i in range(len(v.bd_params + v.all_cards))]
    striiing = str(tuple(a))[1:-1]
    request = f'INSERT INTO users VALUES (?, ?, 0, {striiing})'
    if self.cursor.execute(f"SELECT id FROM users WHERE id = ?", (member.id,)).fetchone() is None:
        self.cursor.execute(request, (str(member), member.id))


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
