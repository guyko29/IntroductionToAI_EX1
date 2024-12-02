from Assignment_1.grid_robot.heuristics import base_heuristic, advanced_heuristic
from grid_robot_state import grid_robot_state
from search import *


def test_case_1():
    global actual_h_values
    actual_h_values = []
    print("Initial actual_h_values:", actual_h_values)
    test_map = [
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, -1, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, -1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 3]
    ]
    start_state = grid_robot_state(
        robot_location=(7, 0),
        map=test_map,
        lamp_height=3,
        lamp_location=(0, 7),
        stairs_height=0,
        carrying=False
    )
    result = search(start_state, base_heuristic)

    expected = [14, 13, 12, 11, 10, 9, 8, 7, 7, 6, 5, 4, 3, 2, 2, 1, 0, 0]
    actual_h_values = []

    print("\nExpected heuristic values:", expected)
    print("Actual heuristic values:", actual_h_values)

    assert expected == actual_h_values, f"Heuristic values don't match!\nExpected: {expected}\nGot: {actual_h_values}"

if __name__ == "__main__":
   # actual_h_values = []
    test_case_1()
    #print("All tests passed!")
