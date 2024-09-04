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
    import heapq
    
    pacman_position, food_grid = current
    food_positions = food_grid # Get the list of food positions

    if not food_positions:
        return 0  # No food left to collect

   

    def compute_mst_cost(food_positions):
        if len(food_positions) == 1:
            return 0

        edges = {pos: [] for pos in food_positions}
        for i in range(len(food_positions)):
            for j in range(i + 1, len(food_positions)):
                f1 = food_positions[i]
                f2 = food_positions[j]
                distance = util.manhattanDistance(f1, f2)
                edges[f1].append((f2, distance))
                edges[f2].append((f1, distance))

        mst_cost = 0
        visited = set()
        min_heap = [(0, food_positions[0])]  # Start with an arbitrary node

        while min_heap:
            cost, node = heapq.heappop(min_heap)
            if node in visited:
                continue
            visited.add(node)
            mst_cost += cost

            for neighbor, edge_cost in edges[node]:
                if neighbor not in visited:
                    heapq.heappush(min_heap, (edge_cost, neighbor))

        return mst_cost

    mst_cost_value = compute_mst_cost(food_positions)
    min_distance_from_pacman = min(util.manhattanDistance(pacman_position, food) for food in food_positions)

    return mst_cost_value + min_distance_from_pacman