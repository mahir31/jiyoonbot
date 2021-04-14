from os import name
import discord
from discord import activity
from discord.ext import commands, tasks
import logging
import random
from data import database as db

class Events(commands.Cog):
    """event handler"""
    
    def __init__(self, bot):
        self.bot = bot
        self.statuses = [
            (3, lambda: f"{len(self.bot.guilds)} servers"),
            (3, lambda: "jiyoonbot.xyz")
        ]

    @commands.Cog.listener()
    async def on_ready(self):
        self.status_loop.start()

    @tasks.loop(minutes=5.0)
    async def status_loop(self):
        try:
            await self.change_status()
        except Exception as e:
            logging.error(f"{e}")
    
    async def change_status(self):
        new_status = random.randrange(0, len(self.statuses))
        new_status = self.statuses[new_status]
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType(new_status[0]), name=new_status[1]()
            )
        )
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.new_guild_prefix(guild.id)
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db.remove_guild_prefix(guild.id)

def setup(bot):
    bot.add_cog(Events(bot))