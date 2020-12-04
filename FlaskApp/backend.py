#!/usr/bin/python3
from flask import request
from data import database as db
from tools import spt_requests as sp

def app_auth():
	code = request.args['code']
	db.add_temp(code)
	auth_url = sp.get_authentication_url()
	return auth_url

def rtv_token():
	code = request.args['code']
	refresh_token = sp.get_refresh_token(code)
	discord_id = db.rtv_temp()
	discord_id = sp.get_discord_id(discord_id)
	db.add_spt_user(discord_id, refresh_token)
	db.remove_temp()
	return "Congratulations, authentication has been successful. You may now close this browser window."
