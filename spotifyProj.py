import os
import sys
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# grace's username: 22727lpkw7t7zy7p2gicvwvgy
# nabeel: nabeelornodeal
# christy - spotify:user:1239606975

# grace
#clientid = "4f933fc7044d44d58ab19e959b76e243"
#secret = "325c926d068544cda714d024be6f96bd"

# nabeel
clientid = "b68e8f328092403f8c07380df2df2351"
secret = "b366d934eff740789e6eea7b402f0f03"
redirect = "http://localhost:8888/callback/"

# nabeel
# export SPOTIPY_CLIENT_ID='b68e8f328092403f8c07380df2df2351'
# export SPOTIPY_CLIENT_SECRET='b366d934eff740789e6eea7b402f0f03'
# export SPOTIPY_REDIRECT_URI='http://localhost:8888/callback/'

# class definition

class User:

    def __init__(self, username):
        self.username = username
        self.topTracks = {} # empty dict of top tracks (short, med, or long)

    def __str__(self):
        stri = ""
        for i in range(len(self.topTracks)):
            stri += self.topTracks[i] + ", "
        return "spotify user: " + self.username + ", spotify top tracks: " + stri + ""

    # term should be a list
    def getTopTracks(self, timespan):
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        self.toptracks = dict()
        #timespan can be short term, medium or long or any combination of them
        for term in timespan:
            print ("term: " + term)
            results = sp.current_user_top_tracks(time_range=term, limit=5)
            tracksList = []
            for i, item in enumerate(results['items']):
                # song//artist -- separate by '//'
                tracksList.append(item['name'] + "//" + item['artists'][0]['name'])
                print (str(i) + " " + item['name'] + ' // ' + item['artists'][0]['name'])
            self.toptracks[term] = tracksList
            print("")

    # term can be long, med and short term
    def analyzeMusic(self, term):
        if ((term != 'short_term') & (term != 'medium_term') & (term != 'long_term')):
            print('Term is not valid')
        #if (!((term == 'short_term') || (term == 'medium_term') || (term == 'long_term'))):
        #    print('Term is not valid')
        #    sys.exit()
        else:
            inputTerm = self.toptracks[term]
            for i in range(len(inputTerm)):
                termSplit = inputTerm[i].split('//')
                songName = termSplit[0]
                songArtist = termSplit[1]
 
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
token = util.prompt_for_user_token(username, scope, client_id=clientid, client_secret=secret,redirect_uri=redirect)

# create a new dictionary for user's top tracks
#toptracks = dict() #keys are term (short, long, medium)

# create new user
currUser = User(username)
print()

if token:
    #sp.trace = False
    timespan = ['short_term', 'medium_term', 'long_term']
    currUser.getTopTracks(timespan)
    print('test str method')
    print(str(currUser))

else:
    print("Can't get token for", username)


# find musicality features for top 5 short term songs

print('Musicality of top 5 tracks')
print()

currUser.analyzeMusic('short_term')



#should show the contents of every playlist owned by a user

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        print()
        track = item['track']
        print ((i, track['artists'][0]['name']))
        print(track['name'])

#sp = spotipy.Spotify(auth=token)
#playlists = sp.user_playlists(username)
#print('these are ' + username + 's playlists')
#print(playlists)
