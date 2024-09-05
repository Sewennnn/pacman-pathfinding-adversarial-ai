import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class Q2_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
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
        # def alpha_beta_search(state, depth, alpha, beta, agentIndex):
        #     num_agents = state.getNumAgents()
            
        #     if depth == 0 or state.isWin() or state.isLose():
        #         return self.evaluationFunction(state), None
            
        #     if agentIndex == 0:
        #         value = float('-inf')
        #         best_action = None
        #         for action in state.getLegalActions(agentIndex):
        #             successor = state.generateSuccessor(agentIndex, action)
        #             next_value, _ = alpha_beta_search(successor, depth, alpha, beta, (agentIndex + 1) % num_agents)
        #             if next_value > value:
        #                 value = next_value
        #                 best_action = action
        #             alpha = max(alpha, value)
        #             if beta <= alpha:
        #                 break 
        #         return value, best_action
            
          
        #     else:
        #         value = float('inf')
        #         for action in state.getLegalActions(agentIndex):
        #             successor = state.generateSuccessor(agentIndex, action)
        #             next_agent = (agentIndex + 1) % num_agents
        #             next_depth = depth - 1 if next_agent == 0 else depth
        #             next_value, _ = alpha_beta_search(successor, next_depth, alpha, beta, next_agent)
        #             if next_value < value:
        #                 value = next_value
        #             beta = min(beta, value)
        #             if beta <= alpha:
        #                 break  
        #         return value, None

        
        # _, action = alpha_beta_search(gameState, self.depth, float('-inf'), float('inf'), 0)
        # return action