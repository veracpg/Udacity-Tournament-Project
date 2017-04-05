#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    c = connect()
    db_cursor = c.cursor()
    query = "DELETE FROM matches;"
    db_cursor.execute(query)
    c.commit()
    c.close()


def deletePlayers():
    """Remove all the player records from the database."""
    c = connect()
    db_cursor = c.cursor()
    query = "DELETE FROM players;"
    db_cursor.execute(query)
    c.commit()
    c.close()


def countPlayers():
    """Returns the number of players currently registered."""
    c = connect()
    db_cursor = c.cursor()
    query = "SELECT count(*) AS num FROM players;"
    db_cursor.execute(query)
    player_count = db_cursor.fetchone()[0]
    c.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    c = connect()
    db_cursor = c.cursor()
    db_cursor.execute("INSERT INTO players (name) VALUES (%s);",(name,))
    c.commit()
    c.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    c = connect()
    db_cursor = c.cursor()
    db_cursor.execute("SELECT * FROM standings;")
    player_standings = db_cursor.fetchall()
    c.close()
    return player_standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    c = connect()
    db_cursor = c.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES ({0},{1});". format(winner, loser)
    db_cursor.execute(query)
    c.commit()
    c.close()


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
    c = connect()
    db_cursor = c.cursor()
    query = "SELECT * FROM standings;"
    db_cursor.execute(query)
    pairs = db_cursor.fetchall()
    pairings = []
    count = len(pairs)

    for x in range (0, count -1, 2):
        paired_list = (pairs[x][0], pairs[x][1], pairs[x + 1][0], pairs[x + 1][1])
        pairings.append(paired_list)

    c.close()
    return pairings


