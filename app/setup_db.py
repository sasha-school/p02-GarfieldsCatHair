'''
GarfieldsCatHair: Sasha M, Chloe W, Moyo F, Claire S
SoftDev
P02: TuneTown
2025-01-15
Time Spent:
'''

import sqlite3
from flask import session

def setup(): 
#Create SQLite Table, creates if not already made
    db = sqlite3.connect("database.db", check_same_thread=False)
    cursor = db.cursor()
    db.commit()
    db.close()
    
def connect():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    return c, db

def close(db):
    db.commit()
    db.close()

#user table
def userTable():
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, pfp TEXT NOT NULL, bg_image TEXT NOT NULL, about_me TEXT NOT NULL)")
    db.commit()

#posts table
def testTable0():
    cursor.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY, username TEXT, post TEXT)") 
    db.commit()

# User Helpers
def addUser(username, password):
    cursor, db = connect()
    default_pfp = "https://i.pinimg.com/736x/a6/be/9c/a6be9ced2fd7a0884518e3535ff0bce8.jpg"
    default_bg_image = "https://raw.githubusercontent.com/sasha-school/p02-GarfieldsCatHair/refs/heads/main/flag.jpg"
    default_about_me = "about me!"
    cursor.execute("INSERT INTO users(username, password, pfp, bg_image, about_me) VALUES (?, ?, ?, ?, ?)", (username, password, default_pfp, default_bg_image, default_about_me))
    close(db)

def removeUser(id):
    cursor.execute(f"DELETE FROM users WHERE id='{id}'")
    db.commit()

def validateUser(username, password):
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