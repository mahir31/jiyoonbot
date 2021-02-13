import json
from aiohttp.client_exceptions import ClientResponseError
import requests
import os
import asyncio
from requests import exceptions
import aiohttp

from requests.models import HTTPError

OXFORD_DICTIONARY_APPLICATION_ID = os.environ["OXFORD_DICTIONARY_APPLICATION_ID"]
OXFORD_DICTIONARY_APPLICATION_KEY = os.environ["OXFORD_DICTIONARY_APPLICATION_KEY"]
OXFORD_DICTIONARY_ENDPOINT = 'https://od-api.oxforddictionaries.com'

async def internal_call(endpoint, source_lang, word_id):
    url = f'{OXFORD_DICTIONARY_ENDPOINT}/api/v2/{endpoint}/{source_lang}/{word_id}'
    headers = {
        "app_id":OXFORD_DICTIONARY_APPLICATION_ID,
        "app_key":OXFORD_DICTIONARY_APPLICATION_KEY
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data