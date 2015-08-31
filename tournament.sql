-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE Tournaments (
  active boolean,
  id serial PRIMARY KEY
);

CREATE TABLE Players (
  name text,
  id serial PRIMARY KEY
);

CREATE TABLE RegisteredPlayers (
  player  int REFERENCES Players(id),
  tournament  int REFERENCES Tournaments(id)
);

CREATE TABLE Matches (
  winner_id  int REFERENCES Players(id),
  loser_id  int REFERENCES Players(id),
  tournament  int REFERENCES Tournaments(id),
  id serial PRIMARY KEY
);

CREATE VIEW v_registered_players AS
  SELECT RegisteredPlayers.player, Players.name, RegisteredPlayers.tournament
  FROM RegisteredPlayers JOIN Players
  ON RegisteredPlayers.player = Players.id
  ORDER BY tournament ASC;

CREATE VIEW v_matches_count AS
  SELECT Players.id, count(Matches.id) AS matches, RegisteredPlayers.tournament
  FROM Players LEFT JOIN Matches
  ON Matches.winner_id = Players.id OR Matches.loser_id = Players.id
  JOIN RegisteredPlayers ON RegisteredPlayers.player = Players.id AND RegisteredPlayers.tournament = Matches.tournament
  GROUP BY Players.id, RegisteredPlayers.tournament
  ORDER BY tournament ASC;

CREATE VIEW v_score AS
  SELECT Players.id, Players.name, count(Matches.winner_id) AS wins, RegisteredPlayers.tournament
  FROM Players LEFT JOIN Matches
  ON Matches.winner_id = Players.id
  JOIN RegisteredPlayers ON RegisteredPlayers.player = Players.id
  WHERE RegisteredPlayers.tournament = Matches.tournament
  GROUP BY Players.id, RegisteredPlayers.tournament
  ORDER BY tournament ASC;

CREATE VIEW v_standings AS
  SELECT v_score.id, v_score.name, v_score.wins,
  v_matches_count.matches, v_score.tournament
  FROM v_score JOIN v_matches_count
  ON v_score.tournament = v_matches_count.tournament AND v_score.id = v_matches_count.id
  ORDER BY tournament ASC;

CREATE VIEW v_tournaments AS
  SELECT v_standings.id, v_standings.name, v_standings.wins,
  v_standings.matches, v_standings.tournament, Tournaments.active
  FROM v_standings JOIN Tournaments
  ON v_standings.tournament = Tournaments.id
  ORDER BY tournament ASC;
