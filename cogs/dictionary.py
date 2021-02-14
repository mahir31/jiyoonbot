import discord
from discord.ext import commands
import logging
from tools import ox_requests as ox
import json

class Dictionary(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('cog: dictionary.py connected')

    # commands
    @commands.group(case_insensitive=True)
    async def dc(self, ctx):
        '''Dictionary commands'''

    @dc.command(aliases=["df"])
    async def define(self, ctx, args):
        result = await ox.internal_call('entries', 'en-gb', args)
        if 'error' in result:
            await ctx.send('it work big pog')
        else:
            result = result['results'][0]['lexicalEntries'][0]
            definitions = '\n'.join([definitions['definitions'][0] for definitions in result['entries'][0]['senses']])
            synonyms = ', '.join(synonyms['text'] for synonyms in result['entries'][0]['senses'][0]['synonyms'])
            audiofile = result['entries'][0]['pronunciations'][0]['audioFile']
            await ctx.send(definitions)
            await ctx.send(synonyms)
            await ctx.send(audiofile)

def setup(bot):
    bot.add_cog(Dictionary(bot))