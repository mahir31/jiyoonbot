import discord
from discord.ext import commands
from data import database as db
import logging
from datetime import datetime
import random
import asyncio

class fish(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: fishing.py connected")
    
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
            if bool(can_fish) == True:
                await self.go_fishing(ctx, fisher)
            else:
                await ctx.send("imagine trying to go fishing while you're still on cooldown, couldn't be me.")
        else:
            await self.go_fishing(ctx, fisher)

    async def go_fishing(self, ctx, fisher):
        fisher_id, times_fished, total_fish, last_fished, exp_points, coins = fisher[0]
        catch = random.randint(0, 1)
        catch = 1
        if bool(catch) == True:
            await ctx.send('Something is on the line, type `"catch"` to reel it in!')
            try:
                response = await self.bot.wait_for('message', check=self.catch_check, timeout=15)
                if response:
                    catch = random.randint(0, 1)
                    catch = 1
                    if bool(catch) == True:
                        times_fished += 1
                        total_fish += 1
                        last_fished = datetime.timestamp(datetime.now())
                        exp_points += 8
                        db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
                        await ctx.send('Congratulations, you caught 1 fish and are awarded 8 xp!')
                    else:
                        times_fished += 1
                        last_fished = datetime.timestamp(datetime.now())
                        exp_points += 4
                        db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
                        await ctx.send('You tried your hardest to reel it in but the fish slipped away, you gain only 4 xp, better luck next time.')
            except asyncio.TimeoutError:
                times_fished += 1
                last_fished = datetime.timestamp(datetime.now())
                exp_points += 2
                db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
                await ctx.send('Oops, the fish escaped before you could reel it in, you gain 2 xp')
        else:
            times_fished += 1
            last_fished = datetime.timestamp(datetime.now())
            exp_points += 2
            db.go_fish(fisher_id, times_fished, total_fish, last_fished, exp_points, coins)
            await ctx.send('You cast your reel, but sadly no fish took the bait, you gain 1 xp try again later')

    def catch_check(ctx, payload):
        return payload.content == 'catch'
    
    def cooldown_calc(self, last_fished):
        cooldown = 1800
        can_fish = datetime.timestamp(datetime.now()) - last_fished
        can_fish = cooldown - can_fish
        if can_fish <= 0:
            return True
        else:
            return False

# await ctx.send(f'fisher id: {fisher_id}, times fished: {times_fished}, total fish: {total_fish}, last fished: {last_fished}, exp points: {exp_points}, coins: {coins}')

def setup(bot):
    bot.add_cog(fish(bot))