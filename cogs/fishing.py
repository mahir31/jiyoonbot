import discord
from discord.ext import commands
from data import database as db


class fish(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: fishing.py connected")
    
    @command.group(case_insensitive=True)
    async def fs(ctx, self):
        '''
        Fishing Commands:
        '''
        if ctx.invoked_subcommand is None:
            pass
    
    @fs.command()
    async def go(ctx, self)

def setup(bot):
    bot.add_cog(fish(bot))