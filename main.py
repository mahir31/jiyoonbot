import discord
from discord.ext import commands
import logging
from tools import help
import os

logging.basicConfig(level=logging.DEBUG)

TOKEN = os.environ['JIYOON_BOT_TOKEN']

bot = commands.Bot(owner_id=277176590402846721,
    help_command=help.helpembeds(),
    command_prefix='$', 
    intents=discord.Intents().all(), 
    case_insensitive=True)

@bot.event
async def on_ready():
	print(f"{bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n")

@bot.before_invoke
async def before_any_command(ctx):
    try:
        await ctx.trigger_typing()
    except discord.errors.Forbidden:
        pass

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f"cogs.{extension} has been reloaded")

bot.run(TOKEN)