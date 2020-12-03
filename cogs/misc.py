import discord
import logging
from discord.ext import commands
from discord import Spotify

class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: misc.py connected")

    @commands.command()
    async def spt(self, ctx):
        '''activity test'''
        user = ctx.author
        if isinstance(user, discord.Member):
            username = user.nick or user.display_name
        for activity in user.activities:
            if isinstance(activity, Spotify):
                content = discord.Embed()
                content.color = activity.color
                content.description = activity.album
                content.title = activity.title
                content.set_thumbnail(url=activity.album_cover_url)
                content.set_author(name=username + " is now playing", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=content)

def setup(bot):
    bot.add_cog(misc(bot))