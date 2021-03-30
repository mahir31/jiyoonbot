#!/usr/bin/python3
import os
import urllib
from base64 import b64encode
import requests
import aiohttp

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
DISCORD_CLIENT_ID = os.environ['JIYOON_BOT_DISCORD_CLIENT_ID']
DISCORD_CLIENT_SECRET = os.environ['JIYOON_BOT_DISCORD_CLIENT_SECRET']
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_ENDPOINT = 'https://api.spotify.com'
DISCORD_API_ENDPOINT = 'https://discord.com/api/v8'
CLIENT_URL = 'https://jiyoonbot.xyz'
SPOTIFY_REDIRECT_URI = f'{CLIENT_URL}/callback/q/'
DISCORD_REDIRECT_URI = f'{CLIENT_URL}/callback/sp/'
SPOTIFY_SCOPE = 'user-read-recently-played user-read-currently-playing user-top-read user-read-private'
DISCORD_SCOPE = 'identify'

def encode_authorization_string():
    encoded_authorization_str = f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'
    encoded_authorization_str = encoded_authorization_str.encode('utf-8')
    encoded_authorization_str = b64encode(encoded_authorization_str)
    encoded_authorization_str = encoded_authorization_str.decode('utf-8')
    return encoded_authorization_str

def get_authentication_url():
    auth_query_parameters = {
		'response_type': 'code',
		'redirect_uri': SPOTIFY_REDIRECT_URI,
		'scope': SPOTIFY_SCOPE,
		'client_id': SPOTIFY_CLIENT_ID
	}
    url_args = '&'.join([f'{key}={urllib.parse.quote(val)}' for key,val in auth_query_parameters.items()])
    auth_url = f'{SPOTIFY_AUTH_URL}/?{url_args}'
    return auth_url

def get_refresh_token(code):
    payload = {
		'grant_type': 'authorization_code',
		'code': str(code),
		'redirect_uri': SPOTIFY_REDIRECT_URI
	}
    headers = {'Authorization': f'Basic {encode_authorization_string()}'}
    response = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    response = response.json()
    refresh_token = response['refresh_token']
    return refresh_token

def get_discord_id(code):
    payload = {
		'client_id': DISCORD_CLIENT_ID,
		'client_secret': DISCORD_CLIENT_SECRET,
		'grant_type': 'authorization_code',
        'code': code,
		'redirect_uri': DISCORD_REDIRECT_URI,
		'scope': DISCORD_SCOPE
	}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post('%s/oauth2/token' % DISCORD_API_ENDPOINT, data=payload, headers=headers)
    response = response.json()
    access_token = response['access_token']
    headers = {'authorization': f'Bearer {access_token}'}
    user_id = requests.get(f'{DISCORD_API_ENDPOINT}/users/@me', headers=headers)
    user_id = user_id.json()
    user_id = user_id['id']
    return user_id

async def get_access_token(refresh_token):
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {'authorization': f'Basic {encode_authorization_string()}'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers) as response:
                data = await response.json()
                return data['access_token']
    except requests.exceptions.HTTPError as http_error:
        result = 'error: ' + str(http_error)
        return result

async def internal_call(url, access_token):
    headers = {'authorization': f'Bearer {access_token}'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{SPOTIFY_API_ENDPOINT}{url}', headers=headers) as response:
                data = await response.json(content_type=None)
                return data
    except requests.exceptions.HTTPError as http_error:
        result = 'error: ' + str(http_error)
        return result