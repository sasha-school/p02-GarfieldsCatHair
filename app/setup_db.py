'''
GarfieldsCatHair: Sasha M, Chloe W, Moyo F, Claire S
SoftDev
P02: TuneTown
2025-01-15
Time Spent:
'''

import sqlite3
from flask import session


#connects to SQLite database, creates if not already made
db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()

#user table
def userTable():
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, pfp TEXT NOT NULL, bg_image TEXT NOT NULL, about_me TEXT NOT NULL)")
    db.commit()

#posts table
def testTable0():
    cursor.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY, username TEXT, post TEXT)") 
    db.commit()

userTable()
testTable0()

# User Helpers
def addUser(username, password):
    default_pfp = "https://i.pinimg.com/736x/a6/be/9c/a6be9ced2fd7a0884518e3535ff0bce8.jpg"
    default_bg_image = "https://raw.githubusercontent.com/sasha-school/p02-GarfieldsCatHair/refs/heads/main/flag.jpg"
    default_about_me = "about me!"
    cursor.execute("INSERT INTO users(username, password, pfp, bg_image, about_me) VALUES (?, ?, ?, ?, ?)", (username, password, default_pfp, default_bg_image, default_about_me))
    db.commit()

def getUsers():
    return cursor.execute("SELECT username FROM users").fetchall()

def removeUser(id):
    cursor.execute(f"DELETE FROM users WHERE id='{id}'")
    db.commit()

def validateUser(username, password):
    users = [user[0] for user in getUsers()]
    if username not in users:
        return False
    dbPassword = getPassword(username)
    if dbPassword:
        return (dbPassword==password)
    return False

def getId(username):
    return cursor.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()[0]

def getPassword(username):
    return cursor.execute(f"SELECT password FROM users WHERE username='{username}'").fetchone()[0]

def getPfp(username):
    return cursor.execute(f"SELECT pfp FROM users WHERE username='{username}'").fetchone()[0]

def getBg(username):
    return cursor.execute(f"SELECT bg_image FROM users WHERE username='{username}'").fetchone()[0]

def getAM(username):
    return cursor.execute(f"SELECT about_me FROM users WHERE username='{username}'").fetchone()[0]

def changePfp(pfp, username):
    cursor.execute("UPDATE users SET pfp=? WHERE username=?", (pfp, username))

def changeBg(bg, username):
    cursor.execute("UPDATE users SET bg_image=? WHERE username=?", (bg, username))
    
def changeAM(am, username):
    cursor.execute("UPDATE users SET about_me=? WHERE username=?", (am, username))
    
def index():
    return cursor.execute("SELECT username, pfp FROM users").fetchall()

def addReview(username, text):
    cursor.execute("INSERT INTO posts(username, post) VALUES(?, ?)", (username, text))
    db.commit()

def getReview(reviewid):
    return cursor.execute("SELECT post FROM posts WHERE id=?", (blogid,)).fetchone()