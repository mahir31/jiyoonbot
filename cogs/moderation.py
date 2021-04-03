import discord 
from discord.ext import commands
from tools import utilities as util
import argparse

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
    async def embed(self, ctx, *, args):
        """sends embed in channel"""
        try:
            await ctx.send('job done')
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
    
    @commands.command()
    async def parse(self, ctx, *, args):
        for x in args.split(' | '):
            for y in [x.split(' = ')]:
                await ctx.send(y.pop(0))
                await ctx.send(' '.join(y))


def setup(bot):
    bot.add_cog(Moderation(bot))