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
    async def test(self, ctx):
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
            pages = utils.paginator(tracks, 'track names')
        index=0
        page = await ctx.send(embed=pages[index])
        await page.add_reaction('◀️')
        await page.add_reaction('▶️')
        while True:
            try:
                reaction = await self.bot.wait_for('raw_reaction_add', timeout=60, check=self.event_check)
                if str(reaction.emoji) == '◀️':
                    if index == 0:
                        continue
                    index -= 1
                    await page.edit(embed=pages[index])
                if str(reaction.emoji) == '▶️':
                    if index == len(pages) - 1:
                        continue
                    index += 1
                    await page.edit(embed=pages[index])
            except asyncio.exceptions.TimeoutError:
                return
        
    def event_check(self, payload):
        if payload.user_id == self.bot.user.id:
            return False
        return True


def setup(bot):
    bot.add_cog(test(bot))