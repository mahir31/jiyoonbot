import discord
from discord.ext import commands
from data import database as db
from tools import spt_requests as sp
from tools import utilities as util
import logging
import asyncio
from PIL import Image
from io import BytesIO
import requests
import os
import matplotlib.pyplot as plt
from palettable.cartocolors.qualitative import Pastel_7
from textwrap import wrap

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
    
    @sp.command(aliases=['np'])
    async def nowplaying(self, ctx):
        '''Show currently playing track'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            result = await sp.internal_call('/v1/me/player/currently-playing', access_token)
            if result:
                content = self.create_np_embed(result['item'], ctx.author)
            else:
                result = await sp.internal_call('/v1/me/player/recently-played?limit=1', access_token)
                content = self.create_recently_played_embed(result['items'][0]['track'], ctx.author)
            await ctx.send(embed=content)
    
    @sp.command(aliases=['re'])
    async def recent(self, ctx):
        '''Recently played tracks'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            result = await sp.internal_call(f'/v1/me/player/recently-played?limit=50', access_token)
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
            result = await sp.internal_call(f'/v1/me/top/artists?time_range={time_range}&limit=50', access_token)
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
            result = await sp.internal_call(f'/v1/me/top/tracks?time_range={time_range}&limit=50', access_token)
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
    
    @sp.command(aliases=['sa'])
    async def searchartist(self, ctx, *query):
        '''search for an artist on spotify'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            try:
                if query[0] == 'np':
                    result = await sp.internal_call('/v1/me/player/currently-playing', access_token)
                    if result:
                        artist = await sp.internal_call(f'/v1/artists/{result["item"]["artists"][0]["id"]}', access_token)
                        top_tracks = await sp.internal_call(f'/v1/artists/{result["item"]["artists"][0]["id"]}/top-tracks?country=from_token', access_token)
                        top_tracks = self.linked_tracks(top_tracks)
                        await ctx.send(embed=self.create_artist_embed(artist, top_tracks))
                    else:
                        result = await sp.internal_call('/v1/me/player/recently-played?limit=1', access_token)
                        artist = await sp.internal_call(f'/v1/artists/{result["items"][0]["track"]["artists"][0]["id"]}', access_token)
                        top_tracks = await sp.internal_call(f'/v1/artists/{result["items"][0]["track"]["artists"][0]["id"]}/top-tracks?country=from_token', access_token)
                        top_tracks = self.linked_tracks(top_tracks)
                        await ctx.send(embed=self.create_artist_embed(artist, top_tracks))
                else:
                    artist = await self.spotify_search(query, query_type='artist', access_token=access_token)
                    top_tracks = await sp.internal_call(f'/v1/artists/{artist["artists"]["items"][0]["id"]}/top-tracks?country=from_token', access_token)
                    top_tracks = self.linked_tracks(top_tracks)
                    await ctx.send(embed=self.create_artist_embed(artist['artists']['items'][0], top_tracks))
            except IndexError:
                content = discord.Embed(colour=int(util.color_from_image('https://www.scdn.co/i/_global/touch-icon-72.png'), 16))
                content.description = "Looks like you're missing a few things, give me the name of the artist you're looking for or type 'np' to look for the artist you're listening to now."
                content.set_author(name='Error:',
                    icon_url='https://www.scdn.co/i/_global/touch-icon-72.png')
                await ctx.send(embed=content)
    
    @sp.command(aliases=['salb'])
    async def searchalbum(self, ctx, *query):
        '''search for an album on spotify'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            try:
                if query[0] == 'np':
                    result = await sp.internal_call('/v1/me/player/currently-playing', access_token)
                    if result:
                        await ctx.send(embed=self.create_album_embed(result['item']['album']))
                    else:
                        result = await sp.internal_call('/v1/me/player/recently-played?limit=1', access_token)
                        await ctx.send(embed=self.create_album_embed(result['items'][0]['track']['album']))
                else:
                    result = await self.spotify_search(query, query_type='album', access_token=access_token)
                    await ctx.send(embed=self.create_album_embed(result['albums']['items'][0]))
            except IndexError:
                content = discord.Embed(colour=int(util.color_from_image('https://www.scdn.co/i/_global/touch-icon-72.png'), 16))
                content.description = "Looks like you're missing a few things, give me the name of the album you're looking for or type 'np' to look for the album you're listening to now."
                content.set_author(name='Error:',
                    icon_url='https://www.scdn.co/i/_global/touch-icon-72.png')
                await ctx.send(embed=content)
    
    @sp.command(aliases=['rc'])
    async def recommendations(self, ctx):
        '''recommendations generated from Spotify based on users top tracks, top artists and top genres'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            seed_tracks = []
            seed_artists = []
            result = await sp.internal_call('/v1/me/top/tracks?limit=1&time_range=medium_term', access_token)
            seed_tracks.append(result['items'][0]['id'])
            result = await sp.internal_call('/v1/me/top/tracks?limit=1&time_range=short_term', access_token)
            seed_tracks.append(result['items'][0]['id'])
            result = await sp.internal_call('/v1/me/top/artists?limit=1&time_range=medium_term', access_token)
            seed_artists.append(result['items'][0]['id'])
            result = await sp.internal_call('/v1/me/top/artists?limit=1&time_range=short_term', access_token)
            seed_artists.append(result['items'][0]['id'])
            seed_tracks = ','.join(seed_tracks)
            seed_artists = ','.join(seed_artists)
            result = await sp.internal_call(f"/v1/recommendations?seed_tracks={seed_tracks}&seed_artists={seed_artists}&limit=9", access_token)
            linked_tracks = self.linked_tracks(result)
            linked_tracks = ', '.join(linked_tracks)
            album_artwork = [x['album']['images'][0]['url'] for x in result['tracks']]
            songimg = Image.new('RGB', (1920, 1920))
            xpos = 0
            ypos = 0
            for x in range(0, len(album_artwork)):
                image = requests.get(album_artwork[x])
                image = Image.open(BytesIO(image.content))
                songimg.paste(image, (xpos,ypos))
                xpos += 640
                if(xpos == 1920):
                    xpos = 0
                    ypos += 640
            songimg.save('image.jpeg')
            content = discord.Embed(colour=int(util.color_from_image(result['tracks'][0]['album']['images'][0]['url']), 16))
            file = discord.File('image.jpeg', filename='image.jpeg')
            content.set_image(url='attachment://image.jpeg')
            content.description = f'Click the links to go to their tracks:\n{linked_tracks}'
            content.set_author(name=f"✨{util.displayname(ctx.author)}'s personal recommendations!",
                icon_url='https://www.scdn.co/i/_global/touch-icon-72.png')
            content.set_footer(text='🎵 Generated by Spotify')
            await ctx.send(file=file, embed=content)
            os.remove('image.jpeg')
    
    @sp.command(aliases=['ft'])
    async def features(self, ctx):
        '''display audio features for currently playing or most recently played track'''
        access_token = self.rtv_access_token(ctx.author.id)
        if not access_token:
            await ctx.send(embed=self.create_connect_embed())
        else:
            track = await sp.internal_call('/v1/me/player/currently-playing', access_token)
            if not track:
                track = await sp.internal_call('/v1/me/player/recently-played?limit=1', access_token)
                await self.create_features_chart(ctx, track['items'][0]['track'], access_token)
            else:
                await self.create_features_chart(ctx, track['item'], access_token)

    # helper functions

    def rtv_access_token(self, discord_id):
        refresh_token = db.rtv_refresh_token(discord_id)
        if refresh_token:
            access_token = sp.get_access_token(refresh_token[0][0])
            return access_token
        else:
            return None
    
    def linked_tracks(self, tracks):
        names = [t['name'] for t in tracks['tracks']]
        links = [t['external_urls']['spotify'] for t in tracks['tracks']]
        content = []
        for names, links in zip(names, links):
            x = f'[{names}]({links})'
            content.append(x)
        return content
    
    async def spotify_search(self, query, query_type, access_token):
        query = '%20'.join(query)
        result = await sp.internal_call(f'/v1/search?q={query}&type={query_type}&limit=1', access_token)
        return result

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
        album_artwork = now_playing['album']['images'][1]['url']
        image_color = util.color_from_image(album_artwork)
        track_url = now_playing['external_urls']['spotify']
        popularity = now_playing['popularity']

        content = discord.Embed(colour = int(image_color, 16))
        content.description = album_name
        content.title = f'{artists} - {track_name}'
        content.set_thumbnail(url=album_artwork)
        content.set_author(name=util.displayname(user) + " is now playing",
            icon_url=user.avatar_url,
            url=track_url)
        content.set_footer(text=f'Popularity: {popularity}')
        return content
    
    def create_recently_played_embed(self, recently_played, user):
        track_name = recently_played['name']
        album_name = recently_played['album']['name']
        artists = ', '.join([a['name'] for a in recently_played['artists']])
        album_artwork = recently_played['album']['images'][1]['url']
        image_color = util.color_from_image(album_artwork)
        track_url = recently_played['external_urls']['spotify']
        popularity = recently_played['popularity']

        content = discord.Embed(colour = int(image_color, 16))
        content.description = album_name
        content.title = f'{artists} - {track_name}'
        content.set_thumbnail(url=album_artwork)
        content.set_author(name=util.displayname(user) + ' has most recently played:',
            icon_url=user.avatar_url,
            url=track_url)
        content.set_footer(text=f'Popularity: {popularity}')
        return content
    
    def create_artist_embed(self, artist, top_tracks):
        content = discord.Embed(colour=int(util.color_from_image(artist['images'][0]['url']), 16))
        content.add_field(name='Popularity:', value=f'`{artist["popularity"]}`', inline=True)
        content.add_field(name='Genres:', value=f'`{" ".join(artist["genres"])}`', inline=True)
        content.set_image(url=artist['images'][0]['url'])
        content.set_author(name=f'Artist: {artist["name"]}',
            url=artist['external_urls']['spotify'])
        top_tracks = ', '.join(top_tracks)
        content.description = f'**Top tracks**: {top_tracks}'
        return content

    def create_album_embed(self, album):
        artists = ', '.join([a['name'] for a in album['artists']])
        content = discord.Embed(colour=int(util.color_from_image(album['images'][1]['url']), 16))
        content.set_image(url=album['images'][0]['url'])
        content.set_author(name=f'Album: {album["name"]}',
            url=album['external_urls']['spotify'])
        content.add_field(name='Artist:', value=f'`{artists}`')
        content.add_field(name='Release date:', value=f'`{album["release_date"]}`')
        content.add_field(name='Total tracks:', value=f'`{album["total_tracks"]}`')
        content.add_field(name='Type:', value=f'`{album["album_type"]}`')
        return content

    async def create_features_chart(self, ctx, track, access_token):
        features = await sp.internal_call(f'/v1/audio-features/{track["id"]}', access_token)
        names = 'danceability', 'energy', 'speechiness', 'acousticness', 'liveness', 'valence'
        size = [features['danceability'],
            features['energy'],
            features['speechiness'],
            features['acousticness'],
            features['liveness'],
            features['valence']]
        plt.pie(size, labels=names, colors=Pastel_7.hex_colors, labeldistance=1.15, wedgeprops= { 'linewidth' : 3, 'edgecolor' : 'white' })
        p=plt.gcf()
        plt.rcParams['axes.titlesize'] = 10
        plt.title("\n".join(wrap(f"Spotify catalog information for: {track['name']} by {track['artists'][0]['name']}")))
        plt.savefig('chart.jpeg')
        file = discord.File('chart.jpeg', filename='chart.jpeg')
        
        content = discord.Embed(colour=int(util.color_from_image('https://www.scdn.co/i/_global/touch-icon-72.png'), 16))
        content.set_image(url='attachment://chart.jpeg')
        content.set_author(name=f'📊{track["name"]} feature analysis',
            url=track['external_urls']['spotify'],
            icon_url='https://www.scdn.co/i/_global/touch-icon-72.png')
        content.add_field(name='Key:', value=f'`{util.get_pitch(features["key"])} {util.get_mode(features["mode"])}`')
        content.add_field(name='Length:', value=f'`{util.stringfromtimestamp(features["duration_ms"]/1000.0)}`')
        content.add_field(name='Tempo:', value=f'`{int(features["tempo"])} beats per minute`')
        content.set_footer(text='🎵 Analysis provided by Spotify')
        
        await ctx.send(file=file, embed=content)
        os.remove('chart.jpeg')
        plt.clf()

def setup(bot):
    bot.add_cog(Spotify(bot))