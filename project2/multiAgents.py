# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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


  def getAction(self, gamestate):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a gamestate and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gamestate.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gamestate, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentgamestate, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    gamestates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a gamestate (pacman.py)
    successorgamestate = currentgamestate.generatePacmanSuccessor(action)  # type: object
    newPos = successorgamestate.getPacmanPosition()
    newFood = successorgamestate.getFood()
    newGhostStates = successorgamestate.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    score = successorgamestate.getScore()
    currentFood = currentgamestate.getFood().asList()
    newFood = newFood.asList()
    ghostPos = successorgamestate.getGhostPositions()
    score = score + len(currentFood) - len(newFood) * 100
    max = 0
    min = 0
    for food in newFood:
      x, y = food
      dis = abs(newPos[0] - x) + abs(newPos[1] - y)
      if max < dis:
        max = dis
      if min > dis or min == 0:
        min = dis
    score = score - max - min
    for pos in ghostPos:
      x, y = pos
      dis = abs(newPos[0] - x) + abs(newPos[1] - y)
      score = score + dis * 1.3
    score = score - len(newFood) + newScaredTimes[0]
    return score

def scoreEvaluationFunction(currentgamestate):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentgamestate.getScore()

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

  def getAction(self, gamestate):
    """
      Returns the minimax action from the current gamestate using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gamestate.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gamestate.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gamestate.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    def rmstop(gamestate):
      move = []
      for action in gamestate.getLegalActions(0):
        if action != "Stop":
          move.append(action)
      return move

    agents = gamestate.getNumAgents()
    actionv = []

    def Max(gamestate, depth):
      if depth > self.depth * agents:
        return self.evaluationFunction(gamestate)
      v = float('-inf')
      for action in gamestate.getLegalActions(0):
        if action != "Stop":
          successorState = gamestate.generateSuccessor(0, action)
          v = max(v, Min(successorState, depth + 1, 1))
          if depth == 1:
            actionv.append(v)
      return v

    def Min(gamestate, depth, index):
      if gamestate.isWin() or gamestate.isLose():
        return self.evaluationFunction(gamestate)
      v = float("inf")

      for action in gamestate.getLegalActions(index):
        successorState = gamestate.generateSuccessor(index, action)
        if depth % agents != 0:
          v = min(v, Min(successorState, depth + 1, index + 1))
        else:
          v = min(v, Max(successorState, depth + 1))
      return v

    Max(gamestate, 1)
    maxv = actionv.index(max(actionv))
    move = rmstop(gamestate)[maxv]
    return move

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gamestate):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def rmstop(gamestate):
      move = []
      for action in gamestate.getLegalActions(0):
        if action != "Stop":
          move.append(action)
      return move

    alpha = float('-inf')
    beta = float('inf')
    agents = gamestate.getNumAgents()
    actionv = []

    def Max(gamestate, depth, alpha, beta):
      if depth > self.depth * agents:
        return self.evaluationFunction(gamestate)
      v = float('-inf')
      for action in gamestate.getLegalActions(0):
        if action != "Stop":
          successorState = gamestate.generateSuccessor(0, action)
          v = max(v, Min(successorState, depth + 1, 1, alpha, beta))
          alpha = max(alpha, v)
          if alpha >= beta:
            return v
          if depth == 1:
            actionv.append(v)
      return v

    def Min(gamestate, depth, index, alpha, beta):
      if gamestate.isWin() or gamestate.isLose():
        return self.evaluationFunction(gamestate)
      v = float("inf")

      for action in gamestate.getLegalActions(index):
        successorState = gamestate.generateSuccessor(index, action)
        if depth % agents != 0:
          v = min(v, Min(successorState, depth + 1, index + 1, alpha, beta))
        else:
          v = min(v, Max(successorState, depth + 1, alpha, beta))
          beta = min(beta, v)
          if alpha >= beta:
            return v
      return v

    Max(gamestate, 1, alpha, beta)
    maxv = actionv.index(max(actionv))
    move = rmstop(gamestate)[maxv]
    return move 

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gamestate):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***" 
    agents=gamestate.getNumAgents()

    def expectMax(gamestate, depth, index):
        if gamestate.isWin() or gamestate.isLose():
          return self.evaluationFunction(gamestate)
        legalActions = gamestate.getLegalActions(index)
        p = 1.0/len(legalActions)
        v=0
        for action in gamestate.getLegalActions(index):
            List = []
            successors=gamestate.generateSuccessor(index, action)
            if index == (agents-1):
                v = min(v, Max(successors, depth))
            else:
                v +=p*expectMax(successors, depth, index + 1)
        List.append(v)
        return min(List)

    def Max(gamestate, depth):
        depth += 1
        v = float('-Inf')
        if gamestate.isWin() or gamestate.isLose() or depth >= self.depth:
            return self.evaluationFunction(gamestate)
        for action in gamestate.getLegalActions():
            if action != "Stop": 
                v = max(v, expectMax(gamestate.generatePacmanSuccessor(action), depth, 1))
        return v
    
    MaxValue = -99999999
    movement=[]
    for action in gamestate.getLegalActions():
        if action != "Stop":
            v = expectMax(gamestate.generatePacmanSuccessor(action), 0, 1)
            if v > MaxValue:
                MaxValue = v
                move = action
            movement.append(move)
    return movement.pop()  


def betterEvaluationFunction(currentgamestate):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  successorgamestate = currentgamestate 
  newPos = successorgamestate.getPacmanPosition()
  newFood = successorgamestate.getFood()
  newGhostStates = successorgamestate.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

  score = successorgamestate.getScore()
  newFood = newFood.asList()
  ghostPos = successorgamestate.getGhostPositions()
  score = score - len(newFood) * 100
  max = 0
  min = 0
  for food in newFood:
    x, y = food
    dis = abs(newPos[0] - x) + abs(newPos[1] - y)
    if max < dis:
      max = dis
    if min > dis: #or min == 0:
      min = dis
  score = score - max - min
  for pos in ghostPos:
    x, y = pos
    dis = abs(newPos[0] - x) + abs(newPos[1] - y)
    score = score + dis* 1.3
  print newScaredTimes[0]
  score = score - len(newFood) - newScaredTimes[0]
  return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gamestate):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

