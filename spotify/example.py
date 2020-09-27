''' 
    getting details of an 'artist' by the name 'joji
'''


import SpotifyAPI as spotify
import os
import json
import pprint

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret_key = os.getenv("SPOTIFY_CLIENT_SECRET_KEY")
tokenURL = 'https://accounts.spotify.com/api/token'

client = spotify.spotifyAPI(client_id,client_secret_key,tokenURL)

if(client.CheckOAUTH()):
    respone = client.GlobalSearch('joji','artist')
    responseDict = json.loads(json.dumps(respone))
    data = client.GenerateSearchDict(responseDict)
    pprint.pprint(data)
else:
    raise Exception('Error !')