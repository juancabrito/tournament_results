# Tournament Results
This is a programming with SQL simple exercise.

A Python module that uses the PostgreSQL database to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

For details you can read this document:
https://docs.google.com/document/d/16IgOm4XprTaKxAa8w02y028oBECOoB1EI1ReddADEeY/pub?embedded=true


This project has two parts: defining the database schema (SQL table definitions), and writing the code that will use it.

## Testing the components

To create the database with its tables and views run:

```bash
$ psql
=> \i tournament.sql
```

To test the components just run:

```python
$ python tournament_test.py
```
