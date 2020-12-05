import discord
from discord.ext import commands
from data import database as db
from tools import spt_requests as sp
from tools import utilities as util
import logging

class spt(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("cog: spt.py connected")
    
    # commands

    @commands.group(case_insensitive=True)
    async def sp(self, ctx):
        '''
        Spotify Commands:
        > `available time ranges: shortterm | mediumterm | longterm`
        > `maximum limit: 50`
        > `Defaults listed below`
        '''
        if ctx.invoked_subcommand is None:
            await self.nowplaying(ctx)
    
    @sp.command()
    async def connect(self, ctx):
        '''Connect your Spotify'''
        content = self.create_connect_embed(ctx.author.avatar_url)
        await ctx.send(embed=content)
    
    @sp.command(aliases=['np'])
    async def nowplaying(self, ctx):
        '''Show currently playing track'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed(ctx.author.avatar_url))
        else:
            result = sp.internal_call('/v1/me/player/currently-playing', access_token)
            if result:
                content = self.create_np_embed(result['item'], ctx.author)
            else:
                result = sp.internal_call('/v1/me/player/recently-played?limit=1', access_token)
                content = self.create_recently_played_embed(result['items'][0]['track'], ctx.author)
            await ctx.send(embed=content)
    
    @sp.command(aliases=['re'])
    async def recent(self, ctx, limit=20):
        '''Recently played tracks'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed(ctx.author.avatar_url))
        else:
            result = sp.internal_call(f'/v1/me/player/recently-played?limit={limit}', access_token)
            if result:
                content = self.create_recent_embed(result, ctx.author)
                await ctx.send(embed=content)
            else:
                await ctx.send('```an error occured```')

    @sp.command(aliases=['ta'])
    async def topartists(self, ctx, time_range='st', limit=20):
        '''Top artists'''
        if time_range.isdigit():
            limit = time_range
            time_range = util.get_time_range(time_range)
        else:
            time_range = util.get_time_range(time_range)
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed(ctx.author.avatar_url))
        else:
            result = sp.internal_call(f'/v1/me/top/artists?time_range={time_range}&limit={limit}', access_token)
            if result:
                content = self.create_ta_embed(result, ctx.author, time_range)
                await ctx.send(embed=content)
            else:
                await ctx.send('```an error occured```')
    
    @sp.command(aliases=['tt'])
    async def toptracks(self, ctx, time_range='st', limit=20):
        '''Top tracks'''
        if time_range.isdigit():
            limit = time_range
            time_range = util.get_time_range(time_range)
        else:
            time_range = util.get_time_range(time_range)
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed(ctx.author.avatar_url))
        else:
            result = sp.internal_call(f'/v1/me/top/tracks?time_range={time_range}&limit={limit}', access_token)
            if result:
                content = self.create_tt_embed(result, ctx.author, time_range)
                await ctx.send(embed=content)
            else:
                await ctx.send('```an error occured```')
    
    # helper functions

    def rtv_access_token(self, discord_id):
        refresh_token = db.rtv_refresh_token(discord_id)
        if refresh_token:
            access_token = sp.get_access_token(refresh_token[0][0])
            return access_token
        else:
            return None

    # create embeds

    def create_connect_embed(self, icon):
        url = 'https://jiyoonbot.xyz/authorise/'
        content = discord.Embed(colour = int('ffff00', 16))
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
    
    def create_recent_embed(self, recently_played, user):
        track_names = [t['track']['name'] for t in recently_played['items']]
        artist_names = [a['track']['artists'][0]['name'] for a in recently_played['items']]
        album_artwork = recently_played['items'][0]['track']['album']['images'][0]['url']
        image_color = util.color_from_image(album_artwork)

        content = discord.Embed(colour = int(image_color, 16))
        content.description = '\n'.join('{} - {}'.format(artist_names, track_names) for artist_names, track_names in zip(artist_names, track_names))
        content.set_thumbnail(url=album_artwork)
        content.set_author(name=util.displayname(user) + ' - Recent tracks',
            icon_url=user.avatar_url)
        return content
    
    def create_ta_embed(self, top_artists, user, time_range):
        artist_names = [ta['name'] for ta in top_artists['items']]
        artist_image = top_artists['items'][0]['images'][0]['url']
        image_color = util.color_from_image(artist_image)
        term = util.display_time_range(time_range)

        content = discord.Embed(colour = int(image_color, 16))
        content.description = '\n'.join(artist_names)
        content.set_thumbnail(url=artist_image)
        content.set_author(name=util.displayname(user) + f' - Top artists {term}',
            icon_url=user.avatar_url)
        return content
    
    def create_tt_embed(self, top_tracks, user, time_range):
        track_names = [t['name'] for t in top_tracks['items']]
        artist_names = [a['artists'][0]['name'] for a in top_tracks['items']]
        album_artwork = top_tracks['items'][0]['album']['images'][0]['url']
        image_color = util.color_from_image(album_artwork)
        term = util.display_time_range(time_range)

        content = discord.Embed(colour = int(image_color, 16))
        content.description = '\n'.join('{} - {}'.format(artist_names, track_names) for artist_names, track_names in zip(artist_names, track_names))
        content.set_thumbnail(url=album_artwork)
        content.set_author(name=util.displayname(user) + f' - Top tracks {term}',
            icon_url=user.avatar_url)
        return content


def setup(bot):
    bot.add_cog(spt(bot))