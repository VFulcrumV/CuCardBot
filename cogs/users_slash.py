import datetime
import random

import disnake
from datetime import timedelta
from disnake.ext import commands

from CuCardBot.functions import data_base_functions as db, variables as v, buttons, system_functions as sf


class SlashUsers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = db.connection
        self.cursor = self.connection.cursor()

    @commands.slash_command(name="upgrade", description="Получить из двух одинаковых карточек "
                                                        "карточку выше по редкости того же поколения")
    async def upgrade(self, ctx, name=None):
        crafting = sf.crafting_cards(name)
        if crafting[0] == "wrong card":
            await ctx.send(f"{ctx.author.mention}, вы ввели неправильное название карты.")
        elif crafting[0] == "wrong rarity":
            await ctx.send(f"{ctx.author.mention}, из карт редкости **{crafting[1]}** нельзя ничего скрафтить.")
        else:
            craft_or_no = buttons.AfterCraftButtons(crafting[0], crafting[1], crafting[2], crafting[3], ctx.author.id)
            await ctx.send(
                f"{ctx.author.mention}, вы хотите получить карточку редкости **{crafting[3]}**"
                f" того же поколения, что и ваша карточка? \n"
                f"Это будет стоить **{crafting[2]}** :coin: и потратится 2 карточки **{crafting[0]} .**",
                view=craft_or_no
            )

    @commands.slash_command(name='see', description="Просмотреть карточку из вашего инвентаря")
    async def see(self, ctx, name=None):
        a = db.see_card(self, name, ctx.author.id)
        print(a)
        if a == "no":
            await ctx.send(f"В инвентаре карточка с таким названием отсутствует",
                           ephemeral=True)
        else:
            await ctx.send(f"{ctx.author.mention}", file=disnake.File(a))

    @commands.slash_command(name='drop', description="Получить случайную карточку бесплатно.")
    async def drop(self, ctx):
        if f"{ctx.author}" in v.time_limits_per_drop:
            time_left = v.time_limits_per_drop.get(f"{ctx.author}").replace(microsecond=0)
            time_left -= datetime.datetime.now().replace(microsecond=0)
            if time_left < timedelta(0):
                del v.time_limits_per_drop[f"{ctx.author}"]
        if f"{ctx.author}" not in v.time_limits_per_drop:
            weights = list(map(lambda val: val['drop_chance'], v.drop_info.values()))
            rarity = random.choices(
                list(v.drop_info.keys()),
                weights=weights,
                k=1)[0]
            drop = sf.choose_card_for_drop(rarity)
            if rarity == 'coins':
                await ctx.send(f"{ctx.author.mention}, **поздравляем**, вы получили **{drop}** :coin: монет!")
                db.give_take_money(self, drop, ctx.author.id, '+')

            else:
                cost = drop[1]
                name = drop[2]
                await ctx.send(
                    f"{ctx.author.mention}, вы получили **{rarity}** карточку, поздравляем!",
                    file=disnake.File(f"./cards/{rarity}/{drop[0]}")
                )
                sell_or_take = buttons.SellTakeButtons(cost, name, ctx.author.id, rarity)
                await ctx.send(
                    f" {ctx.author.mention}Вы хотите оставить **{name}** "
                    f"или продать **{name}** за **{cost}** :coin:?",
                    view=sell_or_take
                )
            v.time_limits_per_drop[f"{ctx.author}"] = datetime.datetime.now() + timedelta(minutes=4)
        else:
            time_left = v.time_limits_per_drop.get(f"{ctx.author}").replace(microsecond=0)
            time_left -= datetime.datetime.now().replace(microsecond=0)
            if time_left < timedelta(0):
                del v.time_limits_per_drop[f"{ctx.author}"]
            else:
                await ctx.send(
                    f"Вы сможете использовать дроп только через {time_left}",
                    ephemeral=True
                )

    @commands.slash_command(name="work", description="Получить 0-5 монеток")
    async def work(self, ctx):
        income = random.choice([1, 2, 3, 4, 5, 0, 1, 1, 2, 3])
        db.give_take_money(self, income, ctx.author.id, '+')
        self.connection.commit()
        await ctx.send(f"**{ctx.author}**, вы заработали {income} **монеток** :coin:")
        db.give_take_money(self, income, ctx.author.id, '+')

    @commands.slash_command()
    async def buy_box(self, ctx):
        pass

    @commands.slash_command(name="chances", description="Шансы дропа")
    async def check_drop_chances(self, ctx):
        await ctx.send(embed=disnake.Embed(
            description=f"Дроп ничего не стоит, активируется по комманде /drop раз в 4 минуты."
                        f"\n *Шанс на обычную карту* - **45%**. \n  *Шанс на необычную карту* - **21%**. \n "
                        f"*Шанс на редкую карту* - **14,5%** \n *Шанс на эпическую карту* - **7%**."
                        f"\n *Шанс на мифическую карту* - **3.5%**. \n *Шанс на легендарную карту* - **0.85%**"
                        f"\n *Шанс на секретную карту* - **0.30%**. \n *Шанс на разное кол-во мемокоинов* - **7.75%**"))

    @commands.slash_command(name="inventory", description="Просмотреть свой инвентарь карт")
    async def inventory(self, ctx):
        data = self.cursor.execute(f"""SELECT * from users WHERE id = {ctx.author.id}""").fetchall()[0][12:]
        cards_data = []
        count = 1
        for el in zip(v.all_cards, data):
            if el[1] != 0:
                cards_data.append(f'{count}) {el[0]}\t\t\t\t{el[1]}шт.\n')
                count += 1
        cards = ''.join(cards_data)
        await ctx.send(embed=disnake.Embed(
            description=f" **--ИНВЕНТАРЬ--** \n"
                        f"{cards}"), ephemeral=True)

    @commands.slash_command(name="profile", description="Твоя статистика в целом")
    async def profile(self, ctx):
        opened = self.cursor.execute(f'SELECT cards_opened FROM users WHERE id = {ctx.author.id}').fetchone()[0]
        cash = self.cursor.execute(f'SELECT cash FROM users WHERE id = {ctx.author.id}').fetchone()[0]
        commons = self.cursor.execute(f"SELECT common FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        uncommons = self.cursor.execute(f"SELECT uncommon FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        rares = self.cursor.execute(f"SELECT rare FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        epics = self.cursor.execute(f"SELECT epic FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        mythics = self.cursor.execute(f"SELECT mythic FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        secrets = self.cursor.execute(f"SELECT secret FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        legendarys = self.cursor.execute(f"SELECT legendary FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        craftable = self.cursor.execute(f"SELECT craftable FROM users WHERE id = {ctx.author.id}").fetchone()[0]
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
                        f"\n Получено секретных карт: **{secrets}**"
                        f"\n Созданно карт: **{craftable}**"))

    @commands.slash_command(name="help", description="Просмотреть комманды и что они делают.")
    async def help_commands(self, ctx):
        await ctx.send(embed=disnake.Embed(
            description=f"*Комманды:* \n **!!(дропинфо/шансы)**, \n **!!(профиль/баланс/меню)**, \n "
                        f"**!!(работать/work)**, \n "
                        f" **!!(дроп/drop)**, \n **!!(карты/инвентарь)**, \n"
                        f" **!!(see/посмотреть)** (название карточки) - посмотреть на карточку "
                        f"(только если она в инвентаре), \n**!!(улучшить/upgrade)** (название карточки)"
                        f" - крафтится карточка"
                        f" следуюшей редкости того же поколения, но нужно иметь 2 изначальной карточки и опр. кол-во"
                        f"монет."))


def setup(bot):
    bot.add_cog(SlashUsers(bot))
