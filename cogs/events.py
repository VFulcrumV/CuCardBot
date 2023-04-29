import logging

from disnake.ext import commands

from CuCardBot.functions import data_base_functions as db


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = db.connection
        self.cursor = self.connection.cursor()

    @commands.Cog.listener()
    async def on_ready(self):
        db.create_start_database(self)
        print(f'Bot {self.bot.user} is ready to work!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db.add_new_member(self, member)

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f'Ошибка в использовании команды: неверно заполнены аргументы', ephemeral=True)
        else:
            logging.basicConfig(level=logging.WARNING, filename="log.log", filemode="w",
                                format="%(asctime)s %(levelname)s %(message)s")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f'Ошибка в использовании команды: неверно заполнены аргументы')
        else:
            logging.basicConfig(level=logging.WARNING, filename="log.log", filemode="w",
                                format="%(asctime)s %(levelname)s %(message)s")


def setup(bot):
    bot.add_cog(Events(bot))
