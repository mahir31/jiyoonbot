import discord
from discord.ext import commands
import logging
from tools import utilities as util

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
        content.description = '''Name: Jiyoon Bot\nVersion: 1.02\nDeveloper: doublesocks#3034'''
        await ctx.send(embed=content)

    @commands.command(aliases=["dp", "pfp"])
    async def displaypicture(self, ctx, user: discord.User = None):
        """display user's profile picture"""
        if user is None:
            user = ctx.author

        content = discord.Embed()
        content.set_author(name=str(user), url=user.avatar_url)
        content.set_image(url=user.avatar_url)
        await ctx.send(embed=content)

def setup(bot):
    bot.add_cog(misc(bot))