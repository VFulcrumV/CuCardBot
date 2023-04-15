import os

from typing import Optional

import disnake
from disnake.ext import commands


bot = commands.Bot(
    command_prefix='!!',
    help_command=None,
    intents=disnake.Intents.all(),
)


@bot.command()
@commands.is_owner()
async def load(ctx, extention):
    bot.load_extension(f'cogs.{extention}')


@bot.command()
@commands.is_owner()
async def unload(ctx, extention):
    bot.unload_extension(f'cogs.{extention}')


@bot.command()
@commands.is_owner()
async def reload(ctx, extention):
    bot.reload_extension(f'cogs.{extention}')


for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == '__main__':
    bot.run('OTcxNzczOTU2NjYxMDc2MDI4.GDfXbO.Oz0tzanu61HVkqjaiVge66UuC4O7gf-kSFVQig')
    print("💓 Бот запущен 💓")