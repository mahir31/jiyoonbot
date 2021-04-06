from discord.ext import commands
import discord
from discord.ext.commands import bot
from tools import utilities as util
import aiohttp
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
from data import database as db
from datetime import datetime, timedelta

class Sundry(commands.Cog):
    """sundry commands"""

    def __init__(self, bot):
        self.bot = bot
        self.cookie_types = {
            "none" : self.none,
            "one" : self.one,
            "some" : self.some,
            "nom" : self.nom
        }
        self.weights = [10, 50, 30, 10]
        
    
    @commands.command(aliases=["av", "dp"])
    async def avatar(self, ctx, user : discord.User = None):
        """sends the avatar for self or mentioned user."""
        if user is None:
            user = ctx.author
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{user.avatar_url}') as response:
                data = {
                    'format' : response.headers['Content-Type'],
                    'last-modified': response.headers['Last-Modified'],
                    'url': response.url
                }
                image_bytes = await response.read()
                width, height = Image.open(BytesIO(image_bytes)).size
        content = discord.Embed(colour=int(util.rgb_to_hex(ColorThief(BytesIO(image_bytes)).get_color(quality=1)), 16))
        content.set_author(name=user)
        content.set_image(url=user.avatar_url)
        content.set_footer(text=f"Type: {data['format']} | Size: {width}x{height} | Last Modified: {data['last-modified'][:-17]}")
        await ctx.send(embed=content)
    
    @commands.command()
    async def cookie(self, ctx, user : discord.User = None):
        """gifts cookies to mentioned users"""
        nommer = db.nommer_exists(ctx.author)
        if nommer:
            if user is None:
                

def setup(bot):
    bot.add_cog(Sundry(bot))