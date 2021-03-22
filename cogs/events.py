from os import name
import discord
from discord import activity
from discord.ext import commands, tasks
import logging
import random

class Events(commands.Cog):
    """event handler"""
    
    def __init__(self, bot):
        self.bot = bot
        self.statuses = [
            ("watching", f"{len(self.bot.guilds)} servers"),
            ("watching", "jiyoonbot.xyz")
        ]
        self.activities = {"playing": 0, "streaming": 1, "listening": 2, "watching": 3}
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: events.py connected")
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.status_loop.start()

    @tasks.loop(minutes=5.0)
    async def status_loop(self):
        try:
            await self.next_status()
        except Exception as e:
            logging.error(f"{e}")
    
    async def next_status(self):
        new_status = random.randrange(0, len(self.statuses))
        new_status = self.statuses[new_status]
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType(self.activities[new_status[0]]), name=new_status[1]
            )
        )

def setup(bot):
    bot.add_cog(Events(bot))