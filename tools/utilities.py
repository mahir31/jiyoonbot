import sys
import discord
from urllib.request import urlopen
import io
import asyncio
from colorthief import ColorThief
from discord.ext import commands
from data import database as db

def color_from_image(url):
    image = urlopen(url)
    image = io.BytesIO(image.read())
    image = ColorThief(image)
    dominant_color = image.get_color(quality=1)
    return rgb_to_hex(dominant_color)

def rgb_to_hex(rgb):
    r, g, b = rgb
    def clamp(x):
        return max(0, min(x, 255))
    return "{0:02x}{1:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b))

def displayname(user):
    if isinstance(user, discord.Member):
        username = user.nick or user.display_name
    else:
        username = user.name
    return username

def get_time_range(range):
    if range == 'st':
        result = 'short_term'
    elif range == 'shortterm':
        result = 'short_term'
    elif range == 'mt':
        result = 'medium_term'
    elif range == 'mediumterm':
        result = 'medium_term'
    elif range == 'lt':
        result = 'long_term'
    elif range == 'longterm':
        result = 'long_term'
    elif range.isdigit() == True:
        result = 'short_term'
    return result
    
def display_time_range(range):
    if range == 'short_term':
        result = '(approx. last 4 weeks)'
    elif range == 'medium_term':
        result = '(approx. last 6 months)'
    elif range == 'long_term':
        result = '(all time)'
    return result
    
def addlines(lines):
    description = ''
    for line in lines:
        description+=f'\n{line}'
    return description

def numberitems(items):
    numbereditems = []
    n = 1
    for item in items:
        item = f'`#{n}.` {item}'
        n += 1
        numbereditems.append(item)
    return numbereditems

async def paginate(ctx, items, author, colour, thumbnail, display_picture):
    items = numberitems(items)
    pages = []
    x = slice(0, 10)
    index = 0
    while items:
        sliceditems = items[x]
        page = discord.Embed(colour=int(colour, 16))
        page.set_thumbnail(url=thumbnail)
        page.set_author(name=author, icon_url=display_picture)
        page.description = addlines(sliceditems)
        pages.append(page)
        del items[0:10]
    page = await ctx.send(embed=pages[index])
    
    def event_check(payload):
        if payload.user_id == ctx.bot.user.id:
            return False
        if payload.message_id != page.id:
            return False
        return True
    
    await page.add_reaction('◀️')
    await page.add_reaction('▶️')
    while True:
        try:
            reaction = await ctx.bot.wait_for('raw_reaction_add', timeout=90, check=event_check)
            if str(reaction.emoji) == '◀️':
                if index == 0:
                    await page.remove_reaction(reaction.emoji, ctx.bot.get_user(reaction.user_id))
                    continue
                index -= 1                    
                await page.edit(embed=pages[index])
                await page.remove_reaction(reaction.emoji, ctx.bot.get_user(reaction.user_id))
            if str(reaction.emoji) == '▶️':
                if index == len(pages) - 1:
                    await page.remove_reaction(reaction.emoji, ctx.bot.get_user(reaction.user_id))
                    continue
                index += 1
                await page.edit(embed=pages[index])
                await page.remove_reaction(reaction.emoji, ctx.bot.get_user(reaction.user_id))
        except asyncio.TimeoutError:
            await page.clear_reaction('◀️')
            await page.clear_reaction('▶️')

def stringfromtimestamp(s):
    s = (int(s))
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    comp = []
    if d > 0:
        comp.append(f'{d} day' + ('s' if d > 1 else ''))
    if h > 0:
        comp.append(f'{h} hour' + ('s' if h > 1 else ''))
    if m > 0:
        comp.append(f'{m} minute' + ('s' if m > 1 else ''))
    if s > 0:
        comp.append(f'{s} second' + ('s' if s > 1 else ''))
    return ' '.join(comp)

def get_pitch(p):
    if p == 0:
        tone = 'C'
    elif p == 1:
        tone = 'C♯'
    elif p == 2:
        tone = 'D'
    elif p == 3:
        tone = 'D♯'
    elif p == 4:
        tone = 'E'
    elif p == 5:
        tone = 'F'
    elif p == 6:
        tone = 'F♯'
    elif p == 8:
        tone = 'G'
    elif p == 9:
        tone = 'G♯'
    elif p == 10:
        tone = 'A'
    elif p == 11:
        tone = 'G♯'
    else:
        tone = 'unidentified'
    return tone

def get_mode(m):
    if m == 0:
        mode = 'Minor'
    elif m == 1:
        mode = 'Major'
    return mode

def get_prefix(bot, message):
    return((db.get_prefix(message.guild.id)))