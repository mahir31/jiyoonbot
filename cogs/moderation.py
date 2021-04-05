import discord 
from discord.ext import commands
from tools import utilities as util

class Moderation(commands.Cog):
    """commands to moderate servers"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, limit=2):
        try:
            """clears messages in current channel, limit by default 2, can be specified"""
            await ctx.message.channel.purge(limit=int(limit)+1)
            await ctx.send('\N{Eyes}', delete_after=5)
        except Exception as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
                    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def embed(self, ctx, channel : discord.TextChannel, *, args):
        """
        Sends embed in channel. 
        Use the following example:
            >embed #channel title = none | description = none | colour = none
        Include all tags. 
        Tags with 'none' will be ignored.
        Unsupported tags will be ignored.
        """
        parsed_dict = {}
        try:
            for x in args.split('|'):
                for y in [x.split('=')]:
                    parsed_dict.update({y.pop(0).strip() : ''.join(y).strip()})
            for data in parsed_dict:
                if parsed_dict[data] == '':
                    await ctx.send(f'argument: "_{data}_" has no value - Verify that all tags have values')
                    break
            parsed_dict = {key:val for key, val in parsed_dict.items() if not val == 'none'}
        except Exception as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
    
    @commands.command() 
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, channel : discord.TextChannel, *, args):
        """sends mesasge in specified channel"""
        try:
            await channel.send(str(args))
            await ctx.send('\N{Thumbs Up Sign} Message has been sent to specified channel. This notification will be removed soon', delete_after=5)
        except Exception as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')

def setup(bot):
    bot.add_cog(Moderation(bot))