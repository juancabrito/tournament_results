-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


CREATE TABLE RegisteredPlayers (
  name text,
  id serial PRIMARY KEY
);

CREATE TABLE Matches (
  winner_id  int REFERENCES RegisteredPlayers(id),
  loser_id  int REFERENCES RegisteredPlayers(id),
  round  int
);

CREATE VIEW v_matches_count AS
  SELECT RegisteredPlayers.name,
  SUM(
    CASE WHEN Matches.winner_id = RegisteredPlayers.id OR Matches.loser_id = RegisteredPlayers.id
    THEN 1 ELSE 0 END
  ) AS matches
  FROM RegisteredPlayers LEFT JOIN Matches
  ON Matches.winner_id = RegisteredPlayers.id OR Matches.loser_id = RegisteredPlayers.id
  GROUP BY RegisteredPlayers.name;

CREATE VIEW v_score AS
  SELECT RegisteredPlayers.id, RegisteredPlayers.name,
  SUM(
    CASE WHEN Matches.winner_id = RegisteredPlayers.id
    THEN 1 ELSE 0 END
  ) AS wins
  FROM RegisteredPlayers LEFT JOIN Matches
  ON Matches.winner_id = RegisteredPlayers.id OR Matches.loser_id = RegisteredPlayers.id
  GROUP BY RegisteredPlayers.id;

CREATE VIEW v_standings AS
  SELECT v_score.id, v_score.name, v_score.wins,
  v_matches_count.matches
  FROM v_score LEFT JOIN v_matches_count
  ON v_score.name = v_matches_count.name
  ORDER BY wins DESC;

