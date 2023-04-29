import disnake

from CuCardBot.functions import data_base_functions as db


class SellTakeButtons(disnake.ui.View):
    def __init__(self, cost, name, author, rarity):
        super().__init__(timeout=30.0)
        self.cost = cost
        self.name = name
        self.author = author
        self.rarity = rarity
        self.connection = db.connection
        self.cursor = self.connection.cursor()

    @disnake.ui.button(label="💸Sell💸", style=disnake.ButtonStyle.blurple)
    async def sell(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        if self.author != inter.author.id:
            return
        else:
            await inter.response.send_message(f"Вы продали карточку *{self.name}* за **{self.cost}** :coin:")
            db.sell_card(self)
            self.stop()

    @disnake.ui.button(label="🎴Take🎴", style=disnake.ButtonStyle.green)
    async def take(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        if self.author != inter.author.id:
            return
        else:
            await inter.response.send_message(f"Карточка *{self.name}* добавлена в ваш инвентарь.")
            db.take_card(self)
            db.increase_rarity(self, self.rarity)
            self.stop()


class AfterCraftButtons(disnake.ui.View):
    def __init__(self, card_name, end_card_name, cost, rarity, author):
        super().__init__(timeout=30.0)
        self.cost = cost
        self.name_before = card_name
        self.name = end_card_name
        self.author = author
        self.rarity = rarity
        self.connection = db.connection
        self.cursor = self.connection.cursor()
        self.num_cards = db.number_of_cards_in_inv(self, self.name_before, self.author)
        self.persone_money = db.member_money(self)

    @disnake.ui.button(label="🔨Да🔨", style=disnake.ButtonStyle.green)
    async def sell(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        if self.author != inter.author.id:
            return
        else:
            if self.num_cards >= 2 and self.persone_money >= self.cost:
                db.give_take_money(self, self.cost, self.author, "-")
                await inter.response.send_message(f"Вы получили карточку **{self.name}**",
                                                  file=disnake.File(f"./cards/{self.rarity}/{self.name}.png"))
                db.take_away_card(self, self.author, self.name_before, 2)
                db.take_card(self)
            else:
                await inter.response.send_message(f"У вас не хватает монет или самих карточек ("
                                                  f"нужно **{self.cost}** :coin: и *2* карточки"
                                                  f" **{self.name_before}**)",
                                                  ephemeral=True)
        self.stop()

    @disnake.ui.button(label="❌Нет❌", style=disnake.ButtonStyle.red)
    async def take(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        if self.author != inter.author.id:
            return
        else:
            await inter.response.send_message(f"Вы решили не крафтить карточку.")
            self.stop()
