import disnake
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
        await ctx.send(f'Ошибка в использовании комманды: {error}'
                       f'Тип ошибки: {type(error)}', ephemeral=True)
        print(f'Ошибка в использовании комманды: {error}')
        print(f'Тип ошибки: {type(error)}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f'Ошибка в использовании комманды: {error}'
                       f'Тип ошибки: {type(error)}')
        print(f'Ошибка в использовании комманды: {error}')
        print(f'Тип ошибки: {type(error)}')


def setup(bot):
    bot.add_cog(Events(bot))
