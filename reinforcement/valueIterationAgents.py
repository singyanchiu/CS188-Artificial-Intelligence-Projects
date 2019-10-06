# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here

        # def computeVValue(state, current_k):
        #     #print("State =", state)
        #     if self.mdp.isTerminal(state) or current_k >= self.iterations:
        #         return 0
        #     newQCandidates = []
        #     actions = self.mdp.getPossibleActions(state)
        #     for action in actions:
        #         newQCandidate = 0
        #         #print("action =", action)
        #         transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        #         for transitionStateAndProb in transitionStatesAndProbs:
        #             nextState = transitionStateAndProb[0]
        #             #print("nextState =", nextState)
        #             prob = transitionStateAndProb[1]
        #             #print("prob = ", prob)
        #             reward = self.mdp.getReward(state, action, nextState)
        #             #print("reward = ", reward)
        #             newQCandidate += prob*(reward + self.discount * computeVValue(nextState, current_k+1))
        #         newQCandidates.append(newQCandidate)
        #         #print("newVcandidate after iterating all probability = ", newVCandidate)
        #     return max(newQCandidates)

        self.tempValues = util.Counter()
        allStates = self.mdp.getStates()

        for i in range(self.iterations):
            self.tempValues = self.values.copy()
            #print("self.tempValues =", self.tempValues)
            for state in allStates:
                newQCandidates = []
                actions = self.mdp.getPossibleActions(state)
                if len(actions) > 0:
                    for action in actions:
                        newQCandidate = 0
                        #print("action =", action)
                        transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
                        for transitionStateAndProb in transitionStatesAndProbs:
                            nextState = transitionStateAndProb[0]
                            #print("nextState =", nextState)
                            prob = transitionStateAndProb[1]
                            #print("prob = ", prob)
                            reward = self.mdp.getReward(state, action, nextState)
                            #print("reward = ", reward)
                            newQCandidate += prob*(reward + self.discount * self.tempValues[nextState])
                        newQCandidates.append(newQCandidate)
                        #print("newVcandidate after iterating all probability = ", newVCandidate)
                    self.values[state] = max(newQCandidates)

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        QValue = 0
        transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        for transitionStateAndProb in transitionStatesAndProbs:
            nextState = transitionStateAndProb[0]
            prob = transitionStateAndProb[1]
            reward = self.mdp.getReward(state, action, nextState)
            QValue += prob*(reward + self.discount * self.values[nextState])
        return QValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        actions = self.mdp.getPossibleActions(state)
        QValues = util.Counter()
        if len(actions)>0:
            for action in actions:
                QValues[action] = (self.computeQValueFromValues(state, action))
            #rint("QValues.argMax() =", QValues.argMax())
            return QValues.argMax()
        else:
            return None

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        self.numStates = 0
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        self.tempValues = util.Counter()
        allStates = self.mdp.getStates()
        self.numStates = len(allStates)
        i = 0
        currentIndex = 0

        while currentIndex < self.iterations:
            if i >= self.numStates:
                i = 0
            state = allStates[i]
            newQCandidates = []
            actions = self.mdp.getPossibleActions(state)
            if len(actions) > 0:
                for action in actions:
                    newQCandidate = 0
                    transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
                    for transitionStateAndProb in transitionStatesAndProbs:
                        nextState = transitionStateAndProb[0]
                        prob = transitionStateAndProb[1]
                        reward = self.mdp.getReward(state, action, nextState)
                        newQCandidate += prob*(reward + self.discount * self.values[nextState])
                    newQCandidates.append(newQCandidate)
                self.values[state] = max(newQCandidates)
            i += 1
            currentIndex += 1

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):

        def computeMaxQ(state):
            newQCandidates = []
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                newQCandidate = 0
                transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
                for transitionStateAndProb in transitionStatesAndProbs:
                    nextState = transitionStateAndProb[0]
                    prob = transitionStateAndProb[1]
                    reward = self.mdp.getReward(state, action, nextState)
                    newQCandidate += prob*(reward + self.discount * self.values[nextState])
                newQCandidates.append(newQCandidate)
            return max(newQCandidates)

        #Compute predecessors of all states
        stateAndPredecessors = {}
        allStates = self.mdp.getStates()
        for state in allStates:
            predecessors = set()
            for tempstate in allStates:
                actions = self.mdp.getPossibleActions(tempstate)
                for action in actions:
                    transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(tempstate, action)
                    for transitionStateAndProb in transitionStatesAndProbs:
                        if state == transitionStateAndProb[0]:
                            predecessors.add(tempstate)
            stateAndPredecessors[state] = predecessors
        #print(stateAndPredecessors)

        #Initialize an empty priority queue
        PQueue = util.PriorityQueue()
        tempValueDiffs = {}

        #Push states and its minus diff into PQueue
        for state in allStates:
            if state != "TERMINAL_STATE":
                MaxQ = computeMaxQ(state)
                diff = abs(MaxQ - self.values[state])
                PQueue.push(state, -diff)

        #iterations
        for i in range(self.iterations):
            if PQueue.isEmpty():
                break
            currentState = PQueue.pop()
            self.values[currentState] = computeMaxQ(currentState)
            for p in stateAndPredecessors[currentState]:
                MaxQofP = computeMaxQ(p)
                diff = abs(MaxQofP - self.values[p])
                if diff > self.theta:
                    PQueue.update(p, -diff)
