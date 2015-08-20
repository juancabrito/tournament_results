# Tournament Results
This is a programming with SQL simple exercise.

A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

This project has two parts: defining the database schema (SQL table definitions), and writing the code that will use it.

## Testing the components

To create the database with its tables and views run:

```bash
$ psql
=> \i tournament.sql
```
This will create the "tournament" database and two tables:

- Players
- Matches

Also three views from those tables:

- v_matches_count
- v_score
- v_standings

To test the components just run:

```python
$ python tournament_test.py
```
