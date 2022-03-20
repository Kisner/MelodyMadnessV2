import secrets
from flask import Flask, render_template, request, flash, redirect, url_for
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

@app.route("/", methods=['GET'])
@app.route("/home/", methods=['GET'])
def home():
	return render_template('welcome.html', nav='home')

@app.route('/auth')
def spotify_auth():
	CID = ''
	SECRET = ''
	resp = 0
	request = ''

    # Gets user log in, collects their listening data, returns JSON file of that data
	REDIR_URL = 'http://localhost:8888/callback'

    # temp_list grabs data of top 16 sp artists (long term), user_creds grabs name, id, email from auth'd user
	temp_list = []
    # user_creds = []

    # This block authenticates user login via the API & grabs a temp token
	oauth = SpotifyOAuth(client_id=CID, client_secret=SECRET, redirect_uri=REDIR_URL, scope='user-top-read')
	sp_auth = spotipy.Spotify(auth_manager=oauth)

    # populates user's top 16 artists from raw json -> []
	if sp_auth:
		results = sp_auth.current_user_top_artists(limit=16, offset=0, time_range='long_term')
		for s in range(16):
			temp_list.append(results)

	else:
        # if authentication doesn't work, bad req
		resp = 400

    # data_list = top 16 artist data for a user
	data_list = temp_list[0]['items']

	ParseData(data_list)

	try:
		os.remove('.cache')
	except OSError:
		pass

	if resp == 400:
		request = "ERROR"
	else:
		request = generate(request)
	return request

@app.route('/gen')
def generate(request):
	return render_template('index.html', nav='home')

@app.route('/test')
def test():
	print('test')
	return 'test'



# ParseData(data)
# parses the raw JSON into data needed for the bracket. Data is stored in the Artist model -> db.
def ParseData(data):
	artists = []
	artists_uri = []
	artists_popularity = []
	artists_genres = []
	image_links = []

    # parses JSON into pandas dataframe
	for token in data:
        # Artist name
		artists_name = token['name']
		artists.append(artists_name)

        # Spotify URI for artist (eg: spotify:artist:xxx...)
		artist_uri = token['uri']
		artists_uri.append(artist_uri)

        # For image link indexing and image sizes. img[1] = 300x300 dimensions
		image_link = token['images'][1]['url']
		image_links.append(image_link)

        # Integer value Spotify API returns for an artist's popularity
		popularity = token['popularity']
		artists_popularity.append(popularity)

        # genre[0] = top genre selected for an artist, sometimes Spotify returns multiple genre options.
		genre = token['genres'][0]
		artists_genres.append(genre)

    # df setup
	artist_frame = pd.DataFrame(
        {
            'artist': artists,
            'artist_uri': artists_uri,
            'artists_genres': artists_genres,
            'artist_popularity': artists_popularity,
            'artist_image': image_links
        }
    )
	artist_frame.to_csv('artistData.csv')

#not found route 
# @app.errorhandler(404)
# def page_not_found(e):
# 	return render_template('404.html', title="Not Found"), 404

#https://stackoverflow.com/questions/63530652/storing-and-accessing-dictionary-data-in-flask

if __name__ == '__main__':
	app.run()