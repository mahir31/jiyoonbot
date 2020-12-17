import discord
from discord.ext import commands
from data import database as db
import logging
from datetime import datetime
import random
import asyncio
from tools import utilities as util

class fish(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: fishing.py connected")
    
    # commands
    
    @commands.group(case_insensitive=True)
    async def fs(self, ctx):
        '''
        Fishing Commands:
        '''
    
    @fs.command()
    async def go(self, ctx):
        fisher = db.fisher_exists(ctx.author.id)
        if fisher:
            last_fished = fisher[0][3]
            can_fish = self.cooldown_calc(last_fished)
            if can_fish <= 0:
                await self.go_fishing(ctx, fisher)
            else:
                await ctx.send(f"imagine trying to go fishing while you're still on cooldown, couldn't be me. try again in {util.stringfromtimestamp(can_fish)} ⏰")
        else:
            db.go_fish(ctx.author.id, 0, 0, datetime.timestamp(datetime.now()), 0, 0)
            fisher = db.fisher_exists(ctx.author.id)
            await self.go_fishing(ctx, fisher)

    @fs.command(aliases=['pf'])
    async def profile(self, ctx):
        fisher = db.fisher_exists(ctx.author.id)
        if fisher:
            content = discord.Embed(title=f"Fisher {util.displayname(ctx.author)}'s profile", 
            colour=int('add8e6', 16))
            content.description = f"""🎣 Total times fished: {fisher[0][1]}
            🐋 Total Fish caught: {fisher[0][2]}
            ⏲️ Last fished: {util.stringfromtimestamp(self.cooldown_calc(fisher[0][3]))}
            🌟 Experience points: {fisher[0][4]}"""
            await ctx.send(embed=content)
    
    # helper functions

    async def go_fishing(self, ctx, fisher):
        '''go fishing'''
        fisher_id, times_fished, total_fish, last_fished, exp_points, coins = fisher[0]
        catch = random.randint(0, 1)
        if bool(catch) == True:
            await ctx.send('Something is on the line, type `"catch"` to reel it in!')
            try:
                response = await self.bot.wait_for('message', check=self.catch_check, timeout=15)
                if response:
                    catch = random.randint(0, 1)
                    if bool(catch) == True:
                        times_fished += 1
                        total_fish += 1
                        last_fished = datetime.timestamp(datetime.now())
                        exp_points += 8
                        db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
                        await ctx.send('Congratulations, you caught 1 fish and are awarded 8 xp 🌟!')
                    else:
                        times_fished += 1
                        last_fished = datetime.timestamp(datetime.now())
                        exp_points += 4
                        db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
                        await ctx.send('You tried your hardest to reel it in but the fish slipped away, you gain only 4 xp ⭐, better luck next time.')
            except asyncio.TimeoutError:
                times_fished += 1
                last_fished = datetime.timestamp(datetime.now())
                exp_points += 2
                db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
                await ctx.send('Oops, the fish escaped before you could reel it in, you gain 2 xp 🎇')
        else:
            times_fished += 1
            last_fished = datetime.timestamp(datetime.now())
            exp_points += 2
            db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
            await ctx.send('You cast your reel, but sadly no fish took the bait, you gain 1 xp 🎇 try again later')

    def catch_check(ctx, payload):
        return payload.content == 'catch'
    
    def cooldown_calc(self, last_fished):
        cooldown = 1800
        can_fish = datetime.timestamp(datetime.now()) - last_fished
        can_fish = cooldown - can_fish
        return can_fish

# await ctx.send(f'fisher id: {fisher_id}, times fished: {times_fished}, total fish: {total_fish}, last fished: {last_fished}, exp points: {exp_points}, coins: {coins}')

def setup(bot):
    bot.add_cog(fish(bot))