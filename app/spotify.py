'''
GarfieldsCatHair: Sasha M, Chloe W, Moyo F, Claire S
SoftDev
P02: TuneTown
2025-01-15
Time Spent: 2 hours
'''

import base64
from requests import post, get
import json

#converting javascript code from documentation into python, converting ascii to regular
def get_auth_token_header(client_id, client_secret): #https://developer.spotify.com/documentation/web-api/tutorials/getting-started
    s = client_id +":"+ client_secret
    s = str(base64.b64encode(s.encode("utf-8")), "utf-8") #encodes information as base64
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": "Basic " + s,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    result = post(url, headers=headers, data=data) #returns access token valid for 1 hour
    token = json.loads(result.content)
    return{"Authorization": "Bearer " + token["access_token"]} #https://developer.spotify.com/documentation/web-api/concepts/access-token

#search_type is a list of ["artist", "album", "track"] in any combination
def search(token_header, query, search_type): #https://developer.spotify.com/documentation/web-api/reference/search
    type ="" #string of search_types, comma separated
    for item in search_type:
        type = type + item + ","
    type = type[:-1]
    query = f"https://api.spotify.com/v1/search?q={query}&type={type}&limit=1" #searches 1, limit can be modified
    result = get(query, headers=token_header)
    output = {}
    for t in search_type:
        json_items = json.loads(result.content)[f"{t}s"]["items"]
        if (len(json_items)==0):
            print(f"no {search_type} found")
        else:
            output[t]= json_items[0]["id"]
    return output #returns dictionary, keys are search_type, values are ids

#returns [artist_name, artist_image, [genres], [albums], [top_tracks]]
def artist_info(token_header, id):
    output = {}
    query = f"https://api.spotify.com/v1/artists/{id}"
    result = get(query, headers=token_header)
    json_items = json.loads(result.content)
    output['artist_name'] = json_items['name']
    output['artist_image'] = json_items['images'][0]['url']
    output['genres'] = json_items['genres']
    query = f"https://api.spotify.com/v1/artists/{id}/albums?limit=5" #searches for 5, limit can be modified
    result = get(query, headers=token_header)
    json_items = json.loads(result.content)
    albums = []
    for album in json_items['items']:
        albums += [album['name']]
    output['albums'] = albums
    query = f"https://api.spotify.com/v1/artists/{id}/top-tracks"
    result = get(query, headers=token_header)
    json_items = json.loads(result.content)
    tracks = []
    for track in json_items['tracks']:
        tracks += [track['name']]
    output['top_tracks'] = tracks
    return(output) #returns dictionary

#returns [track_name, album_image, artist_name, album_name, release_date, duration]
def track_info(token_header, id):
    output = {}
    query = f"https://api.spotify.com/v1/tracks/{id}"
    result = get(query, headers=token_header)
    json_items = json.loads(result.content)
    output['track_name'] = json_items['name']
    output['album_image'] = json_items['album']['images'][0]['url']
    output['artist_name'] = json_items['artists'][0]['name']
    output['album_name'] = json_items['album']['name']
    output['release_date'] = json_items['album']['release_date']
    minutes, seconds = divmod(json_items['duration_ms'] // 1000, 60)
    output['duration'] = f"{minutes}:{seconds}"
    return(output) #returns dictionary

#returns [album_name, album_image, artist_name, release_date, [tracks]]
def album_info(token_header, id):
    output = {}
    query = f"https://api.spotify.com/v1/albums/{id}"
    result = get(query, headers=token_header)
    json_items = json.loads(result.content)
    output['album_name'] = json_items['name']
    output['album_image'] = json_items['images'][0]['url']
    output['artist_name'] = json_items['artists'][0]['name']
    output['release_date'] = json_items['release_date']
    tracks = []
    for track in json_items['tracks']['items']:
        tracks += [track['name']]
    output['tracks'] = tracks
    return(output) #returns dictionary

#from spotifys website
def get_embed_html(token_header, category, id):
    return f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/{category}/{id}?utm_source=generator" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
