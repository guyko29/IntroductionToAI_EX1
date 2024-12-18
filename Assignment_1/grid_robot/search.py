from search_node import search_node
from grid_robot_state import grid_robot_state
import heapq


def create_open_set():
    return {}, []


def create_closed_set():
    return {}


def add_to_open(vn, open_set):
    heapq.heappush(open_set[1], (vn.f, vn))
    key = vn.state
    value = vn.g
    open_set[0][key] = value


def open_not_empty(open_set):
    return len(open_set[1]) > 0


def get_best(open_set):
    while open_set[1]:
        out_state = heapq.heappop(open_set[1])[1]
        if out_state.state in open_set[0]:
            del open_set[0][out_state.state]
            return out_state
    return None


def add_to_closed(vn, closed_set):
   key = vn.state
   closed_set[key] = vn


def duplicate_in_closed(vn, closed_set):
    if vn.state in closed_set:
        if vn.g <= closed_set[vn.state].g:
            del closed_set[vn.state]
            return False
        return True
    return False


def duplicate_in_open(vn, open_set):
    if vn.state in open_set[0]:
        if vn.g <= open_set[0][vn.state]:
            del open_set[0][vn.state]
            return False
        return True
    return False


# helps to debug sometimes..
def print_path(path):
    for i in range(len(path)-1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.get_state_str)


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






