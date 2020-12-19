import discord
from discord.ext import commands
from data import database as db
from tools import spt_requests as sp
from tools import utilities as util
import logging
import asyncio

class Spotify(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: spotify.py connected")
    
    # commands

    @commands.group(case_insensitive=True)
    async def sp(self, ctx):
        '''
        Spotify Commands:
        > `available time ranges: shortterm | mediumterm | longterm`
        '''
        if ctx.invoked_subcommand is None:
            await self.nowplaying(ctx)
    
    @sp.command()
    async def connect(self, ctx):
        '''Connect your Spotify'''
        content = self.create_connect_embed()
        await ctx.send(embed=content)
    
    @sp.command(aliases=['np'])
    async def nowplaying(self, ctx):
        '''Show currently playing track'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            result = sp.internal_call('/v1/me/player/currently-playing', access_token)
            if result:
                content = self.create_np_embed(result['item'], ctx.author)
            else:
                result = sp.internal_call('/v1/me/player/recently-played?limit=1', access_token)
                content = self.create_recently_played_embed(result['items'][0]['track'], ctx.author)
            await ctx.send(embed=content)
    
    @sp.command(aliases=['re'])
    async def recent(self, ctx):
        '''Recently played tracks'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            result = sp.internal_call(f'/v1/me/player/recently-played?limit=50', access_token)
            if result:
                track_names = [t['track']['name'] for t in result['items']]
                artist_names = [a['track']['artists'][0]['name'] for a in result['items']]
                album_artwork = result['items'][0]['track']['album']['images'][0]['url']
                image_color = util.color_from_image(album_artwork)
                content = []
                for artist_names, track_names in zip(artist_names, track_names):
                    x = ''.join(f'**{artist_names}** - {track_names}')
                    content.append(x)
                await util.paginate(ctx, 
                    content, 
                    f'{util.displayname(ctx.author)} - Recent tracks:', 
                    image_color, 
                    album_artwork,
                    ctx.author.avatar_url
                )
            else:
                await ctx.send('`an error occured`')

    @sp.command(aliases=['ta'])
    async def topartists(self, ctx, time_range='st'):
        '''Top artists'''
        time_range = util.get_time_range(time_range)
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed(ctx.author.avatar_url))
        else:
            result = sp.internal_call(f'/v1/me/top/artists?time_range={time_range}&limit=50', access_token)
            if result:
                artist_names = [ta['name'] for ta in result['items']]
                artist_image = result['items'][0]['images'][0]['url']
                image_color = util.color_from_image(artist_image)
                term = util.display_time_range(time_range)
                await util.paginate(ctx, 
                    artist_names,
                    f'{util.displayname(ctx.author)} - Top artists {term}:',
                    image_color,
                    artist_image,
                    ctx.author.avatar_url
                )
            else:
                await ctx.send('`an error occured`')
    
    @sp.command(aliases=['tt'])
    async def toptracks(self, ctx, time_range='st'):
        '''Top tracks'''
        time_range = util.get_time_range(time_range)
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            result = sp.internal_call(f'/v1/me/top/tracks?time_range={time_range}&limit=50', access_token)
            if result:
                track_names = [t['name'] for t in result['items']]
                artist_names = [a['artists'][0]['name'] for a in result['items']]
                album_artwork = result['items'][0]['album']['images'][0]['url']
                image_color = util.color_from_image(album_artwork)
                term = util.display_time_range(time_range)
                content = []
                for artist_names, track_names in zip(artist_names, track_names):
                    x = ''.join(f'{artist_names} - **{track_names}**')
                    content.append(x)
                await util.paginate(ctx,
                    content,
                    f'{util.displayname(ctx.author)} - Top tracks {term}:',
                    image_color,
                    album_artwork,
                    ctx.author.avatar_url
                )
            else:
                await ctx.send('`an error occured`')
    
    @sp.command(aliases=['dc'])
    async def disconnect(self, ctx):
        '''Disconnect Spotify account'''
        icon = 'https://www.scdn.co/i/_global/touch-icon-72.png'
        icon_colour = util.color_from_image(icon)
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            content = discord.Embed(title='Disconnect Spotify account', colour=int(icon_colour, 16))
            content.description = 'Are you sure you would like to disconnect your spotify account?'
            confirmation = await ctx.send(embed=content)

            def event_check(payload):
                if payload.user_id == ctx.bot.user.id:
                    return False
                return True

            await confirmation.add_reaction('✅')
            await confirmation.add_reaction('🚫')
            while True:
                try:
                    reaction = await self.bot.wait_for('raw_reaction_add', timeout=90, check=event_check)
                    if str(reaction.emoji) == '✅':
                        db.delete_spt_user(ctx.author.id)
                        content.description = 'Your account has been disconnected.'
                        await confirmation.clear_reaction('✅')
                        await confirmation.clear_reaction('🚫')
                        await confirmation.edit(embed=content)
                    elif str(reaction.emoji) == '🚫':
                        content.description = 'User disconnect has been cancelled'
                        await confirmation.clear_reaction('✅')
                        await confirmation.clear_reaction('🚫')
                        await confirmation.edit(embed=content)
                except asyncio.exceptions.TimeoutError:
                    content.description = 'Disconnect operation has timed out. resend command to retry.'
                    await confirmation.clear_reaction('✅')
                    await confirmation.clear_reaction('🚫')
                    await confirmation.edit(embed=content)

    # helper functions

    def rtv_access_token(self, discord_id):
        refresh_token = db.rtv_refresh_token(discord_id)
        if refresh_token:
            access_token = sp.get_access_token(refresh_token[0][0])
            return access_token
        else:
            return None

    # create embeds

    def create_connect_embed(self):
        icon = 'https://www.scdn.co/i/_global/touch-icon-72.png'
        icon_colour = util.color_from_image(icon)
        url = 'https://jiyoonbot.xyz/authorise/'
        content = discord.Embed(colour = int(icon_colour, 16))
        content.set_author(icon_url=icon,
            name="Connect your Spotify account")
        content.description = f"To utilise Spotify commands please click [here]({url}) to connect your account"
        return content

    def create_np_embed(self, now_playing, user):
        track_name = now_playing['name']
        album_name = now_playing['album']['name']
        artists = ', '.join([a['name'] for a in now_playing['artists']])
        album_artwork = now_playing['album']['images'][0]['url']
        image_color = util.color_from_image(album_artwork)
        track_url = now_playing['external_urls']['spotify']

        content = discord.Embed(colour = int(image_color, 16))
        content.description = album_name
        content.title = f'{artists} - {track_name}'
        content.set_thumbnail(url=album_artwork)
        content.set_author(name=util.displayname(user) + " is now playing",
            icon_url=user.avatar_url,
            url=track_url)
        return content
    
    def create_recently_played_embed(self, recently_played, user):
        track_name = recently_played['name']
        album_name = recently_played['album']['name']
        artists = ', '.join([a['name'] for a in recently_played['artists']])
        album_artwork = recently_played['album']['images'][0]['url']
        image_color = util.color_from_image(album_artwork)
        track_url = recently_played['external_urls']['spotify']

        content = discord.Embed(colour = int(image_color, 16))
        content.description = album_name
        content.title = f'{artists} - {track_name}'
        content.set_thumbnail(url=album_artwork)
        content.set_author(name=util.displayname(user) + ' has most recently played:',
            icon_url=user.avatar_url,
            url=track_url)
        return content


def setup(bot):
    bot.add_cog(Spotify(bot))