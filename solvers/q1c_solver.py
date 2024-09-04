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
    astarData.cost_so_far[start_state] = initial_cost  # No longer unhashable
    astarData.came_from[start_state] = None
    
    return astarData

def astar_loop_body(problem: q1c_problem, astarData: AStarData):
    # YOUR CODE HERE
    
    if astarData.pqueue.isEmpty():
        return True, None  # No solution if priority queue is empty
    
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
            
            astarData.pqueue.push(successor, (priority, new_cost))
            astarData.came_from[successor] = current, action
    
    return False, None

def astar_heuristic(current, goals):
    # YOUR CODE HERE
    # pacman_position, _ = current  
    # return min(util.manhattanDistance(pacman_position, goal) for goal in goals)
    
    pacman_position, remaining_food = current

    if not remaining_food:
        return 0

    # Calculate all pairwise distances
    distances = {}
    for i in range(len(remaining_food)):
        for j in range(i + 1, len(remaining_food)):
            food1 = remaining_food[i]
            food2 = remaining_food[j]
            dist = util.manhattanDistance(food1, food2)
            if food1 not in distances:
                distances[food1] = []
            if food2 not in distances:
                distances[food2] = []
            distances[food1].append((food2, dist))
            distances[food2].append((food1, dist))

    # Helper function to calculate the MST cost using a list-based approach
    def mst_cost(nodes, edges):
        if len(nodes) == 1:
            return 0
        mst_cost = 0
        in_mst = {node: False for node in nodes}
        min_edges = [(0, nodes[0])]  # Start with an arbitrary node
        while min_edges:
            cost, node = min_edges.pop(0)
            if in_mst[node]:
                continue
            in_mst[node] = True
            mst_cost += cost
            for neighbor, edge_cost in edges[node]:
                if not in_mst[neighbor]:
                    min_edges.append((edge_cost, neighbor))
                    min_edges.sort()  # Sort edges to get the minimum cost edge next
        return mst_cost

    # Get the list of food nodes
    food_nodes = list(remaining_food)
    
    # Calculate MST cost
    mst_cost_value = mst_cost(food_nodes, distances)

    # Add the cost of reaching the nearest food dot
    min_distance_to_food = min(util.manhattanDistance(pacman_position, food) for food in remaining_food)

    return mst_cost_value + min_distance_to_food