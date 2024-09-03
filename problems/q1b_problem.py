import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1b_problem:
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.startingGameState: GameState = gameState
        self.startState = gameState.getPacmanPosition()
        self.goalStates = gameState.getFood().asList()
        print("all food positions", self.goalStates)

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        return self.startState 

    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        for gs in self.goalStates:
            if state == gs:
                return True
        return False

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        "*** YOUR CODE HERE ***"
        successors = [] 
        x, y = state
       
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x + dx), int(y + dy)
            if self.startingGameState.hasWall(next_x, next_y):
                continue
            next_state = (next_x, next_y)
            action = direction
            print("direction", direction)
            step_cost = 1
            successors.append((next_state, action, step_cost))
        return successors

