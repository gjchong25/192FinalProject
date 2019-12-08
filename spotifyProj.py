from __future__ import print_function
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
#idk if we need this
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
import time

# get username from terminal
#username = sys.argv[1]

#user ID: 22727l
# or user ID: 22727lpkw7t7zy7p2gicvwvgy?si=e75O1nb5TP6W6Gtao1N3nw ??
#https://open.spotify.com/user/22727lpkw7t7zy7p2gicvwvgy?si=e75O1nb5TP6W6Gtao1N3nw
#spotify:user:22727lpkw7t7zy7p2gicvwvgy

# CIS 192 app on Python
clientid = "4f933fc7044d44d58ab19e959b76e243"
secret = "325c926d068544cda714d024be6f96bd"

# this is the redirect url
#export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback/'


client_credentials_manager = SpotifyClientCredentials(client_id=clientid,
                                                      client_secret=secret)
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#scope = 'user-library-read'


# get user's top artists and tracks based on calculated affinity ??
# does this with user behavior and play history

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" + (sys.argv[0]))
    sys.exit()

scope = 'user-top-read'
token = util.prompt_for_user_token(username, scope)

# create a new dictionary for user's top tracks
toptracks = dict() #sort term

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    timespan = ['short_term', 'medium_term', 'long_term']
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

print('Now printing top tracks: ')
print(toptracks)

# focus on short term, find musicality features for top 5 songs



print('')
print('billie eilish musicality')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

'''
if len(sys.argv) > 1:
    artist_name = ' '.join(sys.argv[1:])
else:
    artist_name = 'Billie Eilish'
'''
artist_name = 'Billie Eilish'
results = sp.search(q=artist_name, limit=2)
#dict_keys(['href', 'items', 'limit', 'next', 'offset', 'previous', 'total'])
print(results["tracks"]['items'])
print('')
print('**************************')
print('')



tids = []
for i, t in enumerate(results['tracks']['items']):
    print(' ' + str(i) + " " + t['name'])
    tids.append(t['uri'])

start = time.time()
features = sp.audio_features(tids)
delta = time.time() - start
for feature in features:
    print()
    print('-------------------------')
    print()
    #print(json.dumps(feature, indent=4))
    #print()
    analysis = sp._get(feature['analysis_url'])
    print(json.dumps('tempo: ' + str(analysis["track"]["tempo"])))
    print(json.dumps('duration: ' + str(analysis["track"]["duration"])))
    print(json.dumps('loudness: ' + str(analysis["track"]["loudness"])))
    print(json.dumps('end_of_fade_in: ' + str(analysis["track"]["end_of_fade_in"])))
    print(json.dumps('start_of_fade_out: ' + str(analysis["track"]["start_of_fade_out"])))
    print(json.dumps('time_signature: ' + str(analysis["track"]["time_signature"])))
    print(json.dumps('key: ' + str(analysis["track"]["key"])))
    print(json.dumps('duration: ' + str(analysis["track"]["duration"])))
    print(json.dumps('rhythm_version: ' + str(analysis["track"]["rhythm_version"])))

print ("features retrieved in %.2f seconds" + str(delta))


'''
 
#spotify:artist:6LuN9FCkKOj5PcnpouEgny
#spotify:track:0u2P5u6lvoDfwTYjAADbn4



# should show the contents of every playlist owned by a user

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print ((i, track['artists'][0]['name']))
        print(track['name'])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print ("Whoops, need your username!")
        print ("usage: python user_playlists.py [username]")
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print (playlist['name'])
                print ('  total tracks', playlist['tracks']['total'])
                results = sp.user_playlist(username, playlist['id'],
                    fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print ("Can't get token for", username)
'''
