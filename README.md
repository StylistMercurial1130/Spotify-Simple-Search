# Spotify-Simple-Search

simple spotify searcher using python 3.8 

# Modules Used 
1. os
2. requests
3. json
4. urlibparse


# Authorization 

A client id and a client secret id is to be entered for autherization 

```python
def __init__(self,client_id,client_secret,tokenURL,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.client_id = client_id
        self.client_secret = client_secret
        self.tokenURL = tokenURL

        self.Authorize()
```

Spotify API being a class, when a object is made of the class the autherization is handled and there is no need to autherize manually 

```python
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
```

## Capability of the Spotify Simple Search
As the name suggests being a simple search, the search capability is not vast and modular. Only cerain query can be searched for based on a searchtype. the data returned is in the form of a python dictionary. the contents of the dictionry are according to the search type 

```pyhton
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
```

```python
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
```
Along with the source code an example snippet is attached to better understand the capabilities of the spotify simple search 

Any improvement is welcomed :)
