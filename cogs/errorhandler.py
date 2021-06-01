import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    """ any errors not caught will bubble here """

    def __init__(self, bot):
        self.bot = bot
        self.colour = int('ff0f0f', 16)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """ events that trigger error handler """
        try:
            error = getattr(error, 'original', error)

            if isinstance(error, commands.CommandNotFound):
                return

            await ctx.send(
                embed=discord.Embed(
                    colour=self.colour,
                    description=f'\N{Cross Mark} {error.__class__.__name__}: {error}'
                )
            )
        except Exception as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
