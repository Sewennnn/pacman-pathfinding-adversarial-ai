import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import Queue
import numpy as np


class q1c_problem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.
    Some useful data has been included here for you
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
        self.startState = (gameState.getPacmanPosition(), tuple(gameState.getFood().asList()))
        self.goalState = gameState.getFood().asList()
        self.walls = gameState.getWalls().asList()
        self.distance_matrix = q1c_problem.floyd_warshall(self.walls, gameState.getFood().asList())

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        return self.startState

    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        pacman_position, remaining_food = state
        return len(remaining_food) == 0

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
        pacman_position, remaining_food = state
        successors = []

        x, y = pacman_position
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(direction)
            next_x, next_y = int(x + dx), int(y + dy)
            if self.startingGameState.hasWall(next_x, next_y):
                continue
            next_position = (next_x, next_y)
            next_food = tuple(food for food in remaining_food if food != next_position)
            
            action = direction
            step_cost = 1
            successors.append(((next_position, next_food), action, step_cost))

        return successors
    
    
    def bfs_distance(walls, start_position, goal_position):

        queue = Queue()
        queue.push((start_position, 0))
        visited = set()
        visited.add(start_position)
        
        while not queue.isEmpty():
            current_position, distance = queue.pop()
            
            if current_position == goal_position:
                return distance
            
            x, y = current_position
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_position = (x + dx, y + dy)
                
                if (0 <= next_position[0] < len(walls)) and (0 <= next_position[1] < len(walls[0])):
                    if not walls[next_position[0]][next_position[1]] and next_position not in visited:
                        visited.add(next_position)
                        queue.push((next_position, distance + 1))
        
        return float('inf')
    
    
    def floyd_warshall(walls, nodes):
    
        num_nodes = len(nodes)
        dist = np.full((num_nodes, num_nodes), float('inf'))
        
        # Initialize distances
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if node1 == node2:
                    dist[i][j] = 0
                else:
                    dist[i][j] = q1c_problem.bfs_distance(walls, node1, node2)
        
        # Floyd-Warshall algorithm
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        
        return dist
    

    