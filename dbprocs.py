#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Helper library to create a character.
# This program is dedicated to the public domain under the CC0 license.
import sqlite3 

def loadDB():
    connection=sqlite3.connect("swrpg.db")
    sqlCreateTable = """CREATE TABLE IF NOT EXISTS curCharacter (
    user_id INTEGER NOT NULL,
    Brawn INTEGER,
    Agility INTEGER,
    Intellect INTEGER,
    Cunning INTEGER,
    Willpower INTEGER,
    Presence INTEGER,
    Health INTEGER,
    Name VARCHAR(250),
    PRIMARY KEY (user_id, Name)
);"""
    cursor = connection.cursor()
    cursor.execute(sqlCreateTable)
    # Save the table.
    connection.commit()
    cursor.close()
    connection.close()
def checkPlayerExistence(user_id, user_stats):
    connection=sqlite3.connect("swrpg.db")
    cursor = connection.cursor()
    sqlPlayerExistence = "SELECT COUNT(*) FROM curCharacter WHERE user_id={0} and Name='{1}';".format(user_id, user_stats['Name'])
    #Find user if they exist.
    cursor.execute(sqlPlayerExistence)
    retValCount = cursor.fetchone()[0]
    if retValCount == 0:
        cursor.close()
        connection.close()
        return False
    else:
        cursor.close()
        connection.close()
        return True
    

def insertUpdatePlayer(user_id, user_stats):
    connection=sqlite3.connect("swrpg.db")
    cursor = connection.cursor()
    # Remove one instance that we don't need and replace it with something we do need.
    if 'character' in user_stats:
        del user_stats['character']
    #user_stats['user_id'] = user_id
    if checkPlayerExistence(user_id, user_stats):
        sqlUpdateData = 'UPDATE curCharacter SET {}'.format(', '.join('{}=?'.format(k) for k in user_stats))
        cursor.execute(sqlUpdateData, list(user_stats.values()))
        connection.commit()
    else:
        placeholder = ", ".join(["?"] * (len(user_stats)))
        sqlInsertData = "insert into curCharacter ({columns}) values ({values});".format(columns=",".join(user_stats.keys()), values=placeholder)
        cursor.execute(sqlInsertData, list(user_stats.values()))
        connection.commit()
    cursor.close()
    connection.close()
def retrievePlayer(user_id, user_stats):
    connection=sqlite3.connect("swrpg.db")
    cursor = connection.cursor()
    # Grab via user ID.
    sqlFindPlayer = "SELECT * FROM curCharacter WHERE user_id = {0};".format(user_id)
    cursor.execute(sqlFindPlayer)
    ourData = cursor.fetchone()
    cursor.close()
    connection.close()
    return ourData