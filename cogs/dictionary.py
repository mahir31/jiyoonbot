import discord
from discord import colour
from discord.embeds import Embed
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
            await self.extraction_and_send(ctx, result)

    # helper functions

    async def extraction_and_send(self, ctx, data):
        total_entries = []
        content = discord.Embed(colour = discord.Colour.from_rgb(0, 189, 242))
        content.description = ''

        for entry in data['results'][0]['lexicalEntries']:
            definitions_value = ''
            name = data['results'][0]['word']
        
        for i in range(len(entry['entries'][0]['senses'])):
            for definition in entry['entries'][0]['senses'][i].get('definitions', []):
                top_definition = f'\n**{i + 1}.** {definition}'
                if len(definitions_value + top_definition) > 1024:
                    break
                definitions_value += top_definition
                try:
                    for y in range(len(entry['entries'][0]['senses'][i]['examples'])):
                        for example in entry['entries'][0]['senses'][i]['examples']:
                            example = f'\n> {example["text"]}'
                            if len(definitions_value + example) > 1024:
                               break
                            definitions_value += example
                    definitions_value += '\n'
                except KeyError:
                    pass
        word_type = entry['lexicalCategory']['text']
        current_entry = {
            'id': name,
            'definitions': definitions_value,
            'type': word_type, 
        }
        total_entries.append(current_entry)
        content.set_author(name=total_entries[0]['id'], icon_url='https://i.imgur.com/vDvSmF3.png')

        for entry in total_entries:
            content.add_field(name=f'{entry["type"]}', value=entry['definitions'], inline=False)
        await ctx.send(embed=content)

def setup(bot):
    bot.add_cog(Dictionary(bot))