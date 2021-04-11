import discord
from discord import colour 
from discord.ext import commands
from tools import utilities as util
from data import database as db

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
    async def embed(self, ctx, channel : discord.TextChannel, *, args):
        """
        - Sends embed in channel, accepts defined arguments
        - Arguments must be separated with "|" arguments must be defined with "="
        - Tags with 'none' & unsupported tags will be ignored.\n
        Supported Arguments:\n
            > title: The title of the embed 
            > description: The description of the embed
            > colour: The colour code of the embed - provide hex code without hash(#)
            > footer: Sets the footer for the embed content
            > thumbnail: Sets the thumbnail for the embed content - provide image url
            > image: Sets the image for the embed content - provide image url
            > author: Sets the author for the embed content.
        """
        parsed_dict = {}
        try:
            for x in args.split('|'):
                for y in [x.split('=')]:
                    parsed_dict.update({y.pop(0).strip() : ''.join(y).strip()})
            for data in parsed_dict:
                if parsed_dict[data] == '':
                    await ctx.send(f'argument: "{data}" has no value - Verify that all tags have values')
                    return
                break
            parsed_dict = {key:val for key, val in parsed_dict.items() if not val == 'none'}
            if not 'colour' in parsed_dict:
                content = discord.Embed(colour=int('ffdd38', 16))
            else:
                content = discord.Embed(colour=int(parsed_dict['colour'], 16))
            if 'title' in parsed_dict:
                content.title = parsed_dict['title']
            if 'description' in parsed_dict:
                content.description = parsed_dict['description']
            if 'footer' in parsed_dict:
                content.set_footer(text=parsed_dict['footer'])
            if 'thumbnail' in parsed_dict:
                content.set_thumbnail(url=parsed_dict['thumbnail'])
            if 'image' in parsed_dict:
                content.set_image(url=parsed_dict['image'])
            if 'author' in parsed_dict:
                content.set_author(name=parsed_dict['author'])
            await ctx.send(embed=content)
        except Exception as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
    
    @commands.command() 
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, channel : discord.TextChannel, *, args):
        """sends mesasge in specified channel"""
        try:
            await channel.send(str(args))
            await ctx.send('\N{Thumbs Up Sign} Message has been sent to specified channel. This notification will be removed soon', delete_after=5)
        except Exception as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def prefix(self, ctx, prefix):
        """changes prefix for current server"""
        try:
            if prefix.startswith(" "):
                await ctx.send("\N{Warning Sign} Prefix can't start with space")
                return
            
            if len(prefix) > 4:
                await ctx.send("\N{Warning Sign} Prefix cannot exceed 4 characters")
                return
            
            db.replace_prefix(ctx.guild.id, prefix.lstrip())
            await ctx.send(f"\N{White Heavy Check Mark} Bot prefix has been updated to {prefix}")
        except Exception as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

def setup(bot):
    bot.add_cog(Moderation(bot))