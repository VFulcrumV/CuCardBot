import disnake
import random
from disnake.ext import commands

from CuCardBot.functions import data_base_functions as db, buttons, variables as v, system_functions as sf


class Moderators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = db.connection
        self.cursor = self.connection.cursor()

    @commands.command(name="админдроп", aliases=["testdrop", "admindrop"])
    @commands.has_permissions(administrator=True)
    async def admin_drop(self, ctx):
        weights = list(map(lambda val: val['drop_chance'], v.admin_drop_info.values()))
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

    @commands.command(name="просмотреть баланс у любого человека", aliases=["админ_баланс", "see_balance"])
    @commands.has_permissions(administrator=True)
    async def check_user_balance(self, ctx, user: disnake.Member):
        cash = self.cursor.execute(f'SELECT cash FROM users WHERE id = {user.id}').fetchone()[0]
        await ctx.send(embed=disnake.Embed(
            description=f'Баланс пользователя *{user.mention}* составляет **{cash}** :coin:'))

    @commands.command(name="выдать деньги человеку", aliases=["выдать", "award"])
    @commands.has_permissions(administrator=True)
    async def award(self, ctx, user: disnake.Member = None, amount: int = None):
        if int(amount) < 1:
            await ctx.send(
                f"Минимальная сумма выдаваемых коинов: **1** :coin:",
                ephemeral=True
            )
        else:
            db.give_take_money(self, amount, user.id, '+')
            await ctx.send(
                f"Сумма **{amount}** :coin: была переведена на счёт пользователя {user.mention}"
            )

    @commands.command(name="забрать деньги у человека", aliases=["забрать", "take"])
    @commands.has_permissions(administrator=True)
    async def take_away_coins(self, ctx, user: disnake.Member=None, amount=None):
        if int(amount) < 1:
            await ctx.send(
                f"Минимальная сумма забираемых кардкоинов: **1** :coin:"
            )
        else:
            db.give_take_money(self, amount, user, '-')
            await ctx.send(
                f"Сумма **{amount}** :coin: была изъяна со счета пользователя {user.mention}"
            )


def setup(bot):
    bot.add_cog(Moderators(bot))
