import discord
from discord.ext import commands, tasks
import logging

class Events(commands.Cog):
    """event handler"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: events.py connected")

def setup(bot):
    bot.add_cog(Events(bot))