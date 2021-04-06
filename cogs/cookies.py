from discord.ext import commands
import discord
from data import database as db
from datetime import datetime
import random

class Cookies(commands.Cog):
    """cookie commands"""

    def __init__(self, bot):
        self.bot = bot
        self.cookie_types = {
            "empty" : self.empty,
            "one"   : self.one,
            "some"  : self.some,
            "nom"   : self.nom
        }
        self.weights = [10, 50, 30, 10]

    
    @commands.command()
    async def cookie(self, ctx, user : discord.User = None):
        """gifts cookies to mentioned users"""
        nommer = db.nommer_exists(ctx.author.id)
        if nommer:
            if not self.cooldown_calc(nommer[1]) < 0:
                if user is None:
                    pass
                else:
                    grab = random.choices(list(self.cookie_types.keys()), self.weights)[0]
                    await self.cookie_types[grab](ctx, ctx.author, user)
            else:
                await ctx.send('too early bro')
    
    def cooldown_calc(self, last_time):
        cooldown = 21600
        time_difference = datetime.timestamp(datetime.now()) - last_time
        time_difference = cooldown - time_difference
        return time_difference

    async def empty(self, ctx):
        pass

    async def one(self, ctx, gifter, giftee):
        pass

    async def some(self, ctx):
        pass

    async def nom(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Cookies(bot))