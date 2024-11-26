
from heuristics import *
#from grid_robot_solved.search import *

if __name__ == '__main__':
    map = [
        [0, 0, 0, 0],
        [1, 4, 2, -1],
        [0, 0, 0, -1]
    ]
    robot_start_location = (1, 1)
    lamp_h = 6
    lamp_location = (2, 2)

    start_state = grid_robot_state(robot_start_location,map, lamp_h, lamp_location)
    neighbors = start_state.get_neighbors()
    for neighbor, cost in neighbors:
        print(f"Neighbor: {neighbor.robot_location}, Cost: {cost}")

    #search_result = search(start_state, base_heuristic)
