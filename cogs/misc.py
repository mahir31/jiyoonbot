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

    @commands.command(aliases=["dp", "pfp", "av"])
    async def displaypicture(self, ctx, user: discord.User = None):
        """display user's profile picture"""
        if user is None:
            user = ctx.author

        content = discord.Embed()
        content.set_author(name=str(user), url=user.avatar_url)
        content.set_image(url=user.avatar_url)
        await ctx.send(embed=content)

    @commands.command()
    async def delete(self, ctx, limit):
        """Deletes messages in a channel, number of messages subject to user input"""
        channel = ctx.message.channel
        await channel.purge(limit=int(limit) + 1)

def setup(bot):
    bot.add_cog(misc(bot))