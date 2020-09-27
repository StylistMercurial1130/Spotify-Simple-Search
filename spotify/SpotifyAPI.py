
import base64
import requests
import datetime
from urllib.parse import urlencode


class spotifyAPI :

    tokenURL = None
    client_id = None
    client_secret = None
    access_token = None
    expired = True
    client_OAUTH_status = False
    expires = datetime.datetime.now
    keyreference_albums = [
        'album_type',
        'artists',
        'id',
        'name'
    ]
    keyreference_artist = [
        'followers',
        'genres',
        'id',
        'name',
        'popularity'
    ]
    keyreference_track = [
        'album',
        'artists',
        'duration_ms',
        'id',
        'name',
        'populariy',
    ]
    response_types = [
        'artists',
        'albums',
        'tracks'
    ]

    def __init__(self,client_id,client_secret,tokenURL,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.client_id = client_id
        self.client_secret = client_secret
        self.tokenURL = tokenURL

        self.Authorize()

    def GetClientCred(self):

        client_id = self.client_id
        client_secret = self.client_secret

        if client_id == None or client_secret == None :
            raise Exception("! Empty/invalid client id or secret")

        clientCred = f'{client_id}:{client_secret}'
        b64_clientCred = base64.b64encode(clientCred.encode()) 

        return b64_clientCred.decode()

    def GetTokenData(self):

        tokenData = {
            "grant_type" : "client_credentials"        
        }

        return tokenData

    def GetTokenHeader(self):

        ClientCred  = self.GetClientCred()

        tokenHeader = {
            'Authorization' : f"Basic {ClientCred}"
        }

        return tokenHeader

    def Authorize(self):
        
        tokenURL = self.tokenURL
        tokenData = self.GetTokenData()
        tokenHeader = self.GetTokenHeader()

        Request = requests.post(tokenURL,data = tokenData,headers = tokenHeader)

        response = Request.json()

        if Request.status_code in range(200,299):
            now = datetime.datetime.now()
            self.access_token = response['access_token']
            expires_in = response['expires_in']
            self.expires = now + datetime.timedelta(seconds = expires_in)
            self.expired = self.expires < now
            self.client_OAUTH_status = True
        else:
            self.client_OAUTH_status = False
            raise Exception('autherization error ! Error'+str(Request.status_code))

    def CheckOAUTH(self):

        if self.client_OAUTH_status:
            return True
        else:
            return False

    def GenerateAccessToken(self):

        if self.access_token == None:
            self.Authorize()
        if self.expired == True:
            return self.GenerateAccessToken()

        if self.access_token != None and self.expired == False:
            return True

    def GlobalSearchQuery(self,query,searchType):
        query = urlencode({
            'q' : query,
            'type' : searchType
        })

        return query
    
    def GenerateHeader(self):

        if self.GenerateAccessToken() :
            accessToken = self.access_token
            Headers = {
                'Authorization' : f'Bearer {accessToken}'
            }
            return Headers
        else:
            raise Exception('acess token invalid/not generated !')

    def GlobalSearch(self,search,searchType):

        endpoint = 'https://api.spotify.com/v1/search'
        query = self.GlobalSearchQuery(search,searchType)
        Headers = self.GenerateHeader()
        searchURL = f'{endpoint}?{query}'

        Request = requests.get(searchURL,headers = Headers)

        if Request.status_code not in range(200,299):
            raise Exception('Error',Request.status_code)
        else:
            return Request.json()


    def GenerateSearchDict(self,resDict):
        
        search_type = None
        keywords = None
        data = []
        dataDict = {}

        for i in resDict:
            if i in self.response_types:
                search_type = i
            else:
                raise Exception('search type inalid !')

        if search_type == 'artists':
            keywords = self.keyreference_artist
        else:
            if search_type == 'albums':
                keywords = self.keyreference_albums
            else:
                keywords = self.keyreference_track

        for i in resDict.get(search_type).get('items'):
            field = {}
            for j in i:
                for key in keywords:
                    field[key] = i.get(key)
            data.append(field)

        dataDict['query'] = data

        return dataDict
        




