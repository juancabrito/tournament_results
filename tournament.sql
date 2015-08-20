-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE Players (
  name text,
  id serial PRIMARY KEY
);

CREATE TABLE Matches (
  winner_id  int REFERENCES Players(id),
  loser_id  int REFERENCES Players(id),
  id serial PRIMARY KEY
);

-- View for counting matches by player.
CREATE VIEW v_matches_count AS
	SELECT Players.id, count(Matches.id) AS matches
	FROM Players LEFT JOIN Matches
  ON Matches.winner_id = Players.id OR Matches.loser_id = Players.id
	GROUP BY Players.id ORDER BY matches;

-- View for computing wins by player.
CREATE VIEW v_score AS
  SELECT Players.id, Players.name, count(Matches.winner_id) AS wins
  FROM Players LEFT JOIN Matches
  ON Matches.winner_id = Players.id
  GROUP BY Players.id ORDER BY wins DESC;

-- View for standings, including player's id, name, wins and matches played.
CREATE VIEW v_standings AS
  SELECT v_score.id, v_score.name, v_score.wins, v_matches_count.matches
  FROM v_score JOIN v_matches_count
  ON v_score.id = v_matches_count.id
	ORDER BY wins DESC;
