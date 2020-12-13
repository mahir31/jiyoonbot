import discord
from discord.ext import commands
from tools import utilities as utils
import logging
import asyncio


class test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('cog: test.py connected')
    
    # commands

    @commands.command()
    async def p(self, ctx):
        '''test for pagination'''
        
        tracks = ["I'll Take Half Of Your Sorrows Today", 
            'We Need To Be Careful To Love', 
            'Rose', 
            'A Beginner In Society', 
            "I'll Take Half Of Your Sorrows Today", 
            'Some Flowers', 
            'Look Like You Have A Natural Bent', 
            '魅力とは?', 
            '甘い誘惑', 
            'And July', 
            'More (Feat. Giriboy)', 
            'under the ground', 
            'GOTTASADAE', 
            'DDING (Prod. By GIRIBOY)', 
            'LEGACY', 
            'Nerdy Love', 
            'Weather', 
            'Feel Good (SECRET CODE)', 
            'Voice', 
            'Zig Zag']
        if tracks:
            await utils.paginate(ctx, tracks, 'track list: ')


def setup(bot):
    bot.add_cog(test(bot))