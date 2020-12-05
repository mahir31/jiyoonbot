import discord
import logging
from discord.ext import commands
from discord import Spotify

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: misc.py connected")

def setup(bot):
    bot.add_cog(misc(bot))