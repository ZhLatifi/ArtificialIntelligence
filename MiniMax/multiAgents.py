from Agents import Agent
import util
import random


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.index = 0 # your agent always has index
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        It takes a GameState and returns a tuple representing a position on the game board.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions(self.index)

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed successor
        GameStates (Game.py) and returns a number, where higher numbers are better.
        You can try and change this evaluation function if you want but it is not necessary.
        """
        nextGameState = currentGameState.generateSuccessor(self.index, action)
        return nextGameState.getScore(self.index) - currentGameState.getScore(self.index)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    Every player's score is the number of pieces they have placed on the board.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore(0)


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (Agents.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2', **kwargs):
        self.index = 0 # your agent always has index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent which extends MultiAgentSearchAgent and is supposed to be implementing a minimax tree with a certain depth.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)

    def getAction(self, state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction

        But before getting your hands dirty, look at these functions:

        gameState.isGameFinished() -> bool
        gameState.getNumAgents() -> int
        gameState.generateSuccessor(agentIndex, action) -> GameState
        gameState.getLegalActions(agentIndex) -> list
        self.evaluationFunction(gameState) -> float
        """
        "*** YOUR CODE HERE ***"
        finalChoice = float("-inf")
        actions = state.getLegalActions(0)
        for action in actions:
            value = self.minChoice(0, 1, state.generateSuccessor(0, action))
            if value > finalChoice:
                finalChoice = value
                nextAction = action
        return nextAction

    def maxChoice(self, depth, agent, state):
        finalChoice = float("-inf")
        actions = state.getLegalActions(agent)
        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)
        else:
            for action in actions:
                maxValue = self.minChoice(depth, 1, state.generateSuccessor(agent, action))
                if maxValue > finalChoice:
                    finalChoice = maxValue
            return finalChoice

    def minChoice(self, depth, agent, state):
        agentNum = state.getNumAgents()
        actions = state.getLegalActions(agent)
        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)
        else:
            finalChoice = float("inf")
            for action in actions:
                if agent == agentNum - 1 or agentNum == 1:
                    minValue = self.maxChoice(depth + 1, 0, state.generateSuccessor(agent, action))
                    if minValue < finalChoice:
                        finalChoice = minValue
                else:
                    minValue = self.minChoice(depth, agent + 1, state.generateSuccessor(agent, action))
                    if minValue < finalChoice:
                        finalChoice = minValue
            return finalChoice


        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning. It is very similar to the MinimaxAgent but you need to implement the alpha-beta pruning algorithm too.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction

        You should keep track of alpha and beta in each node to be able to implement alpha-beta pruning.
        """
        "*** YOUR CODE HERE ***"
        alpha = float("-inf")
        beta = float("inf")
        for action in gameState.getLegalActions(0):
            value = self.minChoice(0, 1, gameState.generateSuccessor(0, action), alpha, beta)
            if alpha < value:
                alpha = value
                nextAction = action
        return nextAction

    def minChoice(self, depth, agent, state, alpha, beta):
        agentNum = state.getNumAgents()
        actions = state.getLegalActions(agent)
        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)
        else:
            value = float("inf")
            for action in actions:
                if agent == agentNum - 1 or agentNum == 1:
                    minValue = self.maxChoice(depth + 1, 0, state.generateSuccessor(agent, action), alpha, beta)
                    if minValue < value:
                        value = minValue
                else:
                    minValue = self.minChoice(depth, agent + 1, state.generateSuccessor(agent, action), alpha, beta)
                    if minValue < value:
                        value = minValue
                if value < alpha:
                    return value
                if value <= beta:
                    beta = value
            return value

    def maxChoice(self, depth, agent, state, alpha, beta):
        actions = state.getLegalActions(agent)
        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)
        else:
            value = -10000
            for action in actions:
                maxValue = self.minChoice(depth, 1, state.generateSuccessor(agent, action), alpha, beta)
                if maxValue > value:
                    value = maxValue
                if value > beta:
                    return value
                if value >= alpha:
                    alpha = value
        return value

        util.raiseNotDefined()
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent which has a max node for your agent but every other node is a chance node.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(**kwargs)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All opponents should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        actions = gameState.getLegalActions(0)
        finalChoice = float("-inf")
        for action in actions:
            value = self.expectValue(0, 1, gameState.generateSuccessor(0, action))
            if value > finalChoice:
                finalChoice = value
                nextAction = action

        return nextAction

    def maxChoice(self, depth, agent, state):

        actions = state.getLegalActions(agent)
        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)
        else:
            finalChoice = float("-inf")
            for action in actions:
                maxValue = self.expectValue(depth, agent + 1, state.generateSuccessor(agent, action))
                if maxValue > finalChoice:
                    finalChoice = maxValue
            return finalChoice

    def expectValue(self, depth, agent, state):
        agentNum = state.getNumAgents()
        actions = state.getLegalActions(agent)
        if depth == self.depth or len(actions) == 0:
            return self.evaluationFunction(state)
        else:
            expect = 0
            for action in actions:
                if agent == agentNum - 1:
                    expect += self.maxChoice(depth + 1, 0, state.generateSuccessor(agent, action))
                else:
                    expect += self.expectValue(depth, agent + 1, state.generateSuccessor(agent, action))
            return expect / len(actions)

        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme evaluation function.

    You are asked to read the following paper on othello heuristics and extend it for two to four player rollit game.
    Implementing a good stability heuristic has extra points.
    Any other brilliant ideas are also accepted. Just try and be original.

    The paper: Sannidhanam, Vaishnavi, and Muthukaruppan Annamalai. "An analysis of heuristics in othello." (2015).

    Here are also some functions you will need to use:
    
    gameState.getPieces(index) -> list
    gameState.getCorners() -> 4-tuple
    gameState.getScore() -> list
    gameState.getScore(index) -> int

    """
    
    "*** YOUR CODE HERE ***"

    # parity
    agentNum = currentGameState.getNumAgents()
    if agentNum == 2:
        parity = (100 * (currentGameState.getScore(0) - currentGameState.getScore(1))) / (
                    currentGameState.getScore(0) + currentGameState.getScore(1))
    else:
        competitors = sum(currentGameState.getScore(agent) for agent in range(1, agentNum))
        parity = 100 * (currentGameState.getScore(0) - competitors) / (currentGameState.getScore(0) + competitors)

    # corners
    add = 0
    myUtility = 0
    compUtility = 0
    for free in currentGameState.getCorners():
        add += free
        value = free
        if value == 0:
            myUtility += 1
        elif value > 0:
            compUtility += 1

    if add != -4:
        corners = (100 * (myUtility - compUtility)) / (myUtility + compUtility)
    else:
        corners = 0

    # mobility
    agentNum = currentGameState.getNumAgents()
    myActions = len(currentGameState.getLegalActions(0))
    if agentNum == 2:
        compActions = len(currentGameState.getLegalActions(1))
    else:
        compActions = sum(len(currentGameState.getLegalActions(agent)) for agent in range(1, agentNum))
    if myActions + compActions != 0:
        mobility = 100 * (myActions - compActions) / (myActions + compActions)
    else:
        mobility = 0

    # stability

    # adding different weights to different evaluations
    betterEvaluation = (10 * parity) + (200 * corners) + (30 * mobility)
    return betterEvaluation
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction