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
    closed_set[vn.state] = vn.g



def duplicate_in_open(vn, open_set):
    """
    Checks if a node with the same state exists in the open set with an equal or lower g-value.
    """
    # Iterate over the open set and check for duplicates
    for f_value, node in open_set:
        if node.state == vn.state:
            if vn.g >= node.g:
                return True
    return False

def duplicate_in_closed(vn, closed_set):
    """
    Checks if a node with the same state exists in the closed set with a lower or equal g-value.
    """
    if vn.state in closed_set and vn.g >= closed_set[vn.state]:
        return True
    return False


# helps to debug sometimes..
def print_path(path):
    for i in range(len(path)-1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.state_str)
import logging

# הגדרת לוגינג לכתיבה בקובץ
logging.basicConfig(filename="search_output.log", level=logging.INFO, format='%(message)s')

def log_print(message):
    """פונקציה להדפסת הודעה גם לקונסול וגם לקובץ"""
    print(message)  # מדפיס לקונסול
    logging.info(message)  # כותב לקובץ

def search(start_state, heuristic):
    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, g=0, h=heuristic(start_state))
    add_to_open(start_node, open_set)
    counter = 0
    MAX_ITERATIONS = 10000  # מגבלת מספר איטרציות

    while open_not_empty(open_set):
        counter += 1

        # הדפסת מספר האיטרציות וגדלי הקבוצות
        log_print(f"Iteration {counter}: Open set size = {len(open_set)}, Closed set size = {len(closed_set)}")

        # עצירה אם כמות האיטרציות עברה את המקסימום
        if counter > MAX_ITERATIONS:
            log_print("Maximum iterations reached. Exiting...")
            return None

        # שליפת המצב הטוב ביותר
        current = get_best(open_set)
        log_print(f"Current state: Robot location = {current.state.robot_location}, "
                  f"Stairs height = {current.state.stairs_height}, "
                  f"Carrying = {current.state.carrying}, "
                  f"g = {current.g}, h = {current.h}, f = {current.f}")

        # בדיקה אם הגענו למצב המטרה
        if grid_robot_state.is_goal_state(current.state):
            log_print(f"Goal state reached: Robot location = {current.state.robot_location}, "
                      f"Stairs height = {current.state.stairs_height}")
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        # הוספת המצב הנוכחי ל-closed_set
        add_to_closed(current, closed_set)
        log_print(f"Adding to closed_set: Robot location = {current.state.robot_location}, "
                  f"Stairs height = {current.state.stairs_height}")

        # יצירת שכנים
        for neighbor, edge_cost in current.get_neighbors():
            log_print(f"Neighbor: Robot location = {neighbor.robot_location}, "
                      f"Stairs height = {neighbor.stairs_height}, "
                      f"Carrying = {neighbor.carrying}, "
                      f"Edge Cost = {edge_cost}")

            # יצירת search_node עבור שכן
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)

            # סינון שכנים שנמצאים כבר ב-open_set או ב-closed_set
            if duplicate_in_open(curr_neighbor, open_set):
                log_print(f"Skipping neighbor already in open_set: {neighbor.robot_location}")
            elif duplicate_in_closed(curr_neighbor, closed_set):
                log_print(f"Skipping neighbor already in closed_set: {neighbor.robot_location}")
            else:
                add_to_open(curr_neighbor, open_set)
                log_print(f"Added to open_set: Robot location = {neighbor.robot_location}, "
                          f"Stairs height = {neighbor.stairs_height}, "
                          f"Carrying = {neighbor.carrying}")

    log_print("No solution found.")
    return None


"""
def search(start_state, heuristic):
    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, g=0, h=heuristic(start_state))
    add_to_open(start_node, open_set)
    counter = 0
    MAX_ITERATIONS = 10000

    while open_not_empty(open_set):
        counter += 1
        print(f"Iteration {counter}: Open set size = {len(open_set)}, Closed set size = {len(closed_set)}")

        if counter > MAX_ITERATIONS:
            print("Maximum iterations reached. Exiting...")
            return None

        current = get_best(open_set)
        print(f"Current state: {current.state.get_state_str()}, g = {current.g}, h = {current.h}, f = {current.f}")

        if grid_robot_state.is_goal_state(current.state):
            print(f"Goal state reached: {current.state.get_state_str()}")
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)
        print(f"Adding to closed_set: {current.state.get_state_str()}")

        for neighbor, edge_cost in current.get_neighbors():
            print(f"Neighbor: {neighbor.get_state_str()}, Edge Cost: {edge_cost}")
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)

            if duplicate_in_open(curr_neighbor, open_set):
                print(f"Skipping neighbor already in open_set: {neighbor.get_state_str()}")
            elif duplicate_in_closed(curr_neighbor, closed_set):
                print(f"Skipping neighbor already in closed_set: {neighbor.get_state_str()}")
            else:
                add_to_open(curr_neighbor, open_set)

    print("No solution found.")
    return None
"""




