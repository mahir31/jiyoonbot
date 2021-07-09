from discord.ext import commands
import discord
from discord.ext.commands import bot
from tools import utilities as util
import aiohttp
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
import random

class Sundry(commands.Cog):
    """sundry commands"""

    def __init__(self, bot):
        self.bot = bot
        self.fortune = open('fortunes/fortunes', 'r', encoding='utf8').read().split('%')
        self.colour = '53e9f1'
        self.pat = [
            "(；^＿^)ッ☆(　゜o゜)",
            "( ^ ᗜ ^ )ノ”(◉⩊◉)",
            "ﾅﾃﾞ(　^_^)ﾉ(´･ω･`)ﾅﾃﾞ"
        ]
        self.sparkles = [
            "✧･✧",
            "*✿❀",
            "⋆ₓₒ",
        ]

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
        """performs ping test"""
        try:
            response = await ctx.send('\N{EYES}')
            await response.delete()
            await ctx.send(
                embed=discord.Embed( 
                    description=f"```API Response: {(self.bot.latency * 1000):.2f} ms" + 
                    f"\nCommand Response: {(response.created_at - ctx.message.created_at).total_seconds() * 1000} ms```", 
                    color=int('ffdd38', 16)
                )
            )
        except Exception as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
    
    @commands.command()
    async def fortune(self, ctx):
        """get a fortune cookie!"""
        x = random.randint(0, len(self.fortune))
        content = discord.Embed(
            color=int(self.colour, 16),
            description=self.fortune[x]
        )
        content.set_footer(text=f'fortune cookie: #{x}')
        await ctx.send(embed=content)



    @commands.command(aliases=["inv"])
    async def invite(self, ctx):
        content = discord.Embed(
            colour=int(self.colour, 16), 
            description="Click [here](https://discord.com/api/oauth2/authorize?client_id=763475902339350608&permissions=388160&redirect_uri=https%3A%2F%2Fjiyoonbot.xyz%2Fcallback%2Fsp%2F&scope=bot) to invite Jiyoon Bot to your server!",
            )
        content.set_author(
            name="Server invitation",
            url='https://discord.com/api/oauth2/authorize?client_id=763475902339350608&permissions=388160&redirect_uri=https%3A%2F%2Fjiyoonbot.xyz%2Fcallback%2Fsp%2F&scope=bot',
            icon_url='https://cdn3.iconfinder.com/data/icons/popular-services-brands-vol-2/512/discord-512.png'
        )
        await ctx.send(embed=content)
    
    @commands.command()
    async def pat(self, ctx, args):
        try:
            sparkle = random.choice(self.sparkles)
            await ctx.send(f"{args} \\{sparkle} {random.choice(self.pat)} {sparkle[::-1]}")
        except Exception as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
    
    @commands.command()
    async def roll(self, ctx, *args,):
        """rolls polyhedral dice. standard dice apply: d20, d12, d8, d8, d6, d4
        specify number and then dice, separate arguments with space.
        e.g. 1d6 2d20"""
        message = await ctx.send("\N{game die} Rolling Dice \N{game die}")
        total = 0
        for i in list(args):
            try:
                x = i.split("d")
                rolls = int(x[0])
                dice = int(x[1])
                if dice in [20, 12, 8, 6, 4]:
                    for i in range(rolls):
                        total += random.randint(1, dice)
                else:
                    await ctx.send(f"invalid dice {dice}, valid dice d20, d12, d8, d6, d4")
                    break
            except ValueError:
                await message.delete()
        await message.edit(content=f"\N{game die} **You rolled: {total}** \N{game die}")

def setup(bot):
    bot.add_cog(Sundry(bot))