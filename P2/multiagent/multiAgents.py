# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        successorGameState = currentGameState.generatePacmanSuccessor(action)#state
        newPos = successorGameState.getPacmanPosition()#tuple
        newFood = successorGameState.getFood()#instance
        newGhostStates = successorGameState.getGhostStates()#list
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]#list
        score = successorGameState.getScore()
        cap = currentGameState.getCapsules()
        #Idea resting based on ghost proximity and add based on we are on food
        for ghosts in newGhostStates:
          pos = ghosts.getPosition()
          dist = manhattanDistance(pos,newPos)
          if(dist == 1):
            score -= 15
          if(dist <= 3 and dist != 1):
            score -= 10
          if(dist <= 5 and dist > 3 and dist != 1):
            score -= 5
        
        if newFood[newPos[0]][newPos[1]]:
          score += 5
        else:
          score -= 5

        return score

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

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
        """
        def minimax(gameState, d):
          return maxValue(gameState, d)#we start with max(pacman)

        def maxValue(gameState,d):#this is for pacman!

          v = (float("-inf"),)#initialize utility/action default theres no action
          actions = gameState.getLegalActions(0)#get possible moves

          if gameState.isWin() or gameState.isLose() or self.depth == d or len(actions) == 0:#check terminal
            v = (self.evaluationFunction(gameState),)#terminal case first return to archieve(just score)
            return v
          #if we arent terminal node we need to check our moves and check ghost moves
          for action in actions:#possible moves
            successor = gameState.generateSuccessor(0,action)#if we do this action we generate this state
            v = max(v, (minValue(successor,1,d)[0],action))#we try to get the lowest score for ghost if we
            #do this move(note that since we know that terminal returns no move we only care about score [1])

          return v

        def minValue( gameState, index, d):#this is for ghosts!

          v = (float("inf"),)#initialize utility
          actions = gameState.getLegalActions(index)#possible moves

          if gameState.isWin() or gameState.isLose() or self.depth == d or len(actions) == 0:#terminal node
            v = (self.evaluationFunction(gameState),)#terminal case first return to archieve(just score)
            return v

          for action in actions:
            successor = gameState.generateSuccessor(index,action)#if we do this action we generate this state
            
            if index+1 == gameState.getNumAgents():#we are the last ghost we need to return to pacman
              v = min(v,(maxValue(successor, d+1)[0],action))#we call maxv (still min tho!)
            else:
              v = min(v,(minValue(successor, index+1,d)[0],action))#we are the next ghost so we use again minV
            #do this move(note that since we know that terminal returns no move we only care about score [1])

          return v

        return minimax(gameState,0)[1]#action
          
          
          



        

          
        
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        def AlphaBeta(gameState, d):
          alpha = -float("inf")
          beta = float("inf")
          return maxValue(gameState,d,alpha,beta)#we start with max(pacman)

        def maxValue(gameState,d,alpha,beta):#this is for pacman!

          v = (-float("inf"),)#initialize utility/action default theres no action
          actions = gameState.getLegalActions(0)#get possible moves

          if gameState.isWin() or gameState.isLose() or self.depth == d or len(actions) == 0:#check terminal
            v = (self.evaluationFunction(gameState),)#terminal case first return to archieve(just score)
            return v
          #if we arent terminal node we need to check our moves and check ghost moves
          for action in actions:#possible moves
            successor = gameState.generateSuccessor(0,action)#if we do this action we generate this state
            v = max(v, (minValue(successor,1,d,alpha,beta)[0],action))#we try to get the lowest score for ghost if we
            #do this move(note that since we know that terminal returns no move we only care about score [1])
            if v[0] > beta:#we cut(no more expanding)
              return v
            alpha = max(alpha,v[0])#update alpha

          return v

        def minValue(gameState,index,d,alpha,beta):#this is for ghosts!

          v = (float("inf"),)#initialize utility
          actions = gameState.getLegalActions(index)#possible moves

          if gameState.isWin() or gameState.isLose() or self.depth == d or len(actions) == 0:#terminal node
            v = (self.evaluationFunction(gameState),)#terminal case first return to archieve(just score)
            return v

          for action in actions:
            successor = gameState.generateSuccessor(index,action)#if we do this action we generate this state
            
            if index+1 == gameState.getNumAgents():#we are the last ghost we need to return to pacman
              v = min(v,(maxValue(successor,d+1,alpha,beta)[0],action))#we call maxv (still min tho!)
            else:
              v = min(v,(minValue(successor,index+1,d,alpha,beta)[0],action))#we are the next ghost so we use again minV
            #do this move(note that since we know that terminal returns no move we only care about score [1])
            if v[0] < alpha:#we cut(no more expand)
              return v
            beta = min(beta,v[0])#updating beta
          
          return v

        return AlphaBeta(gameState,0)[1]#action

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
        def expectimax(gameState,index,d):
          if index == gameState.getNumAgents():
            d += 1
            index = 0
          #terminal node
          if gameState.isWin() or gameState.isLose() or self.depth == d:
            return self.evaluationFunction(gameState)
          #max node
          if index == 0:
            return maxValue(gameState,d)
          else:#exp node
            return expValue(gameState,index,d)

          
        def maxValue(gameState,d):
          v = (-float('inf'),)
          actions = gameState.getLegalActions(0)
          for action in actions:
            successor = gameState.generateSuccessor(0,action)
            v = max(v,(expectimax(successor,1,d),action))
          return v

        def expValue(gameState,index,d):
          v = 0
          actions = gameState.getLegalActions(index)
          prob = 1./float(len(actions))
          for action in actions:
            successor = gameState.generateSuccessor(index,action)
            exp = expectimax(successor,index+1,d)
            if type(exp) == tuple:
              v += exp[0]
            else:
              v += exp
          return v*prob
        return expectimax(gameState,0,0)[1]
   
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
   
    newPos = currentGameState.getPacmanPosition()#tuple
    newFood = currentGameState.getFood().asList()#instance
    newGhostStates = currentGameState.getGhostStates()#list
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]#list
    score = currentGameState.getScore()
    cap = currentGameState.getCapsules()
    #Idea: 1st problem solution does not work well here 9 of 10 got nice score but 1 gets -6000
    #So I though about using the base score but decrease it based on how far we are from farest food
    foodDist = [-manhattanDistance(food,newPos) for food in newFood]
    if not foodDist:
      foodDist = [0]

    return max(foodDist) + currentGameState.getScore()

# Abbreviation
better = betterEvaluationFunction

