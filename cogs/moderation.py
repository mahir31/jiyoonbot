import discord 
from discord.ext import commands

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
    async def embed(self, ctx, title=None, description=None, url=None, embed_colour="#ffdd38", footer=None, image=None, thumbnail=None):
        content = discord.Embed(colour=embed_colour)
        await ctx.send(embed=content)

def setup(bot):
    bot.add_cog(Moderation(bot))