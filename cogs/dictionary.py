import discord
from discord.ext import commands
import logging
from tools import ox_requests as ox
import json

class Dictionary(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: dictionary.py connected")

    # commands
    @commands.group(case_insensitive=True)
    async def dc(self, ctx):
        '''Dictionary commands'''

    @dc.command(aliases=["df"])
    async def define(self, ctx, args):
        result = await ox.internal_call("entries", "en-gb", args)
        await ctx.send(str(result))

def setup(bot):
    bot.add_cog(Dictionary(bot))