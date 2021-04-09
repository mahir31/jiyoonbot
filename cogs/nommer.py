from discord.ext import commands
import discord
from data import database as db
from datetime import datetime, timedelta
import random
from tools import utilities as util
from dataclasses import dataclass

@dataclass
class Nommer:
    """class for keeping track of data in nommer object"""
    nommer_id : int
    last_grabbed : float
    total_cookies :int
    total_cookies_grabbed : int
    total_cookies_gifted : int
    total_grab_attempts : int
    total_cookies_received :int

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
        if not nommer:
            nommer = db.grab_cookies(ctx.author.id, datetime.timestamp(datetime.now() - timedelta(hours = 7)), 0, 0, 0, 0, 0)
        if self.cooldown_calc(db.nommer_exists(ctx.author.id)[1]) < 0:
            if user is None:
                await self.cookie_types[random.choices(list(self.cookie_types.keys()), self.weights)[0]](ctx, ctx.author.id, None)
            else:
                await self.cookie_types[random.choices(list(self.cookie_types.keys()), self.weights)[0]](ctx, ctx.author.id, user.id)
        else:
            await ctx.send(f'too early, try again in {util.stringfromtimestamp(self.cooldown_calc(db.nommer_exists(ctx.author.id)[1]))}')

    def cooldown_calc(self, last_time):
        cooldown = 21600
        time_difference = datetime.timestamp(datetime.now()) - last_time
        time_difference = cooldown - time_difference
        return time_difference

    async def empty(self, ctx, gifter_id, giftee_id):
        await self.cookies_sorter(ctx, Nommer(*db.nommer_exists(gifter_id)), giftee_id, 0)

    async def one(self, ctx, gifter_id, giftee_id):
        await self.cookies_sorter(ctx, Nommer(*db.nommer_exists(gifter_id)), giftee_id, 1)

    async def some(self, ctx, gifter_id, giftee_id):
        await self.cookies_sorter(ctx, Nommer(*db.nommer_exists(gifter_id)), giftee_id, random.randint(2, 20))

    async def nom(self, ctx, gifter_id, giftee_id):
        await self.cookies_sorter(ctx, Nommer(*db.nommer_exists(gifter_id)), giftee_id, random.randint(21, 60))
    
    async def cookies_sorter(self, ctx, nommer, giftee_id, increment):
        giftee = db.nommer_exists(giftee_id)
        if giftee_id:
            db.grab_cookies(
                nommer.nommer_id,
                datetime.timestamp(datetime.now()),
                nommer.total_cookies,
                nommer.total_cookies_grabbed + increment,
                nommer.total_cookies_gifted + increment,
                nommer.total_grab_attempts + 1,
                nommer.total_cookies_received
            )
            if giftee:
                giftee = Nommer(*giftee)
                db.grab_cookies(
                    giftee.nommer_id,
                    giftee.last_grabbed,
                    giftee.total_cookies + increment,
                    giftee.total_cookies_grabbed,
                    giftee.total_cookies_gifted,
                    giftee.total_grab_attempts,
                    giftee.total_cookies_received + increment
                )
            else:
                db.grab_cookies(giftee_id, datetime.timestamp(datetime.now() - timedelta(hours = 6)), increment, 0, 0, 0, increment)
            if increment == 0:
                await ctx.send(f"{util.displayname(await self.bot.fetch_user(ctx.author.id))} went to grab some cookies but didn't get any\N{Broken Heart}")
            else:
                await ctx.send(f'\N{Cookie}{util.displayname(await self.bot.fetch_user(ctx.author.id))} grabbed {increment} cookie(s) and gifted it to {util.displayname(await self.bot.fetch_user(giftee_id))}\N{Sparkling Heart}')
        else:
            db.grab_cookies(
                nommer.nommer_id, 
                datetime.timestamp(datetime.now()), 
                nommer.total_cookies + increment, 
                nommer.total_cookies_grabbed + increment, 
                nommer.total_cookies_gifted,
                nommer.total_grab_attempts + increment,
                nommer.total_cookies_received
            )
            if increment == 0:
                await ctx.send(f"{util.displayname(await self.bot.fetch_user(ctx.author.id))} went to grab some cookies but didn't get any\N{Broken Heart}")
            else:
                await ctx.send(f'\N{Cookie}{util.displayname(await self.bot.fetch_user(ctx.author.id))} grabbed {increment} cookie(s)\N{Sparkling Heart}')
    
def setup(bot):
    bot.add_cog(Cookies(bot))