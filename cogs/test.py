import discord
from discord.ext import commands
from tools import utilities as utils
import logging

LEFT_EMOJI = '\u2B05'
RIGHT_EMOJI = '\u27A1'

class test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('cog: test.py connected')
    
    # commands

    @commands.command()
    async def paginate(self, ctx):
        '''test for pagination'''
        tracks = ['Rest', 
            'Intro', 
            'London', 
            'Square (2017)', 
            'Point (feat. Loopy)', 
            'True lover', 
            'Amy', 
            'Newsong2', 
            'Not a girl', 
            'Datoom', 
            'Berlin', 
            '0310', 
            'Bunny', 
            'lovelovelove', 
            'Mr.gloomy', 
            'Meant to be', 
            'can i b u', 
            'Popo (How deep is our love?)']
        if tracks:
            pages = utils.paginator(tracks, 'page test')
        page = await ctx.send(embed=pages[0])
        await page.add_reaction(LEFT_EMOJI)
        await page.add_reaction(RIGHT_EMOJI)


def setup(bot):
    bot.add_cog(test(bot))