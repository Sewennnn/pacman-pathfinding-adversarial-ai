#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1b_problem import q1b_problem

def q1b_solver(problem: q1b_problem):
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
        self.pqueue = util.PriorityQueue()  
        self.closed_list = set() 
        self.cost_so_far = {}  
        self.came_from = {}  

def astar_initialise(problem: q1b_problem):
    # YOUR CODE HERE
    astarData = AStarData()
    
   
    start_state = problem.getStartState()
    goalState = problem.goalStates
    
   
    initial_cost = 0
    initial_heuristic = astar_heuristic(start_state, goalState)
    
    astarData.pqueue.push(start_state, initial_heuristic)
    astarData.cost_so_far[start_state] = initial_cost
    astarData.came_from[start_state] = None
    #print("start state", start_state)
    
    return astarData

def astar_loop_body(problem: q1b_problem, astarData: AStarData):
    # YOUR CODE HERE
    if astarData.pqueue.isEmpty():
        return True, None  
    
    current = astarData.pqueue.pop()
    
    
    if problem.isGoalState(current):
       
        path = []
        while astarData.came_from[current] is not None:
            prev_state, action = astarData.came_from[current]
         
            # dx, dy = current[0] - prev_state[0], current[1] - prev_state[1]
            # action = directionFromDelta(dx, dy)
            path.append(action)
            current = prev_state
        path.reverse()
        return True, path
    
    astarData.closed_list.add(current)
    print(current)
    
    for successor, action, step_cost in problem.getSuccessors(current):
        if successor in astarData.closed_list:
            continue
        
        new_cost = astarData.cost_so_far[current] + step_cost
        if successor not in astarData.cost_so_far or new_cost < astarData.cost_so_far[successor]:
            astarData.cost_so_far[successor] = new_cost
            priority = new_cost + astar_heuristic(successor, problem.goalStates)
            astarData.pqueue.push(successor, priority)
            astarData.came_from[successor] = current, action
    
    return False, None

def astar_heuristic(current, goals):
    # YOUR CODE HERE
    return min(util.manhattanDistance(current, goal) for goal in goals)


