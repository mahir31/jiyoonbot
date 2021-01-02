import discord
from discord.ext import commands
from data import database as db
import logging
from datetime import datetime, timedelta
import random
import asyncio
from tools import utilities as util

colour = 'add8e6'

class fish(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: fishing.py connected")
    
    # commands
    
    @commands.group(case_insensitive=True)
    async def fs(self, ctx):
        '''Fishing Commands:'''
        
        if ctx.invoked_subcommand is None:
            content = discord.Embed(colour=int(colour, 16))
            content.description = "Looks like we're missing some stuff to complete this command, type `$help fs` to get some help"
            await ctx.send(embed=content)
    
    @fs.command()
    async def go(self, ctx):
        '''Go fishing!'''
        fisher = db.fisher_exists(ctx.author.id)
        if fisher:
            last_fished = fisher[0][3]
            can_fish = self.cooldown_calc(last_fished)
            if can_fish <= 0:
                await self.go_fishing(ctx, fisher)
            else:
                content = discord.Embed(colour=int(colour, 16))
                content.description = f'⏱️ You feel tired and reckon you can go fishing in around **{util.stringfromtimestamp(can_fish)}**'
                await ctx.send(embed=content)
        else:
            db.go_fish(ctx.author.id, 0, 0, datetime.timestamp(datetime.now()), 0, 0)
            fisher = db.fisher_exists(ctx.author.id)
            await self.go_fishing(ctx, fisher)

    @fs.command(aliases=['pf'])
    async def profile(self, ctx):
        '''View your fishing profile'''
        fisher = db.fisher_exists(ctx.author.id)
        if fisher:
            last_fished = datetime.now() - datetime.fromtimestamp(fisher[0][3])
            last_fished = util.stringfromtimestamp(last_fished.seconds)
            content = discord.Embed(title=f"Fisher {util.displayname(ctx.author)}'s profile", 
            colour=int(colour, 16))
            content.description = f"""🎣 Total times fished: {fisher[0][1]}\n🐋 Total Fish caught: {fisher[0][2]}\n⏲️ Last fished: {last_fished} ago\n🌟 Experience points: {fisher[0][4]}"""
            await ctx.send(embed=content)
        else:
            content = discord.Embed(colour=int(colour, 16))
            content.description = 'You have not fished before, please fish before checking your profile!'
            await ctx.send(embed=content)
    
    @fs.command(aliases=['rm'])
    async def reminder(self, ctx):
        '''fishing reminders'''
        fisher = db.fisher_exists(ctx.author.id)
        if fisher:
            last_fished = fisher[0][3]
            can_fish = self.cooldown_calc(last_fished)
            if can_fish <= 0:
                content = discord.Embed(colour=int(colour, 16))
                content.description = f'⏰ You feel refreshed and alert, time to go fishing again!'
                await ctx.send(embed=content)
            else:
                content = discord.Embed(colour=int(colour, 16))
                content.description = f'⏱️ You feel tired and reckon you can go fishing in around **{util.stringfromtimestamp(can_fish)}**'
                await ctx.send(embed=content)
        else:
            content = discord.Embed(colour=int(colour, 16))
            content.description = '⏰ You feel refreshed and alert, time to go fishing!'
            await ctx.send(embed=content)
    
    # helper functions

    async def go_fishing(self, ctx, fisher):
        catch = random.randint(0, 1)
        if bool(catch) == True:
            content = discord.Embed(colour=int(colour, 16))
            content.description = 'Something is on the line, type `"catch"` to reel it in!'
            await ctx.send(embed=content)
            try:
                response = await self.bot.wait_for('message', check=self.catch_check, timeout=15)
                response = response.content
                response = response.lower()
                if response == 'catch':
                    catch = random.randint(0, 1)
                    if bool(catch) == True:
                        await self.award_fish(ctx, fisher, True, 8, '🌟 Congratulations, you caught **1 fish** and are awarded **8 xp!**')
                    else:
                        await self.award_fish(ctx, fisher, False, 4, '⭐ You tried your hardest to reel it in but the fish slipped away, you gain only **4 xp**, better luck next time.')
            except asyncio.TimeoutError:
                await self.award_fish(ctx, fisher, False, 2, '🎇 Oops, the fish escaped before you could reel it in, you gain **2 xp**')
        else:
            await self.award_fish(ctx, fisher, False, 1, '🎇 You cast your reel, but sadly no fish took the bait, you gain **1 xp** try again later')

    async def award_fish(self, ctx, fisher, success, exp, message):
        fisher_id, times_fished, total_fish, last_fished, exp_points, coins = fisher[0]
        times_fished += 1
        if success == True:
            total_fish += 1
        last_fished = datetime.timestamp(datetime.now())
        exp_points += exp
        db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
        content = discord.Embed(colour=int(colour, 16))
        content.description = f'{message}'
        await ctx.send(embed=content)

    def catch_check(ctx, payload):
        payload = payload.content
        payload = payload.lower()
        return payload == 'catch'
    
    def cooldown_calc(self, last_fished):
        cooldown = 1800
        can_fish = datetime.timestamp(datetime.now()) - last_fished
        can_fish = cooldown - can_fish
        return can_fish

def setup(bot):
    bot.add_cog(fish(bot))