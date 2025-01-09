'''
GarfieldsCatHair: Sasha M, Chloe W, Moyo F, Claire S
SoftDev
P02: TuneTown
2025-01-15
Time Spent:
'''

import sqlite3
from flask import session
import bcrypt


#Create SQLite Table, creates if not already made
db = sqlite3.connect("database.db", check_same_thread=False)
cursor = db.cursor()

#Create a User Table
def userTable():
    cursor.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT NOT NULL, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
    db.commit()

#Create a Lesson Table
def lessonTable():
    cursor.execute("CREATE TABLE lessons(id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT, completion INTEGER, flashcards TEXT)") # flashcards should be csv file location
    db.commit()

#Create Test Table
def testTable0():
    cursor.execute("CREATE TABLE tests(id INTEGER PRIMARY KEY, questions TEXT, correctAnswers INTEGER)") # questions should be csv file location
    db.commit()

def testTable(name):
    cursor.execute(f"CREATE TABLE '{name}'(id INTEGER PRIMARY KEY, question TEXT, userAnswer TEXT, correctAnswer TEXT)")
    db.commit()

# User Helpers

def addUser(name, username, password):
    cursor.execute("INSERT INTO users(name, username, password) VALUES (?, ?, ?)", (name, username, hashPassword(password)))
    db.commit()

def removeUser(id):
    cursor.execute(f"DELETE FROM users WHERE id='{id}'")
    db.commit()

def validateUser(username, password):
    dbPassword = getHash(username)
    if dbPassword:
        #fix validatePassword()!
        return validatePassword(dbPassword, password)
    return False

def getName(username):
    return cursor.execute(f"SELECT name FROM users WHERE username='{username}'").fetchone()[0]

def getId(username):
    return cursor.execute(f"SELECT id FROM users WHERE username='{username}'").fetchone()[0]

def getHash(username):
    return cursor.execute(f"SELECT password FROM users WHERE username='{username}'").fetchone()[0]