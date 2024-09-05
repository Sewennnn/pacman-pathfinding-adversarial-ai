#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

def q1c_solver(problem: q1c_problem):
    # YOUR CODE HERE
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    return result

class AStarData:
    def __init__(self):
        self.pqueue = util.PriorityQueue()  
        self.closed_list = set() 
        self.cost_so_far = {}  
        self.came_from = {} 

def astar_initialise(problem: q1c_problem):
    astarData = AStarData()
    start_state = problem.getStartState()
    goalState = problem.goalState
    
    initial_cost = 0
    initial_heuristic = astar_heuristic(start_state, goalState)
    
    astarData.pqueue.push(start_state, (initial_heuristic, initial_cost))
    astarData.cost_so_far[start_state] = initial_cost  
    astarData.came_from[start_state] = None
    
    return astarData

def astar_loop_body(problem: q1c_problem, astarData: AStarData):
    # YOUR CODE HERE
    
    if astarData.pqueue.isEmpty():
        return True, None  
    
    current = astarData.pqueue.pop()
    
    if problem.isGoalState(current):
        path = []
        while astarData.came_from[current] is not None:
            prev_state, action = astarData.came_from[current]
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
            heuristic = astar_heuristic(successor, problem.goalState)
            priority = new_cost + heuristic 
            
            astarData.pqueue.push(successor, (priority, -new_cost))
            astarData.came_from[successor] = current, action
    
    return False, None

def astar_heuristic(state, goals):
    # pacman_position, remaining_food, walls = state
    # if not remaining_food:
    #     return 0

    
    #return sum(util.manhattanDistance(pacman_position, food) for food in remaining_food)
#     rows = len(set([f[0] for f in remaining_food]))  
#     cols = len(set([f[1] for f in remaining_food]))  
#     return rows + cols
    pacman_position, remaining_food, walls = state
    if not remaining_food:
        return 0
    
    distances = [util.manhattanDistance(pacman_position, food) for food in remaining_food]
    
   
    max_food_distance = 0
    for i in range(len(remaining_food)):
        for j in range(i + 1, len(remaining_food)):
            food1 = remaining_food[i]
            food2 = remaining_food[j]
            distance = util.manhattanDistance(food1, food2)
            max_food_distance = max(max_food_distance, distance)

    return min(distances) + max_food_distance

   
    # nearest_food = min(remaining_food, key=lambda food: mazeDistance(pacman_position, food, walls))
    # return mazeDistance(pacman_position, nearest_food, walls)






# if len(state.getFood().asList()) > 0:
#         return 1
#     return 0


# def mazeDistance(start, goal, walls):
#     rows, cols = len(walls), len(walls[0])
#     queue = util.Queue()
#     queue.push(tuple(start))  # Use tuple for start
#     distances = {tuple(start): 0}  # Use tuple for distances key

#     while not queue.isEmpty():
#         current = tuple(queue.pop())  # Convert to tuple
#         current_distance = distances[current]

#         for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
#             next_position = (current[0] + direction[0], current[1] + direction[1])

#             if (0 <= next_position[0] < rows and 
#                 0 <= next_position[1] < cols and 
#                 not walls[next_position[0]][next_position[1]] and 
#                 next_position not in distances):
                
#                 distances[next_position] = current_distance + 1
#                 if next_position == goal:
#                     return distances[next_position]
                
#                 queue.push(next_position)
    
#     return float('inf')  # Return infinity if no path is found



