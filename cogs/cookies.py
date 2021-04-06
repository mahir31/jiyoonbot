from discord.ext import commands
import discord
from data import database as db
from datetime import datetime, timedelta
import random
from tools import utilities as util

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
                    await self.cookie_types['one'](ctx, nommer, None)
                else:
                    # grab = random.choices(list(self.cookie_types.keys()), self.weights)[0]
                    await self.cookie_types['one'](ctx, nommer, user)
            else:
                await ctx.send('too early bro')
    
    def cooldown_calc(self, last_time):
        cooldown = 21600
        time_difference = datetime.timestamp(datetime.now()) - last_time
        time_difference = cooldown - time_difference
        return time_difference

    async def empty(self, ctx, gifter, giftee):
        await ctx.send('function works')

    async def one(self, ctx, gifter, giftee):
        nommer_id, last_grabbed, total_cookies, total_cookies_grabbed, total_cookies_gifted, total_grab_attempts, total_cookies_received = gifter
        if giftee:
            db.grab_cookies(nommer_id, datetime.timestamp(datetime.now()), total_cookies, total_cookies_grabbed + 1, total_cookies_gifted + 1, total_grab_attempts + 1, total_cookies_received)
            data = db.nommer_exists(giftee.id)
            if data:
                nommer_id, last_grabbed, total_cookies, total_cookies_grabbed, total_cookies_gifted, total_grab_attempts, total_cookies_received = data
                db.grab_cookies(giftee.id, last_grabbed, total_cookies + 1, total_cookies_grabbed, total_cookies_gifted, total_grab_attempts, total_cookies_received + 1)
            else:
                db.grab_cookies(giftee.id, datetime.timestamp(datetime.now() - timedelta(hours = 6)), 1, 0, 0, 0, 1)
            await ctx.send(f'\N{Cookie}{util.displayname(await self.bot.fetch_user(nommer_id))} grabbed one cookie and gifted it to {util.displayname(await self.bot.fetch_user(giftee.id))}\N{Sparkling Heart}')
        else:
            db.grab_cookies(nommer_id, datetime.timestamp(datetime.now()), total_cookies + 1, total_cookies_grabbed + 1, total_cookies_gifted, total_grab_attempts + 1, total_cookies_received)
            await ctx.send(f'\N{Cookie}{util.displayname(await self.bot.fetch_user(nommer_id))} grabbed one cookie\N{Sparkling Heart}')

    async def some(self, ctx, gifter, giftee):
        await ctx.send('function works')

    async def nom(self, ctx, gifter, giftee):
        await ctx.send('function works')

def setup(bot):
    bot.add_cog(Cookies(bot))