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


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM Matches")
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""

    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM Matches")
    c.execute("DELETE FROM Players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""

    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM players")
    count = c.fetchone()
    db.close()
    return int(count[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    db = connect()
    c = db.cursor()
    name = bleach.clean(name).replace("'", " ")
    c.execute("INSERT INTO Players VALUES('%s')" % name)
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

    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM v_standings")
    db.close

    standings = [(row[0], row[1], row[2], row[3]) for row in c.fetchall()]
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    db = connect()
    c = db.cursor()

    c.execute("INSERT INTO Matches VALUES(%s, %s)" % (winner, loser))
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

    db = connect()
    c = db.cursor()

    c.execute("SELECT id, name FROM v_standings")
    standings = c.fetchall()

    c.execute("SELECT id, name FROM v_standings where wins >= 1")
    played = c.fetchall()

    if not played:
        """Random pairing if there's no matches yet"""

        c.execute("SELECT * FROM Players")
        ps = c.fetchall()
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

        return pairing(standings)


def pairing(unpaired, pairs=[]):
    """Simple pairing helper function"""

    s = unpaired[:2]

    if len(unpaired) == 2:
        pairs.append((s[0][0], s[0][1], s[1][0], s[1][1]))
    else:
        pairs.append((s[0][0], s[0][1], s[1][0], s[1][1]))
        pairing(unpaired[2:], pairs)

    return pairs
