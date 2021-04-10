import sys
import discord
from discord.ext import commands
import logging
from tools import help
import os
from tools import utilities as util

logging.basicConfig(level=logging.INFO)

if len(sys.argv) > 1:
    DEV = sys.argv[1] == "dev"
else:
    DEV = False

logging.info(f'DEVELOPER MODE IS {"ON" if DEV else "OFF"}')

TOKEN = os.environ['GLENN_BOT_TOKEN' if DEV else 'JIYOON_BOT_TOKEN']

bot = commands.Bot(
    owner_id=277176590402846721,
    help_command=help.helpembeds(),
    command_prefix= ">" if DEV else (util.get_prefix), 
    intents=discord.Intents().all(), 
    case_insensitive=True
    )

@bot.before_invoke
async def before_any_command(ctx):
    try:
        await ctx.trigger_typing()
    except discord.errors.Forbidden as e:
        await ctx.send(f'{e.__class__.__name__}: {e}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        logging.info(f'cog:{filename} loaded')

bot.run(TOKEN)