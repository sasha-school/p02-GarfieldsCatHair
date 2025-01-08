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

#search_type is a list
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
            print(f"no {search_type} found") ## modify
        else: 
            output[t]= json_items[0]["id"]
    return output #returns dictionary with keys corresponding to all search_type parameters that find results

#def artist_info(token_header, id):
#def album_info(token_header, id):
#def track_info(token_header, id):