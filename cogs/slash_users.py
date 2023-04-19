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

    @commands.slash_command(name='see')
    async def see(self, ctx, name=None):
        a = db.see_card(self, name, ctx.author.id)
        if a == "no":
            await ctx.send(f"{ctx.author.mention}, карточки **{name}** у вас нет или вы ввели название неправильно.",
                           ephemeral=True)
        else:
            await ctx.send(f"{ctx.author.mention}", file=disnake.File(a))

    @commands.slash_command(name='drop')
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
                    f"или продать **{name}** узбекам за **{cost}** :coin:?",
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
                    f"{ctx.author.mention}, вы сможете использовать дроп только через {time_left}",
                    ephemeral=True
                )

    @commands.slash_command(name="work")
    async def work(self, ctx):
        income = random.choice([1, 2, 3, 4, 5, 0, 1, 1, 2, 3])
        db.give_take_money(self, income, ctx.author.id, '+')
        self.connection.commit()
        await ctx.send(f"**{ctx.author}**, вы заработали {income} **монеток** :coin:")
        db.give_take_money(self, income, ctx.author.id, '+')

    @commands.slash_command()
    async def buy_box(self, ctx):
        pass

    @commands.slash_command(name="chances")
    async def check_drop_chances(self, ctx):
        await ctx.send(embed=disnake.Embed(
            description=f"Дроп ничего не стоит, активируется по комманде /drop раз в 4 минуты."
                        f"\n *Шанс на обычную карту* - **49%**. \n  *Шанс на необычную карту* - **20%**. \n "
                        f"*Шанс на редкую карту* - **12,4%** \n *Шанс на эпическую карту* - **7%**."
                        f"\n *Шанс на мифическую карту* - **3.25%**. \n *Шанс на легендарную карту* - **0.9%**"
                        f"\n *Шанс на секретную карту* - **0.35%**. \n *Шанс на разное кол-во мемокоинов* - **7%**"))

    @commands.slash_command(name="inventory")
    async def inventory(self, ctx):
        records = self.cursor.execute(f"""SELECT * from users WHERE id = {ctx.author.id}""").fetchall()
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
        for i in v.all_cards:
            cards.append(f"{i} : {profile[counter2]}")
            counter2 += 1
        await ctx.send(embed=disnake.Embed(
            description=f" **--ИНВЕНТАРЬ--** \n"
                        f"{cards}"))

    @commands.slash_command(name="profile")
    async def profile(self, ctx):
        opened = self.cursor.execute(f'SELECT mem_opened FROM users WHERE id = {ctx.author.id}').fetchone()[0]
        cash = self.cursor.execute(f'SELECT cash FROM users WHERE id = {ctx.author.id}').fetchone()[0]
        commons = self.cursor.execute(f"SELECT common FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        uncommons = self.cursor.execute(f"SELECT uncommon FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        rares = self.cursor.execute(f"SELECT rare FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        epics = self.cursor.execute(f"SELECT epic FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        mythics = self.cursor.execute(f"SELECT mythic FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        secrets = self.cursor.execute(f"SELECT secret FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        legendarys = self.cursor.execute(f"SELECT legendary FROM users WHERE id = {ctx.author.id}").fetchone()[0]
        await ctx.send(embed=disnake.Embed(
            description=f" **--ПРОФИЛЬ--**"
                        f"\n"
                        f"Ваш баланс составляет  **{cash} мемокоинов :coin:  **"
                        f"Получено карт: **{opened}**."
                        f"\n Получено обычных карт: **{commons}**"
                        f"\n Получено необычных карт: **{uncommons}**"
                        f"\n Получено редких карт: **{rares}**"
                        f"\n Получено эпических карт: **{epics}**"
                        f"\n Получено мифических карт: **{mythics}**"
                        f"\n Получено легендарных карт: **{legendarys}**"
                        f"\n Получено секретных карт: **{secrets}**"))

    @commands.slash_command(name="help")
    async def help_commands(self, ctx):
        await ctx.send(embed=disnake.Embed(
            description=f"*Комманды:* \n **!!(дропинфо/шансы)**,  **!!(профиль/баланс/меню)**,  **!!(работать/work)**, "
                        f" \n**!!(дроп/drop)**,  **!!(карты/инвентарь)**"))


def setup(bot):
    bot.add_cog(SlashUsers(bot))
