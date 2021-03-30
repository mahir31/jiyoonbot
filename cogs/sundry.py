from discord.ext import commands
import discord
from discord.ext.commands import bot

class Sundry(commands.Cog):
    """sundry commands"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(hidden=True)
    async def clear(self, ctx, limit=2):
        """clears messages in current channel, limit by default 2, can be specified"""
        await ctx.message.channel.purge(limit=int(limit)+1)
        await ctx.send('confirm', delete_after=5)

def setup(bot):
    bot.add_cog(Sundry(bot))