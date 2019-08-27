import requests
import oauthlib
import json
import time
from requests.auth import HTTPBasicAuth


class song:
    def __init__(self, name, plays):
        self.name = name
        self.plays = plays

    def getName(self):
        return self.name

    def getPlays(self):
        return self.plays

    def song_exists(playcount, lst):
        for i in range(0, len(lst)):
            if playcount == lst[i].getPlays():
                return True
        return False


class newAlbum:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def getName(self):
        return self.name

    def getId(self):
        return self.id


def getArtistAlbums(artist_id, token):
    url = 'https://api.spotify.com/v1/artists/{}/albums?limit=50'.format(artist_id)
    auth = {'Authorization': 'Bearer {}'.format(token)}

    r = requests.get(url=url, headers=auth)
    resp = r.json()

    albums = []

    for i in range(len(resp['items'])):
        s = resp['items'][i].get('uri')
        s = s[14:]
        # print(resp['items'][i]['artists'])

        if resp['items'][i]['artists'][0].get('id') == artist_id:
            albums.append(s)


    return albums

def getName():
    url = 'https://api.spotify.com/v1/artists/{}/'.format(artist_id)
    auth = {'Authorization': 'Bearer {}'.format(token)}

    r = requests.get(url=url, headers=auth)
    resp = r.json()

    return resp['name']


def albumInSet(albums, id):
    for i in range(len(albums)):
        if id == albums[i].getId():
            return True

    return False


def albumToList(albumId):
    r = requests.get('https://t4ils.dev:4433/api/beta/albumPlayCount?albumid={}'.format(albumId))
    resp = r.json()
    json_data = json.dumps(resp)
    dict = json.loads(json_data)
    songs = []

    for i in range(0, len(dict['data'])):
        name = dict['data'][i]['name']
        playcount = dict['data'][i]['playcount']
        if not playcount in global_playcount:
            songs.append(song(name, playcount))
            global_playcount.append(playcount)

    return songs

start_time = time.time()

client_id = ''
client_secret = ''
auth_url = 'https://accounts.spotify.com/api/token'
data = {'grant_type': 'client_credentials'}

r = requests.post(url=auth_url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
resp = r.json()
token = resp['access_token']
# print(token)

print('Enter artist uri: ')
artist_id = input()[15:]
album_ids = getArtistAlbums(artist_id, token)

songs = []
global_playcount = []
for album_id in album_ids:
    songs += albumToList(album_id)

# sort song object list by most played
songs.sort(key=lambda x: x.getPlays(), reverse=True)

count = 1

with open('{}.txt'.format(getName()), 'w') as outputFile:
    for _songs in songs:
        line = ("{2}. {0} - {1} plays".format(_songs.getName(), '{:,}'.format(_songs.getPlays()), count))
        # print(line)
        outputFile.write(line + '\n')
        count += 1



print("%s seconds to execute" % (time.time() - start_time))

