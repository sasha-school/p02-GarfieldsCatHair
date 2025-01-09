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

@app.route("/response" , methods=['POST', 'GET'])
def register():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    db.addUser(name, username, password)
    session["name"] = name
    session["username"] = username
    session["password"] = password
    return redirect(url_for("home"))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if (session.get('username') != None):
        return redirect(url_for("home"))
    print(request.args)
    print(request.form)
    #fix validation!!
    if request.method == "POST" and db.validateUser(request.form.get("usernameL"), request.form.get("passwordL")):
        session["username"] = request.form.get("usernameL")
        session["name"] = db.getName(session["username"])
        session["password"] = request.form.get("passwordL")
        return redirect(url_for("home"))
    return render_template("signin.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    session.pop("password", None)
    session.pop("name", None)
    return redirect(url_for("home"))

@app.route("/signup")
def signup():
    return render_template("signup.html")