#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1a_problem import q1a_problem

import heapq

def q1a_solver(problem: q1a_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

#-------------------#
# DO NOT MODIFY END #
#-------------------#

class AStarData:
    # YOUR CODE HERE
    def __init__(self):
        self.open_list = []  # Priority queue (min-heap) for open nodes
        self.closed_list = set()  # Set for closed nodes
        self.came_from = {}  # Dictionary to reconstruct the path
        self.cost_so_far = {}  # Dictionary to keep track of costs

def astar_initialise(problem: q1a_problem):
    # YOUR CODE HERE
    # astarData = AStarData()
    # astarData.x = 'stuff'
    # astarData.y = 123
    #return astarData
    astarData = AStarData()
    
    start_state = problem.getStartState()
    goal_state = problem.goalState
    
    # Initialize the open list with the start state
    initial_cost = 0
    initial_heuristic = astar_heuristic(start_state, goal_state)
    heapq.heappush(astarData.open_list, (initial_cost + initial_heuristic, initial_cost, start_state))
    
    astarData.came_from[start_state] = None
    astarData.cost_so_far[start_state] = initial_cost
    
    return astarData

def astar_loop_body(problem: q1a_problem, astarData: AStarData):
    # YOUR CODE HERE
    #util.raiseNotDefined()  # Delete this line
    if not astarData.open_list:
        return True, None  # No solution found
    
    _, current_cost, current = heapq.heappop(astarData.open_list)
    
    if problem.isGoalState(current):
        # Goal found, reconstruct path
        path = []
        while current in astarData.came_from:
            prev_state = astarData.came_from[current]
            if prev_state is not None:
                action = (current[0] - prev_state[0], current[1] - prev_state[1])  # Assuming action can be derived this way
                path.append(action)
            current = prev_state
        path.reverse()
        return True, path
    
    astarData.closed_list.add(current)
    
    for successor, action, step_cost in problem.getSuccessors(current):
        if successor in astarData.closed_list:
            continue
        
        new_cost = astarData.cost_so_far[current] + step_cost
        if successor not in astarData.cost_so_far or new_cost < astarData.cost_so_far[successor]:
            astarData.cost_so_far[successor] = new_cost
            priority = new_cost + astar_heuristic(successor, problem.goalState)
            heapq.heappush(astarData.open_list, (priority, new_cost, successor))
            astarData.came_from[successor] = current
    
    return False, None

def astar_heuristic(current, goal):
    # YOUR CODE HERE
    #return 0
    x1, y1 = current
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)  # Manhattan distance
