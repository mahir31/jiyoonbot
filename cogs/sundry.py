from discord.ext import commands
import discord
from discord.ext.commands import bot
from tools import utilities as util
import aiohttp
from PIL import Image

class Sundry(commands.Cog):
    """sundry commands"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def clear(self, ctx, limit=2):
        """clears messages in current channel, limit by default 2, can be specified"""
        await ctx.message.channel.purge(limit=int(limit)+1)
        await ctx.send('\N{Eyes}', delete_after=5)
    
    @commands.command()
    async def avatar(self, ctx, user : discord.User = None):
        if user is None:
            user = ctx.author
        await ctx.send(user.avatar_url)

def setup(bot):
    bot.add_cog(Sundry(bot))