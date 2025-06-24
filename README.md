# Degrees of Separation

This project finds the shortest path between two actors based on movies they have appeared in together. It is inspired by the "Six Degrees of Kevin Bacon" game.

## Problem Description

Given a dataset containing information about people, movies, and the relationships between them, the goal is to determine the shortest chain of connections between two actors. A connection exists if two actors have starred in the same movie.

For example:
If Actor A and Actor B both appeared in Movie X, and Actor B and Actor C both appeared in Movie Y, then Actor A is connected to Actor C through Actor B.

## Files

- `degrees.py`: Main program logic.
- `util.py`: Contains helper classes for nodes and search frontiers.
- `people.csv`: Contains information about each person (ID, name, birth year).
- `movies.csv`: Contains information about each movie (ID, title, year).
- `stars.csv`: Maps people to the movies they starred in.

## How to Run

To run the program, use the following command:

