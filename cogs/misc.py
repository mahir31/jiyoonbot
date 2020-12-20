import discord
from discord.ext import commands
import logging

colour = int('4eca58', 16)

class misc(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('cog: misc.py connected')
    
    # commands

    @commands.command()
    async def about(self, ctx):
        '''Bot information'''
        content = discord.Embed(title='About:', colour=colour)
        content.description = '''Name: Jiyoon Bot
        Version: 1.02
        Developer: doublesocks#3034'''
        await ctx.send(embed=content)

def setup(bot):
    bot.add_cog(misc(bot))