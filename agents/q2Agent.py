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
    pacman_position = currentGameState.getPacmanPosition()
    food_positions = currentGameState.getFood().asList()
    ghost_states = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    score = currentGameState.getScore()

    
    if food_positions:
        closest_food = min([util.manhattanDistance(pacman_position, food_position) for food_position in food_positions])
        farthest_food = max([util.manhattanDistance(pacman_position, food_position) for food_position in food_positions])
        score += 10.0 / closest_food  
        score += 5.0 / farthest_food 

        for food_position in food_positions:
            if food_position[0] == pacman_position[0] or food_position[1] == pacman_position[1]:
                score * 7 

    #score -= 3 * len(food_positions)  

    if capsules:
        closest_capsule_distance = min([util.manhattanDistance(pacman_position, capsule) for capsule in capsules])
        score -= 10 * (closest_capsule_distance )

    score -= 5 * len(capsules)

    for ghost_state in ghost_states:
        ghost_position = ghost_state.getPosition()
        ghost_distance = util.manhattanDistance(pacman_position, ghost_position)
        if ghost_state.scaredTimer > 0:
            score += 20.0 / (ghost_distance)
        else:
            if ghost_distance > 0:
                score -= 20.0 / (ghost_distance)
    
    if len(currentGameState.getLegalActions(0)) == 1 and currentGameState.getLegalActions(0)[0] == Directions.STOP:
        score -= 20

    if currentGameState.isWin():
        score += 1000  
    if currentGameState.isLose():
        score -= 1000  

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
                    if score > best_score:
                        best_score = score
                        best_action = action
                else:  # Ghost's turn (Minimizing)
                    if score < best_score:
                        best_score = score
                        best_action = action
            return best_action, best_score
        



            
    #     action, _ = self.minimax(0, 0, gameState)  
    #     return action 
    

    # def minimax(self, curr_depth, agent_index, gameState):
    #         num_agents = gameState.getNumAgents()
    #         if curr_depth == self.depth or gameState.isWin() or gameState.isLose():
    #             return None, self.evaluationFunction(gameState)

    #         legal_actions = gameState.getLegalActions(agent_index)
    #         if not legal_actions:
    #             return None, self.evaluationFunction(gameState)

    #         best_score = float('-inf') if agent_index == 0 else float('inf')
    #         best_action = None

    #         for action in legal_actions:
    #             next_game_state = gameState.generateSuccessor(agent_index, action)
    #             next_agent_index = (agent_index + 1) % num_agents
    #             next_depth = curr_depth + 1 if next_agent_index == 0 else curr_depth

    #             _, score = self.minimax(next_depth, next_agent_index, next_game_state)

    #             if agent_index == 0:  
    #                 if score > best_score:
    #                     best_score = score
    #                     best_action = action
    #             else: 
    #                 if score < best_score:
    #                     best_score = score
    #                     best_action = action

    #         return best_action, best_score
        


        
   