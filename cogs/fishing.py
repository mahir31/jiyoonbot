import discord
from discord.ext import commands
from data import database as db
import logging
import datetime
from datetime import datetime
import random

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
            fisher_id, times_fished, total_fish, time_stamp, exp_points = fisher[0]
            await ctx.send(f'fisher id: {fisher_id}, times fished: {times_fished}, total fish: {total_fish}, timestamp: {time_stamp}, exp points: {exp_points}')
        else:
            catch = self.go_fishing()
            if bool(catch) == True:
                db.go_fish(ctx.author.id, 1, catch, datetime.timestamp(datetime.now()), 8)
                await ctx.send(f'congratulations you caught {catch} fish')
            else:
                db.go_fish(ctx.author.id, 1, catch, datetime.timestamp(datetime.now()), 0)
                await ctx.send('unfortunately you did not catch anything')

    def go_fishing(self):
        catch = random.randint(0, 1)
        return catch

def setup(bot):
    bot.add_cog(fish(bot))