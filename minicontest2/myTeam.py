# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
import distanceCalculator

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveAgent', second = 'DeffensiveAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class OffensiveAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)
    self.start = gameState.getAgentPosition(self.index)
    self.depth = 3
    '''
    Your initialization code goes here, if you need any.
    '''

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    def value(state, currentAgentIndex, currentDepth, alpha, beta):
        if currentDepth == self.depth or state.isOver():
            return self.evaluate(state)
        if currentAgentIndex == self.index:
            maxValue = maximumValue(state, currentAgentIndex, currentDepth, alpha, beta)
            return maxValue
        elif currentAgentIndex == 3:
            minValue = minimumValue(state, 3, currentDepth, alpha, beta)
            return minValue
        elif currentAgentIndex == 4:
            return value(state, self.index, currentDepth+1, alpha, beta)

    def maximumValue(state, currentAgentIndex, currentDepth, alpha, beta):
        v = float("-inf")
        legalMoves = state.getLegalActions(currentAgentIndex)
        #print("legalMoves = ", legalMoves)
        successorValues = []
        for move in legalMoves:
            successorState = state.generateSuccessor(currentAgentIndex, move)
            successorValue = value(successorState, 3, currentDepth, alpha, beta)
            if currentDepth == 0:
                successorValues.append(successorValue)
            if successorValue > v:
                 v = successorValue
            if v > beta: return v
            alpha = max(alpha, v)
        if currentDepth == 0:
            #print("legalMoves = ", legalMoves)
            #print("successor values = ", successorValues)
            bestIndices = [index for index in range(len(successorValues)) if successorValues[index] == v]
            #print("bestIndex = ", bestIndices)
            chosenIndex = random.choice(bestIndices)
            #print("chosenIndex = ", chosenIndex)
            self.action = legalMoves[chosenIndex]

            #print("self.index = ", self.index)
            #print("self.action = ", self.action)
        return v

    def minimumValue(state, currentAgentIndex, currentDepth, alpha, beta):
        v = float("inf")
        legalMoves = state.getLegalActions(currentAgentIndex)
        for move in legalMoves:
            successorState = state.generateSuccessor(currentAgentIndex, move)
            successorValue = value(successorState, 4, currentDepth, alpha, beta)
            if successorValue < v:
                v = successorValue
            if v < alpha: return v
            beta = min(beta, v)
        return v

    foodLeft = len(self.getFood(gameState).asList())
    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    #print("ghost index = ", [i for i in self.getOpponents(gameState) if not gameState.getAgentState(i).isPacman])

    if foodLeft <= 2:
        bestDist = 9999
        actions = gameState.getLegalActions(self.index)
        for action in actions:
            successorState = gameState.generateSuccessor(self.index, action)
            pos2 = successorState.getAgentPosition(self.index)
            dist = self.getMazeDistance(self.start, pos2)
            if dist < bestDist:
              bestAction = action
              bestDist = dist
        return bestAction

    self.action = ""
    rootValue = value(gameState, self.index, 0, float("-inf"), float("inf"))
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)
    #print("---------self.action OUTSIDE = ", self.action, "---------------\n\n")
    #print("--------- RED TEAM indices = ", gameState.getRedTeamIndices(), "---------------\n\n")
    return self.action
    #if self.index == 0: return self.action
    #if self.index == 2: return "Stop"

  def evaluate(self, gameState):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState)
    return features * weights

  def getFeatures(self, gameState):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    foodGrid = self.getFood(gameState)
    foodList = foodGrid.asList()
    capsuleList = gameState.getCapsules()
    blueCapsules = []
    for capsule in capsuleList:
        if capsule[0] > foodGrid.width/2:
            blueCapsules.append(capsule)

    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()

    features['successorScore'] = self.getScore(gameState)

    features['1/foodRemaining'] = 0
    features['1/distanceToFood'] = 0
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['1/distanceToFood'] = 1/minDistance
      features['foodRemaining'] = -len(foodList)

    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    normalGhosts = [a for a in ghosts if a.scaredTimer == 0]
    scaredGhosts = [a for a in ghosts if a.scaredTimer != 0]

    features['ghostDistance'] = 99
    if len(normalGhosts) > 0:
      ndists = [self.getMazeDistance(myPos, a.getPosition()) for a in normalGhosts]
      features['ghostDistance'] = min(ndists)

    features['1/scaredGhostDistance'] = 0
    if len(scaredGhosts) > 0:
      sdists = [self.getMazeDistance(myPos, a.getPosition()) for a in scaredGhosts]
      features['1/scaredGhostDistance'] = 1/min(sdists)
      features['scaredGhostRemaining'] = -len(scaredGhosts)

    features['1/distanceToBase'] = 0
    if myState.numCarrying >= 1:
        distanceToBase = self.getMazeDistance(myPos, self.start)
        features['1/distanceToBase'] = 1/distanceToBase

    features['1/capsuleDistance'] = 0
    if len(blueCapsules) > 0:
        cdists = [self.getMazeDistance(myPos, a) for a in blueCapsules]
        features['1/capsuleDistance'] = 1/min(cdists)
        features['capsulesRemaining'] = -len(blueCapsules)

    actions = gameState.getLegalActions(self.index)
    if len(actions) <= 2 and features['ghostDistance'] <= 3:
        features['trapped'] = -1
    # else:
    #     for action in actions:
    #         successorState = gameState.generateSuccessor(self.index, action)
    #         successorActions = successorState.getLegalActions(self.index)
    #         if len(successorActions) <= 2 and features['ghostDistance'] <= 3:
    #             features['trapped'] = -1
            # else:
            #     for successorAction in successorActions:
            #         subSuccessorState = successorState.generateSuccessor(self.index, successorAction)
            #         subSuccessorActions = subSuccessorState.getLegalActions(self.index)
            #         if len(subSuccessorActions) <= 2 and features['ghostDistance'] <= 2:
            #             features['trapped'] = -1

    #print("myState.numCarrying = ", myState.numCarrying)
    #print("Blue Capsules = ", blueCapsules)
    #print(features)
    return features

  def getWeights(self, gameState):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    #return {'successorScore': 0, 'distanceToFood': -1000, 'foodRemaining': -100, 'ghostDistance': 10, 'scaredGhostDistance': -1, 'capsuleDistance': -1000}
    return {'successorScore': 50000, '1/distanceToFood': 300, 'foodRemaining': 1000, 'capsulesRemaining': 900, \
            'ghostDistance': 0.1, '1/scaredGhostDistance': 150, 'scaredGhostRemaining': 200, '1/capsuleDistance': 150, \
            'trapped': 999999, '1/distanceToBase': 70000}#99999}


class DeffensiveAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)
    self.start = gameState.getAgentPosition(self.index)
    self.depth = 3
    '''
    Your initialization code goes here, if you need any.
    '''

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    def value(state, currentAgentIndex, currentDepth, alpha, beta):
        if currentDepth == self.depth or state.isOver():
            return self.evaluate(state)
        if currentAgentIndex == self.index:
            maxValue = maximumValue(state, currentAgentIndex, currentDepth, alpha, beta)
            return maxValue
        elif currentAgentIndex == 3:
            minValue = minimumValue(state, 3, currentDepth, alpha, beta)
            return minValue
        elif currentAgentIndex == 4:
            return value(state, self.index, currentDepth+1, alpha, beta)

    def maximumValue(state, currentAgentIndex, currentDepth, alpha, beta):
        v = float("-inf")
        legalMoves = state.getLegalActions(currentAgentIndex)
        #print("legalMoves = ", legalMoves)
        successorValues = []
        for move in legalMoves:
            successorState = state.generateSuccessor(currentAgentIndex, move)
            successorValue = value(successorState, 3, currentDepth, alpha, beta)
            if currentDepth == 0:
                successorValues.append(successorValue)
            if successorValue > v:
                 v = successorValue
            if v > beta: return v
            alpha = max(alpha, v)
        if currentDepth == 0:
            #print("legalMoves = ", legalMoves)
            #print("successor values = ", successorValues)
            bestIndices = [index for index in range(len(successorValues)) if successorValues[index] == v]
            #print("bestIndex = ", bestIndices)
            chosenIndex = random.choice(bestIndices)
            #print("chosenIndex = ", chosenIndex)
            self.action = legalMoves[chosenIndex]

            #print("self.index = ", self.index)
            #print("self.action = ", self.action)
        return v

    def minimumValue(state, currentAgentIndex, currentDepth, alpha, beta):
        v = float("inf")
        legalMoves = state.getLegalActions(currentAgentIndex)
        for move in legalMoves:
            successorState = state.generateSuccessor(currentAgentIndex, move)
            successorValue = value(successorState, 4, currentDepth, alpha, beta)
            if successorValue < v:
                v = successorValue
            if v < alpha: return v
            beta = min(beta, v)
        return v

    foodLeft = len(self.getFood(gameState).asList())
    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    #print("ghost index = ", [i for i in self.getOpponents(gameState) if not gameState.getAgentState(i).isPacman])

    if foodLeft <= 2:
        bestDist = 9999
        actions = gameState.getLegalActions(self.index)
        for action in actions:
            successorState = gameState.generateSuccessor(self.index, action)
            pos2 = successorState.getAgentPosition(self.index)
            dist = self.getMazeDistance(self.start, pos2)
            if dist < bestDist:
              bestAction = action
              bestDist = dist
        return bestAction

    self.action = ""
    rootValue = value(gameState, self.index, 0, float("-inf"), float("inf"))
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)
    #print("---------self.action OUTSIDE = ", self.action, "---------------\n\n")
    #print("--------- RED TEAM indices = ", gameState.getRedTeamIndices(), "---------------\n\n")
    return self.action
    #if self.index == 0: return self.action
    #if self.index == 2: return "Stop"

  def evaluate(self, gameState):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState)
    weights = self.getWeights(gameState)
    return features * weights

  def getFeatures(self, gameState):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    foodGrid = self.getFoodYouAreDefending(gameState)
    foodList = foodGrid.asList()
    capsuleList = gameState.getCapsules()
    redCapsules = []
    for capsule in capsuleList:
        if capsule[0] <= foodGrid.width/2:
            redCapsules.append(capsule)

    myState = gameState.getAgentState(self.index)
    myPos = myState.getPosition()

    features['successorScore'] = self.getScore(gameState)


    # if len(foodList) > 0: # This should always be True,  but better safe than sorry
    #   minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
    #   if minDistance == 0:
    #       features['1/distanceToSelfFood'] =
    #   else:
    #       features['1/distanceToSelfFood'] = 1/minDistance

    features['selfFoodRemaining'] = len(foodList)

    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    #normalGhosts = [a for a in ghosts if a.scaredTimer == 0]
    #scaredGhosts = [a for a in ghosts if a.scaredTimer != 0]

    # features['ghostDistance'] = 99
    # if len(normalGhosts) > 0:
    #   ndists = [self.getMazeDistance(myPos, a.getPosition()) for a in normalGhosts]
    #   features['ghostDistance'] = min(ndists)

    features['1/invaderDistance'] = 99
    if len(invaders) > 0:
      idists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['1/invaderDistance'] = 1/min(idists)
      features['invadersRemaining'] = -len(invaders)

    # features['1/scaredGhostDistance'] = 0
    # if len(scaredGhosts) > 0:
    #   sdists = [self.getMazeDistance(myPos, a.getPosition()) for a in scaredGhosts]
    #   features['1/scaredGhostDistance'] = 1/min(sdists)
    #   features['scaredGhostRemaining'] = -len(scaredGhosts)


    features['1/capsuleDistance'] = 0
    if len(redCapsules) > 0:
        cdists = [self.getMazeDistance(myPos, a) for a in redCapsules]
        if min(cdists) == 0:
            features['1/capsuleDistance'] = 5000
        else:
            features['1/capsuleDistance'] = 1/min(cdists)

    #features['capsulesRemaining'] = -len(redCapsules)

    # features['trapped'] = 0
    # if len(gameState.getLegalActions(self.index)) <= 2 and features['ghostDistance'] <= 6:
    #     features['trapped'] = -1

    #print("Blue Capsules = ", blueCapsules)
    #print(features)
    return features

  def getWeights(self, gameState):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    #return {'successorScore': 0, 'distanceToFood': -1000, 'foodRemaining': -100, 'ghostDistance': 10, 'scaredGhostDistance': -1, 'capsuleDistance': -1000}
    return {'successorScore': 10, '1/distanceToSelfFood': 0, 'selfFoodRemaining': 2000, '1/capsuleDistance': 100,\
            '1/invaderDistance': 9000, 'invadersRemaining': 99999}


class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)
