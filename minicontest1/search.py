# search.py
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class Node:
    def __init__(self):
        self.list = []

    def getNodeState(self):
        return self.list[len(self.list)-1][0]

    def appendNode(self, newNode):
        return self.list + [newNode]

    def getNodeTotalCost(self):
        nodeTotalCost = 0
        for nodeItem in self.list:
            nodeTotalCost = nodeTotalCost + nodeItem[2]
        return nodeTotalCost

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    #from game import Directions
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    """
    print("Start node: ", startNode.list)
    print("Start node state: ", startNode.getNodeState())

    successors = problem.getSuccessors(startNode.getNodeState())

    for successor in successors:
        childNode = Node(startState, stop)
        childNode.list = startNode.appendNode((successor[0],successor[1]))
        print("Current child node: ", childNode.list)
        print("Current child node state: ", childNode.getNodeState())
    """
    closed = []
    startState = problem.getStartState()
    fringe = util.Stack()
    startNode = Node()
    startNode.list = [((startState),"Stop")]
    fringe.push(startNode)

    while True:
        #print("Current fringe: \n", "\n".join(str(node.list) for node in fringe.list))
        if fringe.isEmpty():
            return
        node = fringe.pop()
        #print("Current node:", node.list)
        if problem.isGoalState(node.getNodeState()):
            break
        if node.getNodeState() not in closed:
            closed.append(node.getNodeState())
            #print("Current closed: ", closed)

            successors = problem.getSuccessors(node.getNodeState())
            #print("Current Successors: ", successors)

            for successor in successors:
                childNode = Node()
                childNode.list = node.appendNode((successor[0],successor[1]))
                #print("Current child node: ", childNode.list)
                #print("Current child node state: ", childNode.getNodeState())
                fringe.push(childNode)

    actionList = []
    #print("Solution path: ", node.list)
    #iterate through the resulted node object to retrieve the list of actions taken
    for item in node.list[1:len(node.list)]:
        actionList.append(item[1])
    #print("actionList: ", actionList)
    return actionList
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    closed = []
    startState = problem.getStartState()
    fringe = util.Queue()
    startNode = Node()
    startNode.list = [((startState),"Stop")]
    fringe.push(startNode)

    while True:
        if fringe.isEmpty():
            return
        node = fringe.pop()
        if problem.isGoalState(node.getNodeState()):
            break
        if node.getNodeState() not in closed:
            closed.append(node.getNodeState())

            successors = problem.getSuccessors(node.getNodeState())

            for successor in successors:
                childNode = Node()
                childNode.list = node.appendNode((successor[0],successor[1]))
                fringe.push(childNode)

    actionList = []

    for item in node.list[1:len(node.list)]:
        actionList.append(item[1])
    return actionList

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    closed = []
    startState = problem.getStartState()
    fringe = util.PriorityQueue()
    startNode = Node()
    startNode.list = [((startState),"Stop",0)]
    fringe.push(startNode,0)
    nodeTotalCost = 0

    while True:
        if fringe.isEmpty():
            return
        node = fringe.pop()
        if problem.isGoalState(node.getNodeState()):
            break
        if node.getNodeState() not in closed:
            closed.append(node.getNodeState())

            successors = problem.getSuccessors(node.getNodeState())

            for successor in successors:
                childNode = Node()
                childNode.list = node.appendNode(successor)
                fringe.push(childNode, childNode.getNodeTotalCost())

    actionList = []

    for item in node.list[1:len(node.list)]:
        actionList.append(item[1])
    return actionList

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    closed = []
    startState = problem.getStartState()
    fringe = util.PriorityQueue()
    startNode = Node()
    startNode.list = [((startState),"Stop",0)]
    fringe.push(startNode,0)
    nodeTotalCost = 0

    #dummy test line. Delete after test
    #heuristic(startState,problem)

    while True:
        if fringe.isEmpty():
            return
        node = fringe.pop()
        #print("heuristic = ", heuristic(node.getNodeState(),problem))
        #print("Cost to node = ", node.getNodeTotalCost())
        #print("heuristic + cost =", heuristic(node.getNodeState(),problem)+node.getNodeTotalCost(),"\n")
        if problem.isGoalState(node.getNodeState()):
            break
        if node.getNodeState() not in closed:
            closed.append(node.getNodeState())

            successors = problem.getSuccessors(node.getNodeState())

            for successor in successors:
                childNode = Node()
                childNode.list = node.appendNode(successor)
                fringe.push(childNode, childNode.getNodeTotalCost() + heuristic(childNode.getNodeState(),problem))
                #print("\n heuristic =", heuristic(childNode.getNodeState(),problem))

    actionList = []

    for item in node.list[1:len(node.list)]:
        actionList.append(item[1])
    return actionList

    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
