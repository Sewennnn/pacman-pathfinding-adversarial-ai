import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance


# def scoreEvaluationFunction(currentGameState):
#     """
#       This default evaluation function just returns the score of the state.
#       The score is the same one displayed in the Pacman GUI.

#       This evaluation function is meant for use with adversarial search agents
#       (not reflex agents).
#     """
#     return currentGameState.getScore()

def scoreEvaluationFunction( currentGameState: GameState):
    pacmanPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

  
    foodList = food.asList()
    if not foodList:
        return float('inf') 

    minFoodDist = min(manhattanDistance(pacmanPos, food) for food in foodList)
    ghostDist = min(manhattanDistance(pacmanPos, ghost.getPosition()) for ghost in ghostStates)

    score = currentGameState.getScore()

    
    if ghostDist <= 1:
        score -= 1000

 
    score += 10 / (minFoodDist + 1)

    return score


class Q2_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    
    @log_function
    def getAction(self, gameState: GameState):
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
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"

            
        action, _ = self.minimax(0, 0, gameState)  
        return action 
    

    def minimax(self, curr_depth, agent_index, gameState):
            num_agents = gameState.getNumAgents()
            if curr_depth == self.depth or gameState.isWin() or gameState.isLose():
                return None, self.evaluationFunction(gameState)

            legal_actions = gameState.getLegalActions(agent_index)
            if not legal_actions:
                return None, self.evaluationFunction(gameState)

            best_score = float('-inf') if agent_index == 0 else float('inf')
            best_action = None

            for action in legal_actions:
                next_game_state = gameState.generateSuccessor(agent_index, action)
                next_agent_index = (agent_index + 1) % num_agents
                next_depth = curr_depth + 1 if next_agent_index == 0 else curr_depth

                _, score = self.minimax(next_depth, next_agent_index, next_game_state)

                if agent_index == 0:  # Pacman's turn (Maximizing)
                    if score > best_score or (score == best_score and (best_action is None or action < best_action)):
                        best_score = score
                        best_action = action
                else:  # Ghost's turn (Minimizing)
                    if score < best_score or (score == best_score and (best_action is None or action > best_action)):
                        best_score = score
                        best_action = action

            return best_action, best_score
        


        
   