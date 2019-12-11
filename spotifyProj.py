import os
import sys
import json
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# authentication requirements
clientid = "b68e8f328092403f8c07380df2df2351"
secret = "b366d934eff740789e6eea7b402f0f03"
redirect = "http://localhost:8888/callback/"

# user class stores top tracks and other important musical info
class User:
    toptracks = {}
    topURIs = {}
    recommendations = []
    def __init__(self, username):
        self.username = username
        self.toptracks = {} # empty dict of top tracks (short, med, or long)
        self.recommendations = []

    def __str__(self):
        timespan = ['short_term', 'medium_term', 'long_term']
        stri = ""
        for term in timespan:
            stri += "Your Spotify top "
            if term == 'short_term':
                stri += 'short term '
            elif term == 'medium_term':
                stri += 'medium term '
            else:
                stri += 'long term '
            stri += 'tracks are: '
            for i in range(len(self.toptracks[term])- 1):
                stri += self.toptracks[term][i] + ", "
            stri += "and "
            stri += self.toptracks['short_term'][len(self.toptracks['short_term']) - 1]
            stri += ". \n"
        return stri

    # term should be a list
    def getTopTracks(self, timespan):
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        self.toptracks = dict()
        #timespan can be short term, medium or long or any combination of them
        for term in timespan:
            print ("term: " + term)
            results = sp.current_user_top_tracks(time_range=term, limit=5)
            #self.toptracks = results
            tracksList = []
            uriList = []
            for i, item in enumerate(results['items']):
                # song//artist -- separate by '//'
                tracksList.append(item['name'] + "//" + item['artists'][0]['name'])
                uriList.append(item['uri'])
                print (str(i) + " " + item['name'] + ' // ' + item['artists'][0]['name'])
            self.toptracks[term] = tracksList
            self.topURIs[term] = uriList
            print("")

    # term can be long, med or short term
    def analyzeMusic(self, term):
        if ((term != 'short_term') & (term != 'medium_term') & (term != 'long_term')):
            print('Term is not valid')
            sys.exit()
        else:
            inputTerm = self.toptracks[term]
            # separate artist and song name
            for i in range(len(inputTerm)):
                termSplit = inputTerm[i].split('//')
                songName = termSplit[0]
                songArtist = termSplit[1]

                sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
                sp.trace=False

                # this finds the song with the artist and song name
                results = sp.search(q='artist:' + songArtist + ' track:' + songName, type='track', limit = 1)

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

                self.averages = dict()
                print()
                print('*****************')
                print()

    def getRecs(self, timespan):
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        inputTerm = self.toptracks[timespan]
        seed = self.topURIs[timespan]
        k = sp.recommendations(seed_artists=None, seed_genres=None, seed_tracks=seed, limit=10, country=None)
        for i in range(0, 10):
            print (k['tracks'][i]['name']+'//'+k['tracks'][i]['artists'][0]['name'])
            self.recommendations.append(k['tracks'][i]['name']+'//'+k['tracks'][i]['artists'][0]['name'])

client_credentials_manager = SpotifyClientCredentials(client_id=clientid,
                                                      client_secret=secret)

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


# create new user
currUser = User(username)

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

print('Recommended songs')
currUser.getRecs('short_term')


#should show the contents of every playlist owned by a user
def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print ((i, track['artists'][0]['name']))
        print(track['name'])
