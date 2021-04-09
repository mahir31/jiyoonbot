from zlib import decompress
from discord.ext import commands
import discord
from discord.ext.commands import bot
from tools import utilities as util
import aiohttp
from PIL import Image
from io import BytesIO
from colorthief import ColorThief


class Sundry(commands.Cog):
    """sundry commands"""

    def __init__(self, bot):
        self.bot = bot

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
    async def ping(self, ctx):
        try:
            await ctx.send(embed=discord.Embed(description=f"Ping: **{round(self.bot.latency *1000)}** milliseconds!", color=int('ffdd38', 16)))
        except Exception as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')

def setup(bot):
    bot.add_cog(Sundry(bot))