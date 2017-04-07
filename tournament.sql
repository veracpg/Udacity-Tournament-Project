-- Table definitions for the tournament project.

-- Drop database if it exists
DROP DATABASE IF EXISTS tournament;

-- Create Database
CREATE DATABASE tournament;

--Connect to database
\c tournament

-- Create players table
CREATE TABLE players(id SERIAL PRIMARY KEY, name text);

-- Create matcher table
CREATE TABLE matches (id SERIAL PRIMARY KEY , winner INTEGER REFERENCES players (id),
                      loser INTEGER REFERENCES players (id));

-- Creates a view of matches played
CREATE VIEW wins AS
  SELECT players.id, count(matches.winner) AS n FROM players
  LEFT JOIN matches ON players.id =  matches.winner
  GROUP BY players.id;

CREATE VIEW count AS
  SELECT players.id, count(matches.winner) AS n FROM players
  LEFT JOIN matches ON players.id = matches.winner
  OR players.id = matches.loser
  GROUP BY players.id;

CREATE VIEW standings AS
  SELECT players.id, players.name, wins.n AS wins, count.n AS matches_played
      FROM players, wins, count
      WHERE players.id = wins.id and players.id = count.id
      ORDER BY wins DESC;




