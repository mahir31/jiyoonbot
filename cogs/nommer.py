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
        if not nommer:
            nommer = await self.instantiate_nommer(ctx, ctx.author.id)
        if self.cooldown_calc(db.nommer_exists(ctx.author.id)[1]) < 0:
            if user is None:
                grab = random.choices(list(self.cookie_types.keys()), self.weights)[0]
                await self.cookie_types['one'](ctx, ctx.author.id, None)
            else:
                grab = random.choices(list(self.cookie_types.keys()), self.weights)[0]
                await self.cookie_types['one'](ctx, ctx.author.id, user.id)
        else:
            await ctx.send('too early bro')

    def cooldown_calc(self, last_time):
        cooldown = 21600
        time_difference = datetime.timestamp(datetime.now()) - last_time
        time_difference = cooldown - time_difference
        return time_difference

    async def empty(self, ctx, gifter, giftee):
        await ctx.send('function works')

    async def one(self, ctx, gifter_id, giftee_id):
        if not gifter_id:
            await self.cookies_sorter(ctx, await self.get_nommer_info(ctx, db.nommer_exists(gifter_id)), None, 1)
        else:
            await self.cookies_sorter(ctx, await self.get_nommer_info(ctx, db.nommer_exists(gifter_id)), giftee_id, 1)

    async def some(self, ctx, gifter, giftee):
        await ctx.send('function works')

    async def nom(self, ctx, gifter, giftee):
        await ctx.send('function works')
    
    async def get_nommer_info(self, ctx, nommer):
        (
            nommer_id, 
            last_grabbed, 
            total_cookies, 
            total_cookies_grabbed, 
            total_cookies_gifted, 
            total_grab_attempts, 
            total_cookies_received
        ) = nommer
        return nommer
    
    async def cookies_sorter(self, ctx, nommer, giftee_id, increment):
        if giftee_id:
            db.grab_cookies(
                nommer[0],
                datetime.timestamp(datetime.now()),
                nommer[2],
                nommer[3] + increment,
                nommer[4] + increment,
                nommer[5] + 1,
                nommer[6]
            )
            giftee = db.nommer_exists(giftee_id)
            if giftee:
                db.grab_cookies(
                    giftee[0],
                    giftee[1],
                    giftee[2] + increment,
                    giftee[3],
                    giftee[4],
                    giftee[5],
                    giftee[6] + increment
                )
            else:
                db.grab_cookies(
                    giftee_id, 
                    datetime.timestamp(datetime.now() - timedelta(hours = 6)), 
                    increment, 
                    0, 
                    0, 
                    0, 
                    increment
                )
            await ctx.send(f'\N{Cookie}{util.displayname(await self.bot.fetch_user(nommer[0]))} grabbed {increment} cookie(s) and gifted it to {util.displayname(await self.bot.fetch_user(giftee_id))}\N{Sparkling Heart}')
        else:
            db.grab_cookies(
                nommer[0], 
                datetime.timestamp(datetime.now()), 
                nommer[2] + increment, 
                nommer[3] + increment, 
                nommer[4], 
                nommer[5] + increment,
                nommer[6]
            )
            await ctx.send(f'\N{Cookie}{util.displayname(await self.bot.fetch_user(nommer[0]))} grabbed {increment} cookie(s)\N{Sparkling Heart}')
    
    async def instantiate_nommer(self, ctx, nommer_id):
        db.grab_cookies(nommer_id, datetime.timestamp(datetime.now() - timedelta(hours = 7)), 0, 0, 0, 0, 0)
        return

def setup(bot):
    bot.add_cog(Cookies(bot))