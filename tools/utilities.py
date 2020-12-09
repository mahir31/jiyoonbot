import sys
import discord
from urllib.request import urlopen
import io
from colorthief import ColorThief
from discord.ext import commands

COLOUR = int('ffff00', 16)
FIRST_EMOJI = '\u23EE'
LEFT_EMOJI = '\u2B05'
RIGHT_EMOJI = '\u27A1'
LAST_EMOJI = '\u23ED'

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

def paginator(items, title):
    pages = []
    x = slice(0, 10)
    while items:
        listitems = ''
        sliceditems = items[x]
        page = discord.Embed(colour=COLOUR, title=title)
        page.description = addlines(sliceditems)
        pages.append(page)
        del items[0:10]
    return pages
    
def addlines(lines):
    description = ''
    for line in lines:
        description+=f'\n{line}'
    return description
