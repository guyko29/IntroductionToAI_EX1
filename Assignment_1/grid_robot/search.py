from itertools import count
import logging


from search_node import search_node
from grid_robot_state import grid_robot_state
import heapq


def create_open_set():
    return []


def create_closed_set():
    return {}


def add_to_open(vn, open_set):
    heapq.heappush(open_set, (vn.f, vn))


def open_not_empty(open_set):
    return len(open_set) > 0


def get_best(open_set):
    return heapq.heappop(open_set)[1]


def add_to_closed(vn, closed_set):
   key = (vn.state.robot_location, vn.state.carrying, vn.state.stairs_height)
   closed_set[key] = vn.g



def duplicate_in_closed(vn, closed_set):
    key = (vn.state.robot_location, vn.state.carrying, vn.state.stairs_height)
    return key in closed_set and vn.g >= closed_set[key]

def duplicate_in_open(vn, open_set):
    for _, node in open_set:
        if (node.state.robot_location == vn.state.robot_location and
            node.state.carrying == vn.state.carrying and
            node.state.stairs_height == vn.state.stairs_height and
            vn.g >= node.g):
            return True
    return False

# helps to debug sometimes..
def print_path(path):
    for i in range(len(path)-1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.state_str)
import logging

def log_print(message):
    """פונקציה להדפסת הודעה גם לקונסול וגם לקובץ"""
    print(message)  # מדפיס לקונסול
    logging.info(message)  # כותב לקובץ

### Given function, dont change
def search(start_state, heuristic):

    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)

        if grid_robot_state.is_goal_state(current.state):
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)

        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_open(curr_neighbor, open_set) and not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set)

    return None








