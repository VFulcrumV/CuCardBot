import os
from typing import Optional
import disnake
from disnake.ext import commands
import random
from dateutil import parser
from random import choice
import sqlite3
import datetime


client = commands.Bot(command_prefix='!!', intents=disnake.Intents.all())
client.remove_command("help")

connection = sqlite3.connect('server.db')
cursor = connection.cursor()

work_incom = [
  1, 2, 3, 4, 5, 0, 1, 1, 2, 3,
]

common_cards = ["bucky_o_hare_1", "dune2000_1", "metroid_1", "prince_of_persia_1", "tempest_1"

]
uncommon_cards = ["contra_1", "defender_1", "elite_1", "maniac_mansion_1"

]
rare_cards = ["pitfall_1", "street_fighter_1", "tekken_1"
]
epic_cards = ["donkey_kong_1", "mega_man2_1", "zero_tolerance_1"

]
mythic_cards = ["pac_man_1", "the_legend_of_zelda_1"

]
legendary_cards = [
    "mortal_kombat_1", "super_mario_bros_1"
]
secret_cards = [
    "battle_city_1"
]
all_cards = ["bucky_o_hare_1", "dune2000_1", "metroid_1", "prince_of_persia_1", "tempest_1",
             "contra_1", "defender_1", "elite_1", "maniac_mansion_1", "pitfall_1", "street_fighter_1", "tekken_1",
             "donkey_kong_1", "mega_man2_1", "zero_tolerance_1", "pac_man_1", "the_legend_of_zelda_1",
             "mortal_kombat_1", "super_mario_bros_1", "battle_city_1"]
drop_list = [
    "common", "uncommon", "rare", "epic", "mythic", "legendary", "secret", "80 coins",
    "125 coins", "200 coins", "260 coins", "404 coins"
]



drop_chances = [0.500, 0.190, 0.120, 0.060, 0.025, 0.007, 0.003, 0.030, 0.020, 0.020, 0.015, 0.010]

card_costs = {"common_1": 25,
              "uncommon_1": 55,
              "rare_1": 80,
              "epic_1": 170,
              "mythic_1": 270,
              "legendary": 600,
              "secret": 1300}

time_limits_per_drop = {}


@client.event
async def on_ready():
    # cursor.execute("""DROP TABLE USERS""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
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
    for guild in client.guilds:
        for member in guild.members:
            if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0"
                               f"0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
                connection.commit()
            else:
                pass
    connection.commit()
    print('Бот присоеденился, ура')


class Sell(disnake.ui.View):  # класс, который позволяет после дропа либо продать карту, либо оставить
    def __init__(self, cost, name, author, rarity):
        super().__init__(timeout=30.0)  # значит что кнопки через 20 сек не будут работать(меньше захломления бота)
        self.value = Optional[bool]  # хз что это
        self.cost = cost  # цена карты
        self.name = name  # имя карты (без .png)
        self.author = author  # автор сообщения (для бд)
        self.rarity = rarity

    @disnake.ui.button(label="💸Sell💸", style=disnake.ButtonStyle.blurple)
    async def sell(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message(f"Вы продали карточку {self.name}поколение за {self.cost} :coin:")
        cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(self.cost, self.author))
        cursor.execute("UPDATE users SET mem_opened = mem_opened + {} WHERE id = {}".format(1, self.author))
        connection.commit()
        await inter.message.add_reaction("✅")
        self.value = True
        self.stop()

    @disnake.ui.button(label="🎴Take🎴", style=disnake.ButtonStyle.green)
    async def take(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message(f"Карточка *{self.name}поколение* добавлена в ваш инвентарь.")
        cursor.execute(f"UPDATE users SET {self.name} = {self.name} + {1} WHERE id = {self.author}")
        cursor.execute(f"UPDATE users SET {self.rarity[0]} = {self.rarity[0]} + {1} WHERE id = {self.author}")
        connection.commit()
        await inter.message.add_reaction("✅")
        self.value = False
        self.stop()


# ТУТ КАРОЧЕ ТЫ ДОЛЖЕН СДЕЛАТЬ, ЧТОБЫ ПРОИСХОДИЛО ТО ЖЕ САМОЕ ПРИ ДРУГИХ РЕДКОСТЯХ, КРОМЕ common. Их список выше
# Кароче тупо копипаста
def choise_card_for_drop(rarity):
    if rarity == "common":
        name = choice(common_cards)
        genre = int(name[-1])
        card = name + ".png"
        cost = 26
        for i in range(genre):
            cost -= 1
        return card, cost, name
    if rarity == "uncommon":
        name = choice(uncommon_cards)
        genre = int(name[-1])
        card = name + ".png"
        cost = 56
        for i in range(genre):
            cost -= 1
        return card, cost, name
    if rarity == "rare":
        name = choice(rare_cards)
        genre = int(name[-1])
        card = name + ".png"
        cost = 82
        for i in range(genre):
            cost -= 2
        return card, cost, name
    if rarity == "epic":
        name = choice(epic_cards)
        genre = int(name[-1])
        card = name + ".png"
        cost = 173
        for i in range(genre):
            cost -= 3
        return card, cost, name
    if rarity == "mythic":
        name = choice(mythic_cards)
        genre = int(name[-1])
        card = name + ".png"
        cost = 275
        for i in range(genre):
            cost -= 5
        return card, cost, name
    if rarity == "legendary":
        name = choice(legendary_cards)
        genre = int(name[-1])
        card = name + ".png"
        cost = 615
        for i in range(genre):
            cost -= 15
        return card, cost, name
    if rarity == "secret":
        name = choice(uncommon_cards)
        genre = int(name[-1])
        card = name + ".png"
        cost = 1330
        for i in range(genre):
            cost -= 30
        return card, cost, name
    if rarity == "80 coins":
        money = [80]
        return money
    if rarity == "125 coins":
        money = [125]
        return money
    if rarity == "200 coins":
        money = [200]
        return money
    if rarity == "260 coins":
        money = [260]
        return money
    if rarity == "404 coins":
        money = [404]
        return money


@client.event
async def on_member_join(member):  # все кто зашёл на сервер с ботом попадают в бд
    if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
        cursor.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)")
        connection.commit()

    else:
        pass


@client.command(aliases=["дроп", "drop", "получить"])
async def __drop(ctx):
    if f"{ctx.author}" in time_limits_per_drop:  # проверка на есть ли id человека в словаре ограничений по
        time_left = time_limits_per_drop.get(f"{ctx.author}").replace(
            microsecond=0) - datetime.datetime.now().replace(microsecond=0)  # убирание миллисекунд из счётчика времени(для красоты)
        if time_left < datetime.timedelta(0):  # если время до следующего использования комманды кончилось
            del time_limits_per_drop[f"{ctx.author}"]  # то челик убирается из словаря

    if f"{ctx.author}" not in time_limits_per_drop: # если автора нет в словаре
        rarity = random.choices(drop_list, weights=drop_chances, k=1)  # выбирается дроп из листа того, что может выпасть
        print(rarity)
        drop = choise_card_for_drop(*rarity)  # отправление того, что выпало в функцию, которая была выше
        print(drop)
        if len(drop) == 1:
            await ctx.send(f"{ctx.author}, **поздравляем**, вы получили **{drop[0]}** :coin: монет!,")
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(drop[0], ctx.author.id))

        else:
            cost = drop[1]  # итоговоая цена карты
            name = drop[2]  # название карты (без ".png").  В drop[0] название карты с ".png"
            await ctx.send(
                f"{ctx.author}, вы получили **{', '.join(rarity)}** карточку,"
                f" поздравляем!", file=disnake.File(f"./cards/{', '.join(rarity)}/{drop[0]}")) # отправляется сообщение о
            # карточке, которая ищется в папке cards/(название редкости)/(название карты)
            sell_or_take = Sell(cost, name, ctx.author.id, rarity)  # создания экземпляра класса Sell, который был выше.
            await ctx.send(
                f"Вы хотите оставить **{name}** или продать **{name}** узбекам за **{cost}** :coin:?",
                view=sell_or_take)  # view=sell_or_take - это появление кнопок под сообщением

        time_limits_per_drop[f"{ctx.author}"] = \
            datetime.datetime.now() + datetime.timedelta(minutes=4)  # minutes-это сколько времени перед след дропом
    else:
        await ctx.send(f"{ctx.author}, вы сможете использовать дроп только через {time_left}")
    connection.commit()


# ПРОСТО КОММАНДА РАБОТАТЬ, ТЫ ДОЛЖЕН ПОМНИТЬ
@client.command(aliases=["работать", "work", "зарабатывать"])
async def __working(ctx):
    income = choice(work_incom)
    cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(income, ctx.author.id))
    connection.commit()
    await ctx.send(f"**{ctx.author}**, вы заработали {income} **монеток** :coin:")
    await ctx.message.add_reaction("✅")
    connection.commit()


# С ПОМОЩЬЮ ЭТОЙ КОМАНДЫ МОЖНО СМОТРЕТЬ БАЛАНС ДРУГИХ ПОЛЬЗОВАТЕЛЕЙ (ТОЛЬКО АДМИНЫ ТАК МОГУТ)
@client.command(aliases = ["admin_balance", "seebalance", "see_balance", "посмотреть_баланс"])
@commands.has_permissions(administrator=True)
async def __balance(ctx, member: disnake.Member = None):
    if member is None:
        member = ctx.author
    cash = cursor.execute(f'SELECT cash FROM users WHERE id = {member.id}').fetchone()[0]
    await ctx.send(embed=disnake.Embed(description=f'Баланс пользователя *{member.name}* составляет **{cash} мемокоинов :coin:  ** (__только админы могут смотреть чужой баланс__)'))


# ПРОСТО АДМИН КОМАНДА ДЛЯ ВЫДАЧИ МОНЕТОК
@client.command(aliases = ["award", "give", "выдать", "donate", "наградить", "дать"])
@commands.has_permissions(administrator=True)
async def __award(ctx, member: disnake.Member = None, amount: int = None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите пользователя, которому хотите выдать мемокоины")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, укажите сумму мемокоинов, которую хотите выдать человеку :coin: ")
        elif int(amount) < 1:
            await ctx.send(f"**{ctx.author}**, минимальная сумма выдаваемых мемокоинов - **1** :coin: ")
        else:
            cursor.execute("UPDATE users SET cash = cash + {} WHERE id = {}".format(int(amount), member.id))
            connection.commit()
            await ctx.message.add_reaction("✅")
            await ctx.send(f"Сумма **{amount}** мемокоинов была переведена на счёт пользователя :coin:")


# ПРОСТО АДМИН КОМАНДА ДЛЯ ЗАБИРАНИЯ МОНЕТОК
@client.command(aliases=["take", "забрать"])
@commands.has_permissions(administrator=True)
async def __take(ctx, member: disnake.Member = None, amount=None):
    if member is None:
        await ctx.send(f"**{ctx.author}**, укажите сперва пользователя, у которого хотите изъять мемокоины")
    else:
        if amount is None:
            await ctx.send(f"**{ctx.author}**, укажите сумму мемокоинов, которую хотите изъять :coin: ")
        elif amount == "all":
            cursor.execute("UPDATE users SET cash = {} WHERE id = {}".format(0, member.id))
            connection.commit()
            await ctx.message.add_reaction("✅")
        elif int(amount) < 1:
            await ctx.send(f"**{ctx.author}**, минимальная сумма забираемых мемокоинов - **1** :coin: ")
        else:
            cursor.execute("UPDATE users SET cash = cash - {} WHERE id = {}".format(int(amount), member.id))
            connection.commit()
            await ctx.message.add_reaction("✅")
            await ctx.send(f"Сумма **{amount}** мемокоинов была изъяна со счета пользователя :coin:")


# ЭТО БЕСПОЛЕЗНО, ПОКА ЧТО ЗАБЕЙ

@client.command(aliases=[
    "купить_ящик","купить_кейс", "buycrate", "buy", "кейс", "кейсы", "crate", "crates", "box", "бокс", "купить", "цена"
])
async def __buy_crate(ctx):
    await ctx.send(
        f"**{ctx.author}**, вы желаете приобрести мемокейс за **50** мемокоинов? :coin: **Напишите** __'!!открыть'__ .")




#ПРОСТО ПРИСЫЛАЕТ ДРОП. ШАНСЫ
@client.command(aliases=[
    "дропинфо", "дропшансы", "dropchances", "Дропшансы", "Дропинфо", "ДропИнфо", "chances", "шансы"
])
async def __see_drop_chances(ctx):
    await ctx.send(embed=disnake.Embed(
        description=f"Дроп ничего не стоит, активируется по комманде !!drop."
                    f" \n :coin: **Напишите** *'!!дроп'* , чтобы получить карточку.ᅠ ᅠᅠ ᅠ"
                    f"\n *Шанс на обычную карту* - **50%**. \n  *Шанс на необычную карту* - **19%**. \n "
                    f"*Шанс на редкую карту* - **12%** \n *Шанс на эпическую карту* - **6%**."
                    f"\n *Шанс на мифическую карту* - **2.5%**. \n *Шанс на легендарную карту* - **0.7%**"
                    f"\n *Шанс на секретную карту* - **0.3%**. \n *Шанс на разное кол-во мемокоинов* - **9.5%**"))


# инвентарь с карточками (не сделал)
@client.command(aliases=[
    "cards", "inventory", "карты", "инвентарь", "мои", "мой", "my"
])
async def __inventory(ctx):
    records = cursor.execute(f"""SELECT * from users WHERE id = {ctx.author.id}""").fetchall()
    counter = 0
    profile = []
    print(records)
    for i in records:
        for row in i:
            counter += 1
            if counter >= 6:
                profile.append(row)
    cards = []
    counter2 = 0
    for i in all_cards:
        cards.append(f"{i} : {profile[counter2]}")
        counter2 += 1
    await ctx.send(embed=disnake.Embed(
        description=f" **--ИНВЕНТАРЬ--** \n"
                    f"{*cards,}"))


@client.command(aliases=[
    "профиль", "мой профиль", "profile", "menu", "меню" 'balance', 'баланс', 'cash',
    'кеш', "мани", "деньги", "coins", "money", "memcoins"
])
async def __info(ctx):
    opened = cursor.execute(f'SELECT mem_opened FROM users WHERE id = {ctx.author.id}').fetchone()[0]
    cash = cursor.execute(f'SELECT cash FROM users WHERE id = {ctx.author.id}').fetchone()[0]
    commons = cursor.execute(f"SELECT common FROM users WHERE id = {ctx.author.id}").fetchone()[0]
    uncommons = cursor.execute(f"SELECT uncommon FROM users WHERE id = {ctx.author.id}").fetchone()[0]
    rares = cursor.execute(f"SELECT rare FROM users WHERE id = {ctx.author.id}").fetchone()[0]
    epics = cursor.execute(f"SELECT epic FROM users WHERE id = {ctx.author.id}").fetchone()[0]
    mythics = cursor.execute(f"SELECT mythic FROM users WHERE id = {ctx.author.id}").fetchone()[0]
    secrets = cursor.execute(f"SELECT secret FROM users WHERE id = {ctx.author.id}").fetchone()[0]
    legendarys = cursor.execute(f"SELECT legendary FROM users WHERE id = {ctx.author.id}").fetchone()[0]
    await ctx.send(embed=disnake.Embed(
        description=f" **--ПРОФИЛЬ--**"
                    f"\n"
                    f"Ваш баланс составляет  **{cash} мемокоинов :coin:  **ᅠ ᅠ ᅠ ᅠᅠ ᅠ ᅠ ᅠᅠ   ᅠ ᅠ "
                    f"Получено карт: **{opened}**."
                    f"\n Получено обычных карт: **{commons}**"
                    f"\n Получено необычных карт: **{uncommons}**"
                    f"\n Получено редких карт: **{rares}**"
                    f"\n Получено эпических карт: **{epics}**"
                    f"\n Получено мифических карт: **{mythics}**"
                    f"\n Получено легендарных карт: **{legendarys}**"
                    f"\n Получено секретных карт: **{secrets}**"))


@client.command(aliases=[
    "комманды", "commands", "command", "функции", "возможности", "инфо", "помощь", "help"
])
async def __commands(ctx):
    await ctx.send(embed=disnake.Embed(
        description=f"*Комманды:* \n **!!(дропинфо/шансы)**,  **!!(профиль/баланс/меню)**,  **!!(работать/work)**, "
                    f" \n**!!(дроп/drop)**,  **!!(карты/инвентарь)**"))
client.run("OTcxNzczOTU2NjYxMDc2MDI4.GBFUWv.U4UJzDj-nQ0ka57jo_AxWpSHcZD3yG1CU0Ple4")
