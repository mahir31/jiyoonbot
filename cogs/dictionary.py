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
        content = discord.Embed(colour = discord.Colour.from_rgb(128, 0, 0))
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
                        for example in entry['entries'][0]['senses'][i]['examples']:
                            example = f'\n> _example:_ {example["text"]}'
                            if len(definitions_value + example) > 1024:
                                break
                            definitions_value += example
                        definitions_value += '\n'
                    except KeyError:
                        pass
            try:
                synonyms = ', '.join(x['text'] for x in entry['entries'][0]['senses'][0]['synonyms'])
            except KeyError:
                synonyms = None            
            try:
                audiofile = entry['entries'][0]['pronunciations'][0]['audioFile']
            
            except KeyError:
                pass
            
            for reference in entry['entries'][0]['senses'][i].get('crossReferenceMarkers', []):
                definitions_value += reference
            
            word_type = entry['lexicalCategory']['text']
            current_entry = {
                'id': name,
                'definitions': definitions_value,
                'type': word_type, 
            }
            total_entries.append(current_entry)
        
        for entry in total_entries:
            content.add_field(name=f'{entry["type"]}', value=f"{entry['definitions']}", inline=False)
        
        if synonyms:
            content.add_field(name="Similar:", value=f"{synonyms}", inline=False)

        content.set_author(name=f"📚{total_entries[0]['id']}", url=audiofile)
        content.set_footer(text="Definitions provided by Oxford Dictionary", icon_url="https://i.imgur.com/vDvSmF3.png")

        await ctx.send(embed=content)

def setup(bot):
    bot.add_cog(Dictionary(bot))