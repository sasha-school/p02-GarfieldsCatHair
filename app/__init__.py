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

@app.route("/")
def home():
    if session.get("username") != None:
        
        
        
        return render_template("index.html")
    return redirect(url_for("signup"))

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/response", methods=['POST', 'GET'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
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
    if request.method == "POST" and db.validateUser(request.form.get("username"), request.form.get("password")):
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop("username", None)
    session.pop("password", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
