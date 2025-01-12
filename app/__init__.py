'''
GarfieldsCatHair: Sasha M, Chloe W, Moyo F, Claire S
SoftDev
P02: TuneTown
2025-01-15
Time Spent:
'''

import os
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import setup_db as db
import spotify
import urllib.request
import json

app = Flask(__name__) 
secret = os.urandom(32)
app.secret_key = secret

key_id = None
key_secret = None

@app.route("/")
def home():
    if session.get("username") != None:
        return render_template("index.html", username = session.get("username"))
    return redirect(url_for("signup"))

@app.route("/indexTest")
def homepage():
    return render_template("index.html")

@app.route("/signup")
def signup():
    if session.get("username") != None:
        return redirect(url_for("home"))
    return render_template("signup.html")

@app.route("/response", methods=['POST', 'GET'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    users = [user[0] for user in db.getUsers()]
    if username in users:
        #flash message later?
        print("username already taken")
        return redirect(url_for("signup"))
    db.addUser(username, password)
    session["username"] = username
    session["password"] = password
    return redirect(url_for("home"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if (session.get('username') != None):
        return redirect(url_for("home"))
    print(request.args)
    print(request.form)
    if request.method == "POST" and db.validateUser(request.form.get("Username"), request.form.get("Password")):
        session["username"] = request.form.get("Username")
        session["password"] = request.form.get("Password")
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/profile")
def profile():
    if session.get("username") != None:
        username = session.get("username")
        pfp = db.getPfp(username)
        bg = db.getBg(username)
        am = db.getAM(username)
        return render_template("profile.html", username=username, pfp=pfp, bg=bg, am=am)
    return redirect(url_for("login"))

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    if session.get("username") == None:
        return redirect(url_for("login"))
    if request.method == "GET":
        username = session.get("username")
        pfp = db.getPfp(username)
        bg = db.getBg(username)
        am = db.getAM(username)
        return render_template("settings.html", username=username, pfp=pfp, bg=bg, am=am)
    db.changePfp(request.form.get("profile"), session.get("username"))
    db.changeBg(request.form.get("background"), session.get("username"))
    db.changeAM(request.form.get("about"), session.get("username"))
    return redirect(url_for("profile"))

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("home"))

@app.route("/search", methods=['GET', 'POST'])
def search():
    #retrieve keys and access token
    try:
        with open("app/keys/spotify_id.txt", "r") as file:
            key_id = file.read().strip()
    except:
        return error("Missing client ID for Spotify API")
    
    try:
        with open("app/keys/spotify_secret.txt", "r") as file:
            key_secret = file.read().strip()
    except:
        return error("Missing client secret for Spotify API")
    access_token = spotify.get_auth_token_header(key_id, key_secret)
    if not access_token:
        return error("Cannot retrieve access token for Spotify API")    
    #retrieve query and search type
    query = request.args.get("query")
    search_type = request.args.getlist("search_type")
    print(query)
    print(search_type)
    #search for ids
    search_ids = spotify.search(access_token, query, search_type)
    print(search_ids)
    #search for and render info
    data = {}
    if "artist" in search_type:
        artist_id = search_ids.get("artist")
        artist_data = spotify.artist_info(access_token, artist_id)
        data['artist'] = artist_data
    if "track" in search_type:
        track_id = search_ids.get("track")
        track_data = spotify.track_info(access_token, track_id)
        data['track'] = track_data
    if "album" in search_type:
        album_id = search_ids.get("album")
        album_data = spotify.album_info(access_token, album_id)
        data['album'] = album_data  
    return render_template("search.html", data=data)


@app.route("/error")
def error(message):
    return render_template("error.html", error = message)

if __name__ == "__main__":
    app.debug = True
    app.run()
