import discord
from discord.ext import commands
import logging
from PyDictionary import PyDictionary

dic = PyDictionary()

class Dictionary(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: dictionary.py connected")

    # commands

    @commands.group(case_insensitive=True)
    async def dc(self, ctx):
        '''Dictionary commands'''
    
    @dc.command(aliases=["df"])
    async def define(self, ctx, args):
        '''type a word to find the definition'''
        smth = dic.meaning(args)
        await ctx.send(str(smth))
    
    @dc.command(aliasess=["an"])
    async def antonym(self, ctx, args):
        '''type a word to find words with the opposing definitions'''
        smth = dic.antonym(args)
        await ctx.send(str(smth))
    
    @dc.command(aliases=["sy"])
    async def synonym(self, ctx, args):
        '''type a word to find similar words'''
        smth = dic.synonym(args)
        await ctx.send(str(smth))

def setup(bot):
    bot.add_cog(Dictionary(bot))