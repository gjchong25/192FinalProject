from __future__ import print_function
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import time

# grace's username: 22727lpkw7t7zy7p2gicvwvgy

# grace
#clientid = "4f933fc7044d44d58ab19e959b76e243"
#secret = "325c926d068544cda714d024be6f96bd"

# nabeel
clientid = "b68e8f328092403f8c07380df2df2351"
secret = "b366d934eff740789e6eea7b402f0f03"

# nabeel
# export SPOTIPY_CLIENT_ID='b68e8f328092403f8c07380df2df2351'
# export SPOTIPY_CLIENT_SECRET='b366d934eff740789e6eea7b402f0f03'
# export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback/'


client_credentials_manager = SpotifyClientCredentials(client_id=clientid,
                                                      client_secret=secret)
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#scope = 'user-library-read'

# get user's top artists and tracks based on calculated affinity
# does this with user behavior and play history

if len(sys.argv) > 1:
    username = sys.argv[1]
    print('current username: ' + username)
else:
    print('There was no username provided as an argument.')
    sys.exit()

scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope)

# create a new dictionary for user's top tracks
toptracks = dict() #keys are term (short, long, medium)

if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    print('')
    print('')
    print('these are nabeels playlists')
    #print(playlists)

    sp.trace = False
    timespan = ['short_term', 'medium_term', 'long_term']
    #timespan = ['short_term']
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
else:
    print("Can't get token for", username)


# focus on short term, find musicality features for top 5 songs

print()
print('Musicality of top 5 short term tracks')
print()

shortTerm = toptracks['short_term']
print()
for i in range(len(shortTerm)):
    shortTermSplit = shortTerm[i].split('//')
    songName = shortTermSplit[0]
    songArtist = shortTermSplit[1]

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False

    # results = sp.search(q=artist_name, limit=1)
    # this finds the song with the artist and song name
    results = sp.search(q='artist:' + songArtist + ' track:' + songName, type='track', limit = 1)

    # in results['track']['items'][0].keys() --> dict_keys(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri'])
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
        analysis = sp._get(feature['analysis_url'])

    print()
    print('*****************')
    print()


 #should show the contents of every playlist owned by a user

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        print()
        track = item['track']
        print ((i, track['artists'][0]['name']))
        print(track['name'])


#spotify:artist:6LuN9FCkKOj5PcnpouEgny
#spotify:track:0u2P5u6lvoDfwTYjAADbn4
