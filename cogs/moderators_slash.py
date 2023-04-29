import disnake
import random
from disnake.ext import commands

from CuCardBot.functions import data_base_functions as db, buttons, variables as v, system_functions as sf


class SlashModerators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = db.connection
        self.cursor = self.connection.cursor()

    @commands.slash_command(name="admin_drop", description="Гораздо более везучий дроп, для админов")
    @commands.has_permissions(administrator=True)
    async def admin_drop_slash(self, ctx):
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

    @commands.slash_command(name="check_user_balance")
    @commands.has_permissions(administrator=True)
    async def check_user_balance(self, ctx, user: disnake.Member):
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


def setup(bot):
    bot.add_cog(SlashModerators(bot))
