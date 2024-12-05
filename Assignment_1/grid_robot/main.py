import time
from heuristics import *
from search import *

# if _name_ == 'main':
test_cases = [
    # {
    #     "name": "Example Map",
    #     "map": [
    #         [0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 0, 0, 4, 0, 0, 0, 0],
    #         [0, 0, 0, 0, -1, 0, 0, 0],
    #         [0, 0, 0, 0, -1, 0, 3, 0],
    #         [0, 0, 0, 0, -1, 0, 0, 0],
    #         [0, -1, -1, -1, -1, 0, 0, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0]
    #     ],
    #     "robot_start": (2, 1),
    #     "lamp_height": 7,
    #     "lamp_location": (4, 2)
    # },
    {
        "name": "Small Map",
        "map": [
            [0, 0, 0, 0],
            [1, 4, 2, -1],
            [0, -1, 0, -1]
        ],
        "robot_start": (0, 0),
        "lamp_height": 6,
        "lamp_location": (2, 2)
    },
    {
        "name": "Medium Map",
        "map": [
            [0, 0, -1, 0, 0],
            [0, 1, 0, 0, 0],
            [0, -1, -1, -1, 0],
            [2, 0, 0, 0, 0],
            [0, 0, 0, 0, 3]
        ],
        "robot_start": (0, 0),
        "lamp_height": 5,
        "lamp_location": (4, 4)
    },
    {
        "name": "Large Map",
        "map": [
            [0, 0, 0, -1, 0, 0, 0],
            [0, -1, 0, -1, 0, 1, 0],
            [0, -1, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, -1, 2, 0],
            [0, 3, 0, 0, 0, 0, 0],
            [0, -1, -1, 0, -1, 0, 4],
            [0, 0, 0, 0, 0, 0, 0]
        ],
        "robot_start": (0, 0),
        "lamp_height": 6,
        "lamp_location": (6, 6)
    },
    {
        "name": "Extra Large Map",
        "map": [
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, -1, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, 0, -1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 3]
        ],
        "robot_start": (7, 0),
        "lamp_height": 3,
        "lamp_location": (0, 7)
    }
]

for test in test_cases:
    print(f"Running test case: {test['name']}")
    start_state = grid_robot_state(
        map=test["map"],
        robot_location=test["robot_start"],
        lamp_height=test["lamp_height"],
        lamp_location=test["lamp_location"]
    )

    # Base heuristic
    start_time_base = time.time()
    search_result_base = search(start_state, base_heuristic)
    end_time_base = time.time() - start_time_base
    print("Base Heuristic:")
    print(f"Runtime: {end_time_base:.6f} seconds")
    print(f"Solution cost: {search_result_base[-1].g if search_result_base else 'No solution found'}\n")

    # Advanced heuristic
    start_time_advanced = time.time()
    search_result_advanced = search(start_state, advanced_heuristic)
    end_time_advanced = time.time() - start_time_advanced
    print("Advanced Heuristic:")
    print(f"Runtime: {end_time_advanced:.6f} seconds")
    print(f"Solution cost: {search_result_advanced[-1].g if search_result_advanced else 'No solution found'}\n")