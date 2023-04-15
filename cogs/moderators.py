import disnake
from disnake.ext import commands

from CuCardBot.functions import data_base_functions as db


class Moderators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = db.connection
        self.cursor = self.connection.cursor()

    @commands.slash_command(name="check_user_balance")
    @commands.has_permissions(administrator=True)
    async def check_user_balance(self, ctx, user: disnake.Member):
        cash = self.cursor.execute(f'SELECT cash FROM users WHERE id = {user.id}').fetchone()[0]
        await ctx.response.send_message(embed=disnake.Embed(
            description=f'Баланс пользователя *{user.mention}* составляет **{cash}** :coin:'))

    @commands.command(name="просмотреть баланс у любого человека", aliases=["админ_баланс", "see_balance"])
    @commands.has_permissions(administrator=True)
    async def check_user_balance_2(self, ctx, user: disnake.Member):
        cash = self.cursor.execute(f'SELECT cash FROM users WHERE id = {user.id}').fetchone()[0]
        await ctx.response.send_message(embed=disnake.Embed(
            description=f'Баланс пользователя *{user.mention}* составляет **{cash}** :coin:'))

    @commands.slash_command(name="award_user_balance")
    @commands.has_permissions(administrator=True)
    async def award(self, ctx, user: disnake.Member = None, amount: int = None):
        if int(amount) < 1:
            await ctx.response.send_message(
                f"Минимальная сумма выдаваемых коинов: **1** :coin:",
                ephemeral=True
            )
        else:
            db.give_take_money(self, amount, user.id, '+')
            await ctx.response.send_message(
                f"Сумма **{amount}** :coin: была переведена на счёт пользователя {user.mention}"
            )

    @commands.command(name="выдать деньги человеку", aliases=["выдать", "award"])
    @commands.has_permissions(administrator=True)
    async def award_2(self, ctx, user: disnake.Member = None, amount: int = None):
        if int(amount) < 1:
            await ctx.response.send_message(
                f"Минимальная сумма выдаваемых коинов: **1** :coin:",
                ephemeral=True
            )
        else:
            db.give_take_money(self, amount, user.id, '+')
            await ctx.response.send_message(
                f"Сумма **{amount}** :coin: была переведена на счёт пользователя {user.mention}"
            )

    @commands.slash_command(name="take_from_the_user_balance")
    @commands.has_permissions(administrator=True)
    async def take_away_coins(self, ctx, user: disnake.Member = None, amount=None):
        if int(amount) < 1:
            await ctx.response.send_message(
                f"Минимальная сумма забираемых кардкоинов: **1** :coin:",
                ephemeral=True
            )
        else:
            db.give_take_money(self, amount, user, '-')
            await ctx.response.send_message(
                f"Сумма **{amount}** :coin: была изъяна со счета пользователя {user.mention}"
            )

    @commands.command(name="забрать деньги у человека", aliases=["забрать", "take"])
    @commands.has_permissions(administrator=True)
    async def take_away_coins_2(self, ctx, user: disnake.Member=None, amount=None):
        if int(amount) < 1:
            await ctx.response.send_message(
                f"Минимальная сумма забираемых кардкоинов: **1** :coin:",
                ephemeral=True
            )
        else:
            db.give_take_money(self, amount, user, '-')
            await ctx.response.send_message(
                f"Сумма **{amount}** :coin: была изъяна со счета пользователя {user.mention}"
            )


def setup(bot):
    bot.add_cog(Moderators(bot))