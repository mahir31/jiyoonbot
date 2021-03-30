import asyncio
import tweepy
import discord
import os
import logging
from data import database as db
from discord.ext import commands

consumer_key = os.environ['TWITTER_API_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_API_CONSUMER_SECRET']
key = os.environ['TWITTER_ACCESS_TOKEN']
secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):

	def __init__(self, client, streamcog):
		self.discord_client = client
		self.streamcog = streamcog
		super().__init__()

	def on_connect(self):
		print("connected")

	def on_status(self, status):
		self.discord_client.loop.create_task(self.streamcog.tweethandler(status))
	
	def on_error(self, status_code):
		self.discord_client.loop.create_task(self.streamcog.restart(status_code))

	def on_exception(self, exception):
		self.discord_client.loop.create_task(self.streamcog.restart(exception))

	def on_timeout(self):
		self.discord_client.create_task(self.streamcog.restart("stream timeout"))


class TwitterStreamer(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.twitterStream = None
	
	# bot commands

	@commands.group(case_insensitive=True, hidden=True)
	@commands.is_owner()
	async def tw(self, ctx):
		'''Commands for Twitter streamer:'''
	
	@tw.command()
	@commands.is_owner()
	async def addsite(self, ctx, channel: discord.TextChannel, username):
		'''specify a channel and an account to add a site'''
		twitter_id = api.get_user(username).id
		current_channel = db.channel_exists(channel.id)
		if current_channel:
			is_followed = db.is_followed(channel.id, twitter_id)
			if is_followed:
				await ctx.send(f"{username} is already being followed in {channel.mention}")
			else:
				db.follow_site(channel.id, twitter_id)
				await ctx.send(f"{username} has been added to {channel.mention}")
		else:
			db.follow_site(channel.id, twitter_id)
			await ctx.send (f"{username} has been added to {channel.mention}")
	
	@tw.command()
	@commands.is_owner()
	async def sitecheck(self, ctx, channel: discord.TextChannel):
		'''specify a channel to check which sites are aligned to it'''
		twitter_id = db.check_site(channel.id)[0]
		for tw_id in twitter_id:
			username = api.get_user(tw_id).screen_name
			await ctx.send(username)
	
	@tw.command()
	@commands.is_owner()
	async def removesite(self, ctx, channel: discord.TextChannel, username):
		'''specify a channel and a username to remove the site from the channel'''
		user = api.get_user(username).id
		db.remove_site(channel.id, user)
		await ctx.send(f"site '{username}' has been removed from {channel.mention}")
	
	@tw.command(aliases=['dc'])
	@commands.is_owner()
	async def disconnect(self, ctx):
		'''disconnect the bot - requires bot owner role'''
		self.disconnect_stream()
		await ctx.send('Twitter streamer has been disconnected')
	
	@tw.command()
	@commands.is_owner()
	async def start(self, ctx):
		'''start and connect the bot - requires bot owner role'''
		self.run_stream()
		await ctx.send('Twitter streamer is now running')

	# streamer management functions 

	def run_stream(self):
		self.twitterStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(self.bot, self))
		self.twitterStream.filter(follow=db.get_sites(), is_async=True)
	
	async def restart(self, data):
		self.twitterStream.disconnect()
		del self.twitterStream
		await asyncio.sleep(10)
		self.run_stream()
	
	def disconnect_stream(self):
		logging.info('Disconnecting Twitter Stream')
		self.twitterStream.disconnect()
		del self.twitterStream
		self.twitterStream = None
	
	# incoming tweet code flow

	async def tweethandler(self, status):
		if self.is_retweet(status):
			return
		if self.is_reply(status):
			return
		tweet = api.get_status(str(status.id), tweet_mode="extended", include_entities=True)
		await self.main(tweet)

	def is_retweet(self, status):
		if status.retweeted or "RT @" in status.text:
			return True

	def is_reply(self, status):
		if status.in_reply_to_screen_name is not None:
			return True

	async def main(self, tweet):
		text = self.tweet_text(tweet)
		media_links = self.media_links(tweet)
		await self.send_tweet(tweet, text, media_links)

	def tweet_text(self, tweet):
		try:
			text = tweet.full_text
			return text
		except AttributeError:
			return tweet.text

	def media_links(self, tweet):
		media_links = []
		try:
			if 'media' in tweet.entities:
				for media in tweet.extended_entities['media']:
					media_url = media['media_url_https']
					media_links.append(media_url)
				return media_links
		except AttributeError:
			return media_links

	async def send_tweet(self, tweet, text, media_links):
		for channel_id in db.get_channels(tweet.user.id):
			channel = self.bot.get_channel(id=channel_id)
		content = discord.Embed(colour=int(tweet.user.profile_link_color, 16))
		content.set_author(icon_url=tweet.user.profile_image_url_https,
		name=f"@{tweet.user.screen_name}",
		url=f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}")
		content.description = text
		if media_links:
			content.set_image(url=media_links[0])
			await channel.send(embed=content)
			del media_links[0]
			content._author = None
			content.description = None
			if media_links:
				for media in media_links:
					content.set_image(url=media)
					await channel.send(embed=content)


def setup(bot):
    bot.add_cog(TwitterStreamer(bot))