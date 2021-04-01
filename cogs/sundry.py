from discord.ext import commands
import discord
from discord.ext.commands import bot
from tools import utilities as util
import aiohttp
from PIL import Image
from io import BytesIO
from requests import get

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
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{user.avatar_url}') as response:
                data = {
                    'format' : response.headers['Content-Type'],
                    'last-modified': response.headers['Last-Modified'],
                    'url': response.real_url
                }
                image_bytes = await response.read()
                image = Image.open(BytesIO(image_bytes))
                width, height = image.size
                await ctx.send(f'{width}, {height}')

def setup(bot):
    bot.add_cog(Sundry(bot))