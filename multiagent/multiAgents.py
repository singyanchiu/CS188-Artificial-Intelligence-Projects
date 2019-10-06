# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #print("successorGameState =","\n", successorGameState, "\n")
        #print("newPos =","\n", newPos, "\n")
        #print("newFood =","\n", newFood, "\n")
        #print("newGhostStates =","\n", [newGhostState.getPosition() for newGhostState in newGhostStates], "\n")
        #print("newScaredTimes =","\n", newScaredTimes, "\n")

        distancesToFood = [manhattanDistance(newPos, foodPosition) for foodPosition in newFood.asList()]
        if len(distancesToFood) > 0:
            closestDistanceToFood = min(distancesToFood)
        else:
            closestDistanceToFood = 0

        distancesToGhosts = [manhattanDistance(newPos, newGhostState.getPosition()) for newGhostState in newGhostStates if newGhostState.scaredTimer == 0]
        if len(distancesToGhosts) > 0:
            closestDistanceToGhost = min(distancesToGhosts)
        else:
            closestDistanceToGhost = 999

        distancesToScaredGhosts= [manhattanDistance(newPos, newGhostState.getPosition()) for newGhostState in newGhostStates if newGhostState.scaredTimer != 0]
        if len(distancesToScaredGhosts) > 0:
            closestDistanceToScaredGhost = min(distancesToScaredGhosts)
        else:
            closestDistanceToScaredGhost = 999

        #print("closestDistanceToScaredGhost = ", closestDistanceToScaredGhost)
        eval = closestDistanceToGhost + 23/(closestDistanceToFood+1) + 30/(closestDistanceToScaredGhost+1) + successorGameState.getScore()

        return eval

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'better', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def __init__(self, **kwargs):
        MultiAgentSearchAgent.__init__(self, **kwargs)
        self.currentDepth = 0
        self.actionList = []
        self.actionIndex = 0
        self.action = ""

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        """
        successorGameState = gameState.generateSuccessor(0, action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        legalMoves = gameState.getLegalActions(0)
        """
        def value(state, currentAgentIndex, currentDepth):
            #if currentDepth == self.depth:
            #    return self.evaluationFunction(state)
            #print("self.depth in value function = ", self.depth)
            if currentDepth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if currentAgentIndex < state.getNumAgents():
                if currentAgentIndex == 0:
                    maxValue = maximumValue(state, currentAgentIndex, currentDepth)
                    return maxValue
                else:
                    minValue = minimumValue(state, currentAgentIndex, currentDepth)
                    return minValue
            else: #currentAgentIndex exceeded
                return value(state, 0, currentDepth+1)

        def maximumValue(state, currentAgentIndex, currentDepth):
            #v = float("-inf")
            legalMoves = state.getLegalActions(0)
            successorValues = []
            for move in legalMoves:
                successorState = state.generateSuccessor(currentAgentIndex, move)
                successorValues.append(value(successorState, currentAgentIndex + 1, currentDepth))
            v = max(successorValues)
            if currentDepth == 0:
                bestIndices = [index for index in range(len(successorValues)) if successorValues[index] == v]
                chosenIndex = random.choice(bestIndices)
                self.action = legalMoves[chosenIndex]
            return v

        def minimumValue(state, currentAgentIndex, currentDepth):
            v = float("inf")
            legalMoves = state.getLegalActions(currentAgentIndex)
            for move in legalMoves:
                successorState = state.generateSuccessor(currentAgentIndex, move)
                successorValue = value(successorState, currentAgentIndex + 1, currentDepth)
                if successorValue < v:
                    v = successorValue
            return v

        self.action = ""
        rootValue = value(gameState, 0, 0)
        return self.action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def value(state, currentAgentIndex, currentDepth, alpha, beta):
            if currentDepth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            if currentAgentIndex < state.getNumAgents():
                if currentAgentIndex == 0:
                    maxValue = maximumValue(state, currentAgentIndex, currentDepth, alpha, beta)
                    return maxValue
                else:
                    minValue = minimumValue(state, currentAgentIndex, currentDepth, alpha, beta)
                    return minValue
            else:
                return value(state, 0, currentDepth+1, alpha, beta)

        def maximumValue(state, currentAgentIndex, currentDepth, alpha, beta):
            v = float("-inf")
            legalMoves = state.getLegalActions(0)
            successorValues = []
            for move in legalMoves:
                successorState = state.generateSuccessor(currentAgentIndex, move)
                successorValue = value(successorState, currentAgentIndex + 1, currentDepth, alpha, beta)
                if currentDepth == 0:
                    successorValues.append(successorValue)
                if successorValue > v:
                     v = successorValue
                if v > beta: return v
                alpha = max(alpha, v)
            if currentDepth == 0:
                bestIndices = [index for index in range(len(successorValues)) if successorValues[index] == v]
                chosenIndex = random.choice(bestIndices)
                self.action = legalMoves[chosenIndex]
            return v

        def minimumValue(state, currentAgentIndex, currentDepth, alpha, beta):
            v = float("inf")
            legalMoves = state.getLegalActions(currentAgentIndex)
            for move in legalMoves:
                successorState = state.generateSuccessor(currentAgentIndex, move)
                successorValue = value(successorState, currentAgentIndex + 1, currentDepth, alpha, beta)
                if successorValue < v:
                    v = successorValue
                if v < alpha: return v
                beta = min(beta, v)
            return v

        self.action = ""
        rootValue = value(gameState, 0, 0, float("-inf"), float("inf"))
        return self.action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def value(state, currentAgentIndex, currentDepth):
            if currentDepth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            if currentAgentIndex < state.getNumAgents():
                if currentAgentIndex == 0:
                    maxValue = maximumValue(state, currentAgentIndex, currentDepth)
                    return maxValue
                else:
                    minValue = expectValue(state, currentAgentIndex, currentDepth)
                    return minValue
            else: #currentAgentIndex exceeded
                return value(state, 0, currentDepth+1)

        def maximumValue(state, currentAgentIndex, currentDepth):
            legalMoves = state.getLegalActions(0)
            successorValues = []
            for move in legalMoves:
                successorState = state.generateSuccessor(currentAgentIndex, move)
                successorValues.append(value(successorState, currentAgentIndex + 1, currentDepth))
            v = max(successorValues)
            if currentDepth == 0:
                bestIndices = [index for index in range(len(successorValues)) if successorValues[index] == v]
                chosenIndex = random.choice(bestIndices)
                self.action = legalMoves[chosenIndex]
            return v

        def expectValue(state, currentAgentIndex, currentDepth):
            v = 0
            legalMoves = state.getLegalActions(currentAgentIndex)
            for move in legalMoves:
                successorState = state.generateSuccessor(currentAgentIndex, move)
                successorValue = value(successorState, currentAgentIndex + 1, currentDepth)
                v += successorValue/(len(legalMoves))
            return v

        self.action = ""
        rootValue = value(gameState, 0, 0)
        return self.action

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """

    PacPos = currentGameState.getPacmanPosition()
    allFood = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    allCapsules = currentGameState.getCapsules()
    #ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]

    # getGhostPosition(self, agentIndex)
    # getGhostPositions(self)
    # getCapsules(self)
    # getNumFood(self)

    distancesToCapsules = [manhattanDistance(PacPos, CapsulePosition) for CapsulePosition in allCapsules]
    if len(distancesToCapsules) > 0:
        closestDistanceToCapsule = min(distancesToCapsules)
    else:
        closestDistanceToCapsule = 999

    distancesToFood = [manhattanDistance(PacPos, foodPosition) for foodPosition in allFood.asList()]
    if len(distancesToFood) > 0:
        closestDistanceToFood = min(distancesToFood)
    else:
        closestDistanceToFood = 0

    distancesToGhosts = [manhattanDistance(PacPos, GhostState.getPosition()) for GhostState in GhostStates if GhostState.scaredTimer == 0]
    if len(distancesToGhosts) > 0:
        closestDistanceToGhost = min(distancesToGhosts)
    else:
        closestDistanceToGhost = 999

    distancesToScaredGhosts = [manhattanDistance(PacPos, GhostState.getPosition()) for GhostState in GhostStates if GhostState.scaredTimer != 0]
    if len(distancesToScaredGhosts) > 0:
        closestDistanceToScaredGhost = min(distancesToScaredGhosts)
    else:
        closestDistanceToScaredGhost = 999

    #print("closestDistanceToScaredGhost = ", closestDistanceToScaredGhost)
    eval = closestDistanceToGhost + 23/(closestDistanceToFood+1) + 30/(closestDistanceToScaredGhost+1) +  30/(closestDistanceToCapsule+1) + currentGameState.getScore()

    return eval

# Abbreviation
better = betterEvaluationFunction
