from flask import Flask, jsonify, request, render_template, url_for, redirect
import json
import requests
from urllib.parse import quote
import spotipy
from spotipy import oauth2
import os
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

#authentication required fields
clientid = "4f933fc7044d44d58ab19e959b76e243"
secret = "325c926d068544cda714d024be6f96bd"
redirect_uri = "http://localhost:8080/callback"
client_credentials_manager = SpotifyClientCredentials(client_id=clientid,
                                                      client_secret=secret)

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "client_id": clientid
}

# may need to sign into spotify
@app.route("/")
def index():
    # Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format("https://accounts.spotify.com/authorize", url_args)
    return redirect(auth_url)

# a side function that gets the users top tracks
def topTracks(userid):
    scope = 'user-top-read'
    token = util.prompt_for_user_token(userid, scope, client_id=clientid, client_secret=secret,redirect_uri=redirect_uri )

    sp = spotipy.Spotify(auth=token)
    timespan = ['short_term', 'medium_term', 'long_term']

    sp.trace = False
    #store top short, med and long term tracks in dictionary
    toptracks = dict()
    #timespan can be short term, medium or long or any combination of them
    for term in timespan:
        results = sp.current_user_top_tracks(time_range=term, limit=5)
        tracksList = []
        for i, item in enumerate(results['items']):
            tracksList.append(item['name'] + "//" + item['artists'][0]['name'])
            #print (str(i) + " " + item['name'] + ' // ' + item['artists'][0]['name'])
        toptracks[term] = tracksList
    tracks = toptracks

    return toptracks
 
# homepage
@app.route('/homepage')
def homepage():
    user = request.args.get('user')
    display = request.args.get('display')
    return render_template('splash.html', name = user, display = display)

# gets dictionary of all top tracks
@app.route('/alltoptracks/<name>')
def alltoptracks(name):
    tracks = topTracks(name)
    return render_template('overalltop.html', name = name, tracks = tracks)

    #return topTracks(name)

# gets short term top tracks for user
@app.route('/short/<name>')
def short(name):
    scope = 'user-top-read'
    token = util.prompt_for_user_token(name, scope, client_id=clientid, client_secret=secret,redirect_uri=redirect_uri )

    sp = spotipy.Spotify(auth=token)
    timespan = ['short_term']

    sp.trace = False
    toptracks = dict()
    for term in timespan:
        # search by time range and limit to 5
        results = sp.current_user_top_tracks(time_range=term, limit=5)
        tracksList = []
        for i, item in enumerate(results['items']):
            tracksList.append(item['name'] + "//" + item['artists'][0]['name'])
        toptracks[term] = tracksList
    tracks = toptracks
    shorttracks = analyzeMusic(toptracks, 'short_term')
    return render_template('topsongs.html', name = name, tracks = shorttracks)
    #return analyzeMusic(toptracks, 'short_term')

# gets medium term top tracks for user
@app.route('/medium/<name>')
def medium(name):
    scope = 'user-top-read'
    token = util.prompt_for_user_token(name, scope, client_id=clientid, client_secret=secret,redirect_uri=redirect_uri )

    sp = spotipy.Spotify(auth=token)
    timespan = ['medium_term']

    sp.trace = False
    toptracks = dict()
    for term in timespan:
        results = sp.current_user_top_tracks(time_range=term, limit=5)
        tracksList = []
        for i, item in enumerate(results['items']):
            tracksList.append(item['name'] + "//" + item['artists'][0]['name'])
        toptracks[term] = tracksList
    tracks = toptracks
    #return analyzeMusic(toptracks, 'medium_term')
    medtracks = analyzeMusic(toptracks, 'medium_term')
    return render_template('topsongs.html', name = name, tracks = medtracks)

# gets long term top tracks for user
@app.route('/long/<name>')
def long(name):
    scope = 'user-top-read'
    token = util.prompt_for_user_token(name, scope, client_id=clientid, client_secret=secret,redirect_uri=redirect_uri )

    sp = spotipy.Spotify(auth=token)
    timespan = ['long_term']

    sp.trace = False
    toptracks = dict()
    for term in timespan:
        results = sp.current_user_top_tracks(time_range=term, limit=5)
        tracksList = []
        for i, item in enumerate(results['items']):
            tracksList.append(item['name'] + "//" + item['artists'][0]['name'])
        toptracks[term] = tracksList
    tracks = toptracks
    longtracks = analyzeMusic(toptracks, 'long_term')
    return render_template('topsongs.html', name = name, tracks = longtracks)

# function to analyze music characteristics of songs
def analyzeMusic(toptracks, term):
    songWithMusicality = dict()
    inputTerm = toptracks[term]
    for i in range(len(inputTerm)):
        termSplit = inputTerm[i].split('//')
        songName = termSplit[0]
        songArtist = termSplit[1]

        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        sp.trace=False

        # this finds the song with the artist and song name
        results = sp.search(q='artist:' + songArtist + ' track:' + songName, type='track', limit = 1)

        tids = []
        for i, t in enumerate(results['tracks']['items']):
            # unique track (song) id
            tids.append(t['uri'])

        features = sp.audio_features(tids)
        for feature in features:
            # key is song name, value is musical features
            songWithMusicality[results["tracks"]['items'][0]['name']] = feature
            analysis = sp._get(feature['analysis_url'])

    return songWithMusicality


@app.route("/callback")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": redirect_uri,
        'client_id': clientid,
        'client_secret': secret,
    }
    post_request = requests.post("https://accounts.spotify.com/api/token", data=code_payload)

    # access token needed to use spotify api
    response = json.loads(post_request.text)
    print(response)
    access_token = response["access_token"]
    authHeader = {"Authorization": "Bearer {}".format(access_token)}

    # data about profile
    user_profile_api_endpoint = "{}/me".format("{}/{}".format("https://api.spotify.com", "v1"))
    profiledata = requests.get(user_profile_api_endpoint, headers=authHeader)
    userData = json.loads(profiledata.text)
    username = userData['id']
    print(username)

    #return userData
    #return render_template('splash.html', name = userData['display_name'])
    #return getTopTracks(userData['id'])
    return redirect(url_for('homepage', user = userData['id'], display = userData['display_name']))

# run the port 8080
if __name__ == "__main__":
    app.run(port=8080, debug=True)
