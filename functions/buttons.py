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
        await inter.response.send_message(f"Вы продали карточку *{self.name}* за **{self.cost}** :coin:")
        db.sell_card(self)
        self.stop()

    @disnake.ui.button(label="🎴Take🎴", style=disnake.ButtonStyle.green)
    async def take(self, button: disnake.ui.Button, inter: disnake.CommandInteraction):
        await inter.response.send_message(f"Карточка *{self.name}* добавлена в ваш инвентарь.")
        db.take_card(self)
        self.stop()