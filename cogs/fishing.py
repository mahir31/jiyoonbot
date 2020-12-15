import discord
from discord.ext import commands
from data import database as db
import logging
import datetime
from datetime import datetime

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
            await ctx.send(f'{fisher_id}, {times_fished}, {total_fish}, {time_stamp}, {exp_points}')
        else:
            db.go_fish(ctx.author.id, 1, 1, datetime.timestamp(datetime.now()), 8)
            await ctx.send('job done')

def setup(bot):
    bot.add_cog(fish(bot))