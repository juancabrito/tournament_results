#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import random
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection and a cursor."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Error connecting database")



def deleteMatches():
    """Remove all the match records from the database."""

    db, cursor = connect()

    query = "TRUNCATE Matches"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""

    db, cursor = connect()

    query = "TRUNCATE Matches, RegisteredPlayers;"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""

    db, cursor = connect()

    query = "SELECT count(*) FROM RegisteredPlayers"
    cursor.execute(query,)
    count = cursor.fetchone()
    db.close()
    return int(count[0])

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      name: the player's full name (need not be unique).
    """

    db, cursor = connect()

    query = "INSERT INTO RegisteredPlayers (name) VALUES (%s);"
    parameter = (name,)
    cursor.execute(query, parameter)

    db.commit()
    db.close


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    db, cursor = connect()

    query = "SELECT * FROM v_standings;"
    
    cursor.execute(query,)
    db.close

    standings = [(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db, cursor = connect()

    query1 = "SELECT count(*) FROM Matches;"
    cursor.execute(query1,)
    matches_exist = cursor.fetchone()
    matches_exist = matches_exist[0]
    
    query2 = "SELECT count(*) FROM RegisteredPlayers;"
    cursor.execute(query2,)
    players = cursor.fetchone()
    players = players[0]/2

    rounds = matches_exist % players

    if rounds == 0:
        roundn = matches_exist / players + 1
        query = "INSERT INTO Matches VALUES (%s, %s, %s);"
        parameter = (winner, loser, roundn)
        cursor.execute(query, parameter)
    else:
        roundn = int(matches_exist / players + 1)
        query = "INSERT INTO Matches VALUES (%s, %s, %s);"
        parameter = (winner, loser, roundn)
        cursor.execute(query, parameter)


    db.commit()
    db.close


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    db, cursor = connect()

    query = "SELECT id, name FROM v_standings;"
    cursor.execute(query,)
    standings = cursor.fetchall()


    query = "SELECT id, name FROM v_standings WHERE wins >= 1;"
    cursor.execute(query,)
    played = cursor.fetchall()


    if not played:
        """Random pairing if there's no matches yet"""
        
        query = "SELECT * FROM RegisteredPlayers;"
        cursor.execute(query,)

        ps = cursor.fetchall()
        db.close
        if ps:
            random.shuffle(ps)
            pairs = []
            for pair in zip(ps[len(ps)/2:], ps[:len(ps)/2]):
                pairs.append((pair[0][1], pair[0][0], pair[1][1], pair[1][0]))
            return pairs
        else:
            print "No players registered yet"

    else:
        """Swiss pairing process"""
        db.close
        return pairing(standings, [])


def pairing(unpaired, pairs=[]):
    """Simple pairing helper function"""

    s = unpaired[:2]
    

    if len(unpaired) == 2:
        pairs.append((s[0][0], s[0][1], s[1][0], s[1][1]))

    else:
        pairs.append((s[0][0], s[0][1], s[1][0], s[1][1]))
        pairing(unpaired[2:], pairs)
        

    return pairs
