# CS188-Artificial-Intelligence-Projects
Completed assignment projects in Python for UC Berkeley's CS188 Introduction to Artificial Intelligence course: https://inst.eecs.berkeley.edu/~cs188/fa18/

## python_basics
### Project 0 - Python Basics
https://inst.eecs.berkeley.edu/~cs188/fa18/
I had experience in object-oriented programming with JavaScript so this project is not that difficult. But it didn't take long for me to discover that the real challenge lied ahead.

## proj1-search-python3
### Project 1 - Search
https://inst.eecs.berkeley.edu/~cs188/fa18/project1.html
The biggest hurdle when I first tackle this project is to read the codes in multiple Python files and understand how they work together. I googled for tutorials and learnt about class inheritance, abstract functions as well as other Python skills. Then I implemented various search functions (Depth first search, Breadth first search, A* Search ,etc) for Pacman agent to find paths through mazes to reach a particular location and to collect food efficiently.

## multiagent
### Project 2 - Games
https://inst.eecs.berkeley.edu/~cs188/fa18/project2.html
In this project, I've designed both Pacman and ghosts agents using minimax and expectimax search. It also involved the design of an evaluation function to evaluate game states. My first time to try out simple feature engineering. A bit challenging as I've to experiment various weight vectors by tried and error to find out which works best.

## reinforcement
### Project 3 - Reinforcement Learning
https://inst.eecs.berkeley.edu/~cs188/fa18/project3.html
The first machine learning project that I did for this course. I've implemented functions for value iteration and policy evaluations for Markov's Decision Processes.
The most interesting part lies in the implementation of Q-Learning for a Pacman agent, training and finally field testing it on the game.

## ghostbusters
### Project 4 - Ghostbusters
https://inst.eecs.berkeley.edu/~cs188/fa18/project4.html
A relatively more straight forward project compared to the rest. Involves implementation of a discrete distribution class which represents the probability distribution of the ghost. Implemented update functions for time elapse and observation, by both exact evaluation and particle filtering.

## minicontest1
### Mini Contest 1
https://inst.eecs.berkeley.edu/~cs188/fa18/minicontest1.html
One of the more challenging projects in the course in which I've to implement multiple agents that "collaborate" with each other to clear all food in the maze. At first my score keep reducing to zero as my agents take too much time to compute the actions. After much experimentation I finally came up with strategies to minimize computation time - 1) Cache the sequence of actions returned by the search function; 2) Prioritize directions for each agent so they spread out; 3) Assign different food targets for each agent. A challenging but satisfying project!

## minicontest2
### Mini Contest 2
https://inst.eecs.berkeley.edu/~cs188/fa18/minicontest2.html
By far the most challenging project of this course. I need to design evaluation functions that extract different feature vectors for different agents, eg. an offensive agent that sweep out all food in enemy's territory and a defensive agent that protects the food in its own ground. Also, the offensive agent need to be hard-coded to return home after it collected enough food.
