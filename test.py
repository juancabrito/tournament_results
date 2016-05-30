from tournament import *
import random

"""Set of tests for FSND Project 2 (SQL)"""

# Registering some players

print "\nRegistering users..."
registerPlayer("Andres O'Neal");
registerPlayer('Beto O"Brien');
registerPlayer('Carlos');
registerPlayer('Daniel');
registerPlayer('Elisa');
registerPlayer('Francisca');
registerPlayer('Gabriela');
registerPlayer('Helene');
registerPlayer('Ines');
registerPlayer('Juan');
registerPlayer('Kiko');
registerPlayer('Luis');
print "Success!"

# First pairing that must be random

print "\nRunning pairing process..."
pairs = swissPairings()
print "Success!"
print "\nPairs list: %s" % pairs
print "Pairs count: %s" % len(pairs)

# Entering some results for the first matches

def reportMatches(players):
    for _ in range(len(pairs)):
        options = [0,2]
        random.shuffle(options)
        reportMatch(players[ _ ][options.pop()], players[ _ ][options.pop()])

print "\nRunning bulk reporting of matches..."
reportMatches(pairs)
print "Success!"

# Review standings

print "\nFirst standings: %s" % playerStandings()

# New pairing, now using Swiss Pairing

print "\nRunning pairing process..."
players = swissPairings()
print "Success!"

print "\nNew swiss pairs: %s" % players

# Entering some new results for the first matches

print "\nRunning bulk reporting of matches..."
reportMatches(players)
print "Success!"

# Review standings again

print "\nSecond standings: %s" % playerStandings()

# Third pairing, using Swiss Pairing

print "\nRunning pairing process..."
players = swissPairings()
print "Success!"

print "\nNew swiss pairs: %s" % players

# Entering some new results for the first matches

print "\nRunning bulk reporting of matches..."
reportMatches(players)
print "Success!"

# Review standings again

print "\nThird standings: %s" % playerStandings()

# Fourth pairing, using Swiss Pairing

print "\nRunning pairing process..."
players = swissPairings()
print "Success!"

print "\nNew swiss pairs: %s" % players

# Entering some new results for the first matches

print "\nRunning bulk reporting of matches..."
reportMatches(players)
print "Success!"

# Review standings again

print "\nFourth standings: %s" % playerStandings()
