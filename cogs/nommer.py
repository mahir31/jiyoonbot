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
    
    @commands.command(aliases=['biscuit'])
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
                await ctx.send(f"{util.displayname(await self.bot.fetch_user(ctx.author.id))} went to grab some cookies but didn't get any \N{Broken Heart}")
            else:
                await ctx.send(f'{util.displayname(await self.bot.fetch_user(ctx.author.id))} grabbed {increment} \N{Cookie} and gifted {("it" if increment == 1 else "them")} to {util.displayname(await self.bot.fetch_user(giftee_id))} \N{Sparkling Heart}')
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
                await ctx.send(f"{util.displayname(await self.bot.fetch_user(ctx.author.id))} went to grab some cookies but didn't get any \N{Broken Heart}")
            else:
                await ctx.send(f'\N{Sparkles} {util.displayname(await self.bot.fetch_user(ctx.author.id))} grabbed {increment} \N{Cookie}')
    
    @commands.command()
    async def cookiejar(self, ctx, user : discord.User = None):
        try:
            if user is None:
                user = ctx.author
            nommer = db.nommer_exists(user.id)
            if nommer:
                nommer = Nommer(*nommer)
                content = discord.Embed(
                    colour=int('eee0b1', 16), 
                    title=f"\N{Cookie} {util.displayname(user)}'s cookie jar!")
                content.description = '\n'.join(
                    [
                        f'\N{Sparkles} Total Cookies: {nommer.total_cookies}',
                        f'\N{Person Raising Both Hands in Celebration} Total Cookies Grabbed: {nommer.total_cookies_grabbed}',
                        f'\N{Wrapped Present} Total Cookies Gifted: {nommer.total_cookies_gifted}',
                        f'\N{Clapping Hands Sign} Total Grab Attempts: {nommer.total_grab_attempts}',
                        f'\N{Red Gift Envelope} Total Cookies Received: {nommer.total_cookies_received}',
                        f'\N{Timer Clock} Last Grabbed: {("Never" if nommer.total_cookies_grabbed == 0 else util.stringfromtimestamp((datetime.now() - datetime.fromtimestamp(nommer.last_grabbed)).seconds))}'
                    ]
                )
                await ctx.send(embed=content)
            else:
                await ctx.send(f"{util.displayname(user)} has no cookies in their cookiejar")
        except Exception as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")
    
    @commands.command(aliases=['bt'])
    async def bakingtimer(self, ctx, user: discord.User = None):
        try:
            if user is None:
                user = ctx.author
            nommer = db.nommer_exists(user.id)
            if nommer:
                nommer = Nommer(*nommer)
                nommer = self.cooldown_calc(nommer.last_grabbed)
                if nommer < 0:
                    await ctx.send("Fresh cookies are ready! Grab 'em while they're hot! \N{Fire}")
                else:
                    await ctx.send(f"\N{Timer Clock} Cookies are still in the oven, they'll be ready in {util.stringfromtimestamp(nommer)}")
            else:
                await ctx.send("Fresh cookies are ready! Grab 'em while they're hot! \N{Fire}")
        except Exception as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

def setup(bot):
    bot.add_cog(Cookies(bot))