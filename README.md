# Minesweeper-AI
This is a repository created for my Intro to AI class.

In this I have utilized code from Kylie Ying. I have made my own changes, such as: including a flag feature and keeping track of unrevealed squares and bombs.

I have also with the help of my TA made a solver. I treated the problem as a constraint satisfaction problem. I generated a copy of the board that was being played on. The first move made by the solver is always random. After uncovering clues the board makes educated decisions on which squares are safe. If there are no safe squares that can be identified, the solver chooses a random square that is in the set of unrevealed squares.

How does the solver work:

