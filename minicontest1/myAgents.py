# myAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from game import Agent, Directions, Actions
from searchProblems import PositionSearchProblem, manhattanHeuristic, mazeDistance

import util
import time
import search
import math, random

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

def manhattan(startPosition, targetPosition):
    xy1 = startPosition
    xy2 = targetPosition
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def spreadOutAndFindDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        currentPosition = gameState.getPacmanPosition(self.index)
        foodList = gameState.getFood().asList()
        walls = gameState.getWalls()
        randomFood = []
        problem = []

        #problem = AnyFoodSearchProblem(gameState, self.index)

        # if min(manhattan(currentPosition, foodPosition) for foodPosition in food.asList()) > 10:
        #     return [Directions.STOP]
        #print("self.targets = ", self.targets)
        if self.index == 0:
            TargetFood = ClosestFood(currentPosition, foodList)
            #self.targets.append(TargetFood)
            problem = PositionSearchProblem(gameState, 0, goal=TargetFood, start=currentPosition, warn=False, visualize=False)
            return search.aStarSearch(problem, manhattanHeuristic)
        if self.index == 1:
            TargetFood = ClosestFood(currentPosition, foodList)
            """
            want to find a way to avoid both agents coming up with the same target. But the below doesn't work because
            each agent has their own self.targets. How to keep a common list of targets?
            """
            # if TargetFood in self.targets:
            #     tempFoodList = foodList.copy()
            #     tempFoodList.pop(tempFoodList.index(TargetFood))
            #     TargetFood = ClosestFood(currentPosition, tempFoodList)
            #     self.targets.append(TargetFood)
            # else:
            #     self.targets.append(TargetFood)
            problem = PositionSearchProblem(gameState, 1, goal=TargetFood, start=currentPosition, warn=False, visualize=False)
            return search.aStarSearch(problem, manhattanHeuristic)
        if self.index == 2:
            TargetFood = RandomFood(currentPosition, foodList)
            problem = PositionSearchProblem(gameState, 2, goal=TargetFood, start=currentPosition, warn=False, visualize=False)
            return search.aStarSearch(problem, manhattanHeuristic)
        if self.index == 3:
            TargetFood = RandomFood(currentPosition, foodList)
            problem = PositionSearchProblem(gameState, 3, goal=TargetFood, start=currentPosition, warn=False, visualize=False)
            return search.aStarSearch(problem, manhattanHeuristic)
        #return search.bfs(problem)

        #util.raiseNotDefined()

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0

        if self.actionIndex == 0:
            self.actions = self.spreadOutAndFindDot(state)
            if len(self.actions) == 1:
                return self.actions[0]
            else:
                self.actionIndex += 1
                return self.actions[0]
        else:
            i = self.actionIndex
            self.actionIndex += 1
            if i < len(self.actions):
                return self.actions[i]
            else:
                self.actionIndex = 0
                return Directions.STOP
                # self.actions = self.spreadOutAndFindDot(state)
                # if len(self.actions) == 1:
                #     return self.actions[0]
                # else:
                #     self.actionIndex += 1
                #     return self.actions[0]

        #raise NotImplementedError()

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """
        self.actions = []
        "*** YOUR CODE HERE"
        #raise NotImplementedError()

"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""



def spreadHeuristic(state, problem):
    currentPosition = state
    #distanceWithClosestFood = min([manhattan(currentPosition, foodPosition) for foodPosition in problem.food.asList()])
    if len(problem.allPacPositions) > 1:
        distanceWithClosestPac = min([manhattan(pacPosition, currentPosition) for pacPosition in problem.allPacPositions if pacPosition != currentPosition])
        return 10/distanceWithClosestPac
    else:
        return 0

def FurthestHeuristic(state, problem):
    currentPosition = state
    distanceWithFurthestFood = max([manhattan(currentPosition, foodPosition) for foodPosition in problem.food.asList()])

    return distanceWithFurthestFood

def FurthestFood(state, foodList):
    maxDist = 0
    for foodPosition in foodList:
        Dist = manhattan(state, foodPosition)
        if Dist > maxDist:
            maxDist = Dist
            farFood = foodPosition
    return farFood

def ClosestFood(state, foodList):
    minDist = 999999
    for foodPosition in foodList:
        Dist = manhattan(state, foodPosition)
        if Dist < minDist:
            minDist = Dist
            nearestFood = foodPosition
    return nearestFood

def RandomFood(state, foodList):
    return random.choice(foodList)

def ClosestHeuristic(state, problem):
    currentPosition = state
    closerFoods = []
    for foodPosition in problem.food.asList():
        if abs(currentPosition[0]-foodPosition[0])<6 and abs(currentPosition[1]-foodPosition[1])<6:
            closerFoods.append(foodPosition)
    if len(closerFoods)>0:
        distanceWithClosestFood = min([manhattan(currentPosition, food) for food in closerFoods])
    else:
        distanceWithClosestFood = min([manhattan(currentPosition, food) for food in problem.food.asList()])

    return distanceWithClosestFood

def CloseHeuristic(state, problem):
    currentPosition = state

    distanceWithCloseFood = 10
    for foodPosition in problem.food.asList():
        if manhattan(currentPosition, foodPosition) < 5:
            distanceWithCloseFood = manhattan(currentPosition, foodPosition)
            break
    return distanceWithCloseFood

def RandomHeuristic(state, problem, agentIndex):
    randomFood = random.choice(problem.food.asList())
    return manhattan(state, random.choice(problem.food.asList()))




class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)

        return search.breadthFirstSearch(problem)
        util.raiseNotDefined()

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()
        self.targets = []



        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        #self.position = gameState.getPacmanPosition(agentIndex)
        self.allPacPositions = gameState.getPacmanPositions()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        if state in self.food.asList():
            return True
        else:
            return False

        util.raiseNotDefined()
class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState, agentIndex):
        self.start = (startingGameState.getPacmanPosition(agentIndex), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

# class AStarFoodSearchAgent(SearchAgent):
#     "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
#     def __init__(self):
#         self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
#         self.searchType = FoodSearchProblem

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """
    import itertools



    def manhattan(startPosition, targetPosition):
        xy1 = startPosition
        xy2 = targetPosition
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    position, foodGrid = state

    return len(foodGrid.asList())
    #
    # """
    # The below algorithm is from:
    # https://stackoverflow.com/questions/9994913/pacman-what-kinds-of-heuristics-are-mainly-used
    #
    # Find real/manhattan distance between two currently furthest fruits in labyrinth - let's call that x.
    # Find real/manhattan distance from current Pacman position to the closer of previous two fruits - let's call that y.
    # Then, answer is just: x + y.
    # The interpretation of this x + y formula could be something like this:
    #
    # x - either way, you will have to travel this distance, at least at the end
    # y - while you are at the some of the two furthest fruits, it's better to collect
    # the food that is near to it so you don't have to go back
    # """
    # maxFoodPairDistance = 0
    #
    # if len(foodGrid.asList()) >= 2:
    #
    #     #calculate manhattan/real distance between each pair of food (all permutations in foodGrid) and find the maximum of them, and
    #     #store the pair with max distance in maxFoodPair
    #     for foodPair in itertools.permutations(foodGrid.asList(),2):
    #         #foodPairDistance = mazeDistance(foodPair[0], foodPair[1], problem.startingGameState)
    #         foodPairDistance = manhattan(foodPair[0], foodPair[1])
    #         if foodPairDistance >= maxFoodPairDistance:
    #             maxFoodPairDistance = foodPairDistance
    #             maxFoodPair = foodPair
    #
    #     #get the real distance between pacman and nearest food among the max distance food pair we get above. Using real distance instead
    #     #of manhattan distance here just to "reduce" the number of nodes expand to get additional point. But that's a bit of a cheating
    #     #because the mazeDistance function use of breadth First search - which itself is a search with nodes expansion not counted here
    #     #minPacmanToFoodDistance = min([mazeDistance(position, foodPosition, problem.startingGameState) for foodPosition in maxFoodPair])
    #     minPacmanToFoodDistance = min([manhattan(position, foodPosition) for foodPosition in maxFoodPair])
    #
    #     #When only one food left, just return the real distance between pacman and food
    # elif len(foodGrid.asList()) == 1:
    #     foodPosition = foodGrid.asList()[0]
    #     #minPacmanToFoodDistance = mazeDistance(position, foodPosition, problem.startingGameState)
    #     minPacmanToFoodDistance = manhattan(position, foodPosition)
    # else:
    #     minPacmanToFoodDistance = 0
    #
    # return minPacmanToFoodDistance + maxFoodPairDistance
