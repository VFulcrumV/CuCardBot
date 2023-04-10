import datetime
import random

import disnake
from disnake.ext import commands

from CuCardBot.functions import data_base_functions as db, variables as v, buttons, system_functions as sf


class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = db.connection
        self.cursor = self.connection.cursor()

    @commands.slash_command(name='drop')
    async def drop(self, ctx):
        if f"{ctx.author}" not in v.time_limits_per_drop:
            weights = list(map(lambda val: val['drop_chance'], v.drop_info.values()))
            rarity = random.choices(
                list(v.drop_info.keys()),
                weights=weights,
                k=1)[0]
            drop = sf.choose_card_for_drop(rarity)
            if rarity == 'coins':
                await ctx.send(f"{ctx.author}, **поздравляем**, вы получили **{drop}** :coin: монет!")
                db.give_take_money(self, drop, ctx.author.id, '+')

            else:
                cost = drop[1]
                name = drop[2]
                await ctx.send(
                    f"{ctx.author}, вы получили **{rarity}** карточку, поздравляем!",
                    file=disnake.File(f"./cards/{rarity}/{drop[0]}")
                )
                sell_or_take = buttons.SellTakeButtons(cost, name, ctx.author.id, rarity)
                await ctx.send(
                    f"Вы хотите оставить **{name}** или продать **{name}** узбекам за **{cost}** :coin:?",
                    view=sell_or_take
                )
            v.time_limits_per_drop[f"{ctx.author}"] = datetime.datetime.now() + datetime.timedelta(minutes=4)
        else:
            time_left = v.time_limits_per_drop.get(f"{ctx.author}").replace(microsecond=0)
            time_left -= datetime.datetime.now().replace(microsecond=0)
            if time_left < datetime.timedelta(0):
                del v.time_limits_per_drop[f"{ctx.author}"]
            else:
                await ctx.send(
                    f"{ctx.author}, вы сможете использовать дроп только через {time_left}",
                    ephemeral=True
                )

    # @commands.slash_command()
    # async def balance(self, ctx):
    #     pass
    #
    # @commands.slash_command()
    # async def work(self, ctx):
    #     pass
    #
    # @commands.slash_command()
    # async def buy_box(self, ctx):
    #     pass
    #
    # @commands.slash_command()
    # async def check_drop_chances(self, ctx):
    #     pass
    #
    # @commands.slash_command()
    # async def inventory(self, ctx):
    #     pass
    #
    # @commands.slash_command()
    # async def profile(self, ctx):
    #     pass
    #
    # @commands.slash_command()
    # async def help_commands(self, ctx):
    #     pass


def setup(bot):
    bot.add_cog(Users(bot))