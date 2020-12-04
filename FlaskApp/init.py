from flask import Flask, render_template, redirect
from backend import app_auth, rtv_token

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/authorise/')
def dis_auth():
	return redirect('https://discord.com/api/oauth2/authorize?client_id=763475902339350608&redirect_uri=https%3A%2F%2Fjiyoonbot.xyz%2Fcallback%2Fsp%2F&response_type=code&scope=identify')

@app.route('/callback/sp/')
def sp_auth():
	auth_url=app_auth()
	return redirect(auth_url)

@app.route('/callback/q/')
def token_page():
	response=rtv_token()
	return(response)