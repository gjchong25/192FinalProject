# https://github.com/plamere/spotipy/blob/master/spotipy/util.py
# http://www.acmesystems.it/python_httpd
from flask import Flask, jsonify, request, render_template, url_for
app = Flask(__name__)
from bottle import route, run, request, redirect
import spotipy
from spotipy import oauth2
import os
import sys
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
#from userdef import User



PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = '4f933fc7044d44d58ab19e959b76e243'
SPOTIPY_CLIENT_SECRET = '325c926d068544cda714d024be6f96bd'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )
tracks = {}

@app.route("/")
def index():
    #print("now im here")
    return "this is the splash screen"

@app.route('/login')
def login():
    return htmlForLoginButton()

@app.route('/success')
def success():

    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        #return results['id']
        return getTopTracks(results['id'], sp) # get username unique id

    else:
        return htmlForLoginButton()

def getTopTracks(results, sp):

    #scope = 'user-top-read'
    #token = util.prompt_for_user_token(results, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI )
    #if token:
        timespan = ['short_term', 'medium_term', 'long_term']

        #sp = spotipy.Spotify(auth=token)
        sp.trace = False
        toptracks = dict()
        #timespan can be short term, medium or long or any combination of them
        for term in timespan:
            print ("term: " + term)
            results = sp.current_user_top_tracks(time_range=term, limit=5)
            tracksList = []
            for i, item in enumerate(results['items']):
                # song//artist -- separate by '//'
                tracksList.append(item['name'] + "//" + item['artists'][0]['name'])
                print (str(i) + " " + item['name'] + ' // ' + item['artists'][0]['name'])
            toptracks[term] = tracksList
            print("")
        tracks = toptracks
        print('THIS IS TRACKS')
        print(tracks)
        return toptracks
    #else:
        #return "token didnt work this time"

@app.route('/short_term')
def short():
    return analyzeMusic('short_term', tracks)

@app.route('/medium_term')
def med():
    return analyzeMusic('medium_term', tracks)

@app.route('/long_term')
def long():
    return analyzeMusic('long_term', tracks)


def analyzeMusic(term, tracks):

    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                          client_secret=SPOTIPY_CLIENT_SECRET)
    tracks = {'short_term': ['Ball For Me (feat. Nicki Minaj)//Post Malone', 'Press//Cardi B', 'Wow.//Post Malone', '100 Bad Days//AJR', 'Circles//Post Malone'], 'medium_term': ['hot girl bummer//blackbear', 'Ball For Me (feat. Nicki Minaj)//Post Malone', 'Wow.//Post Malone', 'SICKO MODE//Travis Scott', "fuck, i'm lonely (with Anne-Marie) - from “13 Reasons Why: Season 3”//Lauv"], 'long_term': ['Somebody Else//The 1975', 'Vanessa//Lostboycrow', 'Ode to Sleep//Twenty One Pilots', 'PILLOWTALK//ZAYN', 'Car Radio//Twenty One Pilots']}
    print(tracks)
    if ((term != 'short_term') & (term != 'medium_term') & (term != 'long_term')):
        print('Term is not valid')
        sys.exit()
    else:
        inputTerm = tracks[term]
        dict = {}
        for i in range(len(inputTerm)):
            termSplit = inputTerm[i].split('//')
            songName = termSplit[0]
            songArtist = termSplit[1]

            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
            sp.trace=False

            # results = sp.search(q=artist_name, limit=1)
            # this finds the song with the artist and song name
            results = sp.search(q='artist:' + songArtist + ' track:' + songName, type='track', limit = 1)

            #print(results["tracks"]['items']) --> gives you more info
            print('Name of Artist: ' + results["tracks"]['items'][0]['artists'][0]['name'])
            print('Name of Song: ' + results["tracks"]['items'][0]['name'])
            print('Song URI: ' + results["tracks"]['items'][0]['uri'])
            print()

            tids = []
            for i, t in enumerate(results['tracks']['items']):
                # unique track (song) id
                tids.append(t['uri'])


            features = sp.audio_features(tids)
            for feature in features:
                # feature contains all the musical characteristics we want
                print(json.dumps(feature, indent=4))
                dict[results["tracks"]['items'][0]['name']] = feature
                analysis = sp._get(feature['analysis_url'])

            print()
            print('*****************')
            print()
        return dict


def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

#run(host='', port=8080)
if __name__ == "__main__":
    app.run(port=8080, debug=True)
