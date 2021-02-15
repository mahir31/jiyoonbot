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
            await self.extraction_and_send(ctx, result['results'][0]['lexicalEntries'][0])

    # helper functions

    async def extraction_and_send(self, ctx, entry):
        definitions = '\n'.join([definitions['definitions'][0] for definitions in entry['entries'][0]['senses']])
        await ctx.send(definitions)
        try:
            synonyms = ', '.join(synonyms['text'] for synonyms in entry['entries'][0]['senses'][0]['synonyms'])
            await ctx.send(synonyms)
        except KeyError:
            logging.info('no synonyms were found')
        audiofile = entry['entries'][0]['pronunciations'][0]['audioFile']
        await ctx.send(audiofile)

def setup(bot):
    bot.add_cog(Dictionary(bot))