import discord
from discord.ext import commands
from data import database as db
import logging
import datetime
from datetime import datetime
import random
import asyncio

class fish(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: fishing.py connected")
    
    @commands.group(case_insensitive=True)
    async def fs(self, ctx):
        '''
        Fishing Commands:
        '''
    
    @fs.command()
    async def go(self, ctx):
        fisher = db.fisher_exists(ctx.author.id)
        if fisher:
            fisher_id, times_fished, total_fish, time_stamp, exp_points, coins = fisher[0]
            await ctx.send(f'fisher id: {fisher_id}, times fished: {times_fished}, total fish: {total_fish}, timestamp: {time_stamp}, exp points: {exp_points}, coins: {coins}')
        else:
            await self.go_fishing(ctx)

    async def go_fishing(self, ctx):
        catch = random.randint(0, 1)
        if bool(catch) == True:
            await ctx.send('Something is on the line, type "catch" to reel it in!')
            try:
                response = await self.bot.wait_for('message', check=self.catch_check, timeout=15)
                if response:
                    catch = random.randint(0, 1)
                    if bool(catch) == True:
                        await ctx.send('Congratulations you caught 1 fish and gained 8 experience points!')
                    else:
                        await ctx.send('You tried your hardest to reel it in but the fish slipped away, better luck next time.')
            except asyncio.TimeoutError:
                await ctx.send('Oops, the fish escaped before you could reel it in')
        else:
            await ctx.send('You cast your reel, but sadly no fish took the bait, try again later')

    def catch_check(ctx, payload):
        return payload.content == 'catch'

def setup(bot):
    bot.add_cog(fish(bot))