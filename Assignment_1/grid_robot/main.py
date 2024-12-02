from Assignment_1.grid_robot.heuristics import base_heuristic, advanced_heuristic
from grid_robot_state import grid_robot_state
from search import *

def test_neighbors():
    print("Running test_neighbors...")
    test_state = grid_robot_state(
        robot_location=(1, 1),
        map=[
            [0, 0, 0, 0],
            [1, 4, 2, -1],
            [0, 0, 0, -1]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    neighbors = test_state.get_neighbors()
    print("Generated neighbors:")
    for neighbor, cost in neighbors:
        print(f"Neighbor: {neighbor.robot_location}, Cost: {cost}, Carrying: {neighbor.carrying}, Stairs Height: {neighbor.stairs_height}")

    # בדיקות:
    assert len(neighbors) > 0, "No neighbors were generated!"
    assert all(0 <= n.robot_location[0] < len(test_state.map) and 0 <= n.robot_location[1] < len(test_state.map[0]) for n, _ in neighbors), "Invalid neighbor position!"
    print("test_neighbors passed.\n")


def test_pick_up_stairs():
    print("Running test_pick_up_stairs...")
    test_state = grid_robot_state(
        robot_location=(1, 1),
        map=[
            [0, 0, 0, 0],
            [0, 4, 0, -1],
            [0, 0, 0, -1]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    neighbors = test_state.get_neighbors()
    picked_up = any(n.carrying and n.stairs_height == 4 for n, _ in neighbors)
    assert picked_up, "Robot failed to pick up stairs!"
    print("test_pick_up_stairs passed.\n")


def test_place_stairs():
    print("Running test_place_stairs...")
    test_state = grid_robot_state(
        robot_location=(1, 1),
        map=[
            [0, 0, 0, 0],
            [0, 0, 0, -1],
            [0, 0, 0, -1]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=3,
        carrying=True
    )
    neighbors = test_state.get_neighbors()
    placed = any(n.map[1][1] == 3 and not n.carrying for n, _ in neighbors)
    assert placed, "Robot failed to place stairs!"
    print("test_place_stairs passed.\n")


def test_combine_stairs():
    print("Running test_combine_stairs...")
    test_state = grid_robot_state(
        robot_location=(1, 1),
        map=[
            [0, 0, 0, 0],
            [0, 4, 0, -1],
            [0, 0, 0, -1]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=2,
        carrying=True
    )
    neighbors = test_state.get_neighbors()
    combined = any(n.carrying and n.stairs_height == 6 for n, _ in neighbors)
    assert combined, "Robot failed to combine stairs!"
    print("test_combine_stairs passed.\n")


def test_blocked_map():
    print("Running test_blocked_map...")
    test_state = grid_robot_state(
        robot_location=(1, 1),
        map=[
            [-1, -1, -1],
            [-1, 0, -1],
            [-1, -1, -1]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    neighbors = test_state.get_neighbors()
    assert len(neighbors) == 0, "Robot found neighbors in a blocked map!"
    print("test_blocked_map passed.\n")


def test_no_stairs_to_pick_up():
    print("Running test_no_stairs_to_pick_up...")
    test_state = grid_robot_state(
        robot_location=(1, 1),
        map=[
            [0, 0, 0, 0],
            [0, 0, 0, -1],
            [0, 0, 0, -1]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    neighbors = test_state.get_neighbors()
    assert not any(n.carrying for n, _ in neighbors), "Robot picked up stairs when there were none!"
    print("test_no_stairs_to_pick_up passed.\n")


def test_cannot_pick_up_when_carrying():
    print("Running test_cannot_pick_up_when_carrying...")
    test_state = grid_robot_state(
        robot_location=(1, 1),
        map=[
            [0, 0, 0, 0],
            [1, 4, 2, -1],
            [0, 0, 0, -1]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=3,
        carrying=True
    )
    neighbors = test_state.get_neighbors()
    assert not any(n.carrying and n.stairs_height > 3 for n, _ in neighbors), "Robot picked up stairs while already carrying!"
    print("test_cannot_pick_up_when_carrying passed.\n")

def test_base_heuristic():
    print("Running test_base_heuristic...")
    test_state = grid_robot_state(
        robot_location=(0, 0),
        map=[
            [0, -1, 0],
            [4, 0, -1],
            [-1, 2, 0]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    heuristic_value = base_heuristic(test_state)
    expected_value = abs(0 - 2) + abs(0 - 2)  # מרחק מנהטן
    print(f"Base heuristic value: {heuristic_value}, Expected: {expected_value}")
    assert heuristic_value == expected_value, "Base heuristic value is incorrect!"
    print("test_base_heuristic passed.\n")


def test_advanced_heuristic():
    print("Running test_advanced_heuristic...")
    test_state = grid_robot_state(
        robot_location=(0, 0),
        map=[
            [0, -1, 0],
            [4, 0, -1],
            [-1, 2, 0]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=3,
        carrying=True
    )
    heuristic_value = advanced_heuristic(test_state)
    expected_value = abs(0 - 2) + abs(0 - 2) + 3  # מרחק מנהטן + גובה מדרגות שהרובוט נושא
    print(f"Advanced heuristic value: {heuristic_value}, Expected: {expected_value}")
    assert heuristic_value == expected_value, "Advanced heuristic value is incorrect!"
    print("test_advanced_heuristic passed.\n")


def test_heuristic_comparison():
    print("Running test_heuristic_comparison...")
    test_state = grid_robot_state(
        robot_location=(0, 0),
        map=[
            [0, -1, 0],
            [4, 0, -1],
            [-1, 2, 0]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )

    base_value = base_heuristic(test_state)
    advanced_value = advanced_heuristic(test_state)
    print(f"Base heuristic: {base_value}, Advanced heuristic: {advanced_value}")
    assert advanced_value >= base_value, "Advanced heuristic should not be worse than base heuristic!"
    print("test_heuristic_comparison passed.\n")


def test_stairs_combination():
    print("Running test_stairs_combination...")
    # יצירת מצב התחלה עם מדרגות בגבהים שונים
    test_state = grid_robot_state(
        robot_location=(1, 1),  # מיקום הרובוט
        map=[
            [0, 0, 0],  # שורה עליונה
            [0, 2, 2],  # שורה אמצעית (שינוי: מדרגות בגובה 2 במקום 4)
            [0, 0, 0]  # שורה תחתונה
        ],
        lamp_height=6,  # גובה הנורה
        lamp_location=(2, 2),  # מיקום הנורה
        stairs_height=4,  # גובה המדרגות שהרובוט נושא
        carrying=True  # הרובוט נושא מדרגות
    )

    # קבלת השכנים שנוצרים
    neighbors = test_state.get_neighbors()

    # הדפסת כל שכן שנוצר
    for neighbor, cost in neighbors:
        print(f"Neighbor generated: Location = {neighbor.robot_location}, "
              f"Carrying = {neighbor.carrying}, "
              f"Stairs Height = {neighbor.stairs_height}, "
              f"Cost = {cost}")

    # בדיקה אם יש שכן שבו גובה המדרגות המשולב שווה ל-6
    combined = any(n.carrying and n.stairs_height == 6 for n, _ in neighbors)
    if not combined:
        print("No valid neighbors found with stairs height 6.")
    assert combined, "Robot failed to combine stairs correctly!"
    print("test_stairs_combination passed.\n")

def test_hash_function():
    # Test 1: Hash for identical states
    state1 = grid_robot_state(
        robot_location=(0, 0),
        map=[[0, -1, 0], [4, 0, -1], [-1, 2, 0]],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    state2 = grid_robot_state(
        robot_location=(0, 0),
        map=[[0, -1, 0], [4, 0, -1], [-1, 2, 0]],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    assert hash(state1) == hash(state2), "Test 1 failed: Hash values for identical states do not match!"
    print("Test 1 passed: Hash values for identical states match.")

    # Test 2: Hash for different states
    state3 = grid_robot_state(
        robot_location=(0, 1),
        map=[[0, -1, 0], [4, 0, -1], [-1, 2, 0]],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    assert hash(state1) != hash(state3), "Test 2 failed: Hash values for different states match!"
    print("Test 2 passed: Hash values for different states are unique.")

    # Test 3: Uniqueness with a set
    state4 = grid_robot_state(
        robot_location=(0, 0),
        map=[[0, -1, 0], [4, 0, -1], [-1, 2, 0]],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    state_set = {state1, state3, state4}
    assert len(state_set) == 2, "Test 3 failed: Set contains duplicate states!"
    print("Test 3 passed: Set correctly identifies unique states.")

    # Test 4: Consistency of hash values
    hash1 = hash(state1)
    hash2 = hash(state1)
    assert hash1 == hash2, "Test 4 failed: Hash values are inconsistent!"
    print("Test 4 passed: Hash values are consistent.")

    # Test 5: Hash function with large maps
    large_map = [[0 for _ in range(10)] for _ in range(10)]
    state5 = grid_robot_state(
        robot_location=(5, 5),
        map=large_map,
        lamp_height=6,
        lamp_location=(9, 9),
        stairs_height=0,
        carrying=False
    )
    try:
        hash_value = hash(state5)
        print(f"Test 5 passed: Hash value for large map is {hash_value}.")
    except Exception as e:
        print(f"Test 5 failed: {e}")

    # Test 6: Hash function with minimal map
    minimal_map = [[0]]
    state6 = grid_robot_state(
        robot_location=(0, 0),
        map=minimal_map,
        lamp_height=0,
        lamp_location=(0, 0),
        stairs_height=0,
        carrying=False
    )
    try:
        hash_value = hash(state6)
        print(f"Test 6 passed: Hash value for minimal map is {hash_value}.")
    except Exception as e:
        print(f"Test 6 failed: {e}")


def run_advanced_tests():
    print("Running advanced tests...")

    # Test 1: Complex Goal State
    print("Test 1: Complex Goal State")
    test_state = grid_robot_state(
        robot_location=(2, 2),
        map=[
            [0, -1, 0],
            [4, 0, -1],
            [-1, 2, 6]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    assert grid_robot_state.is_goal_state(test_state), "Failed to identify a complex goal state!"
    print("Test 1 passed.\n")

    # Test 2: Empty Map
    print("Test 2: Empty Map")
    test_state = grid_robot_state(
        robot_location=(0, 0),
        map=[
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ],
        lamp_height=0,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    neighbors = test_state.get_neighbors()
    assert len(neighbors) > 0, "No neighbors generated on an empty map!"
    print("Test 2 passed.\n")

    # Test 3: Obstacle Navigation
    print("Test 3: Obstacle Navigation")
    test_state = grid_robot_state(
        robot_location=(0, 0),
        map=[
            [0, -1, 0],
            [0, -1, 0],
            [0, 0, 0]
        ],
        lamp_height=0,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    neighbors = test_state.get_neighbors()
    assert all(test_state.map[n.robot_location[0]][n.robot_location[1]] != -1 for n, _ in neighbors), "Robot moved into a blocked cell!"
    print("Test 3 passed.\n")

    # Test 4: Stairs Combination
    print("Test 4: Stairs Combination")
    test_state = grid_robot_state(
        robot_location=(1, 1),
        map=[
            [0, 0, 0],
            [0, 2, 2],  # שינוי המפה כך שגובה המדרגות בתא הנוכחי הוא 2
            [0, 0, 0]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=4,
        carrying=True
    )
    neighbors = test_state.get_neighbors()
    for neighbor, cost in neighbors:
        print(f"Neighbor generated: Location = {neighbor.robot_location}, "
              f"Carrying = {neighbor.carrying}, "
              f"Stairs Height = {neighbor.stairs_height}, "
              f"Cost = {cost}")
    combined = any(n.carrying and n.stairs_height == 6 for n, _ in neighbors)
    assert combined, "Robot failed to combine stairs correctly!"
    print("Test 4 passed.\n")

    # Test 5: Complex Search
    print("Test 5: Complex Search")
    test_state = grid_robot_state(
        robot_location=(0, 0),
        map=[
            [0, -1, 0],
            [4, 0, -1],
            [-1, 2, 0]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    result = search(test_state, base_heuristic)
    assert result is not None, "Search failed to find a solution!"
    assert grid_robot_state.is_goal_state(result[-1].state), "Search did not reach the goal state!"
    print("Test 5 passed. Search path:")
    for step in result:
        print(step.state.get_state_str())
    print()

    # Test 6: Failed Search
    print("Test 6: Failed Search")
    test_state = grid_robot_state(
        robot_location=(0, 0),
        map=[
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1]
        ],
        lamp_height=6,
        lamp_location=(2, 2),
        stairs_height=0,
        carrying=False
    )
    result = search(test_state, advanced_heuristic)
    assert result is None, "Search should fail in a completely blocked map!"
    print("Test 6 passed.\n")


def calculate_expected_heuristic(lamp_location, map_size):
    expected = []
    lamp_x, lamp_y = lamp_location
    for x in range(map_size[0]):  # איטרציה על שורות
        for y in range(map_size[1]):  # איטרציה על עמודות
            expected.append(abs(x - lamp_x) + abs(y - lamp_y))
    return expected

def test_heuristic():
    # הגדרת מצב לבדיקה
    test_state = grid_robot_state(
        robot_location=(7, 0),
        map=[
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, -1, 0, 0, 0, 0],
            [0, 0, 2, 0, 0, -1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 3]
        ],
        lamp_height=3,
        lamp_location=(0, 7),
        stairs_height=0,
        carrying=False
    )

    # ערכי היוריסטיקה הצפויים (לפי המערכת של האוניברסיטה)
    expected_heuristic = [
        14, 13, 12, 11, 10, 9, 8, 7,  # שורה ראשונה
        7, 6, 5, 4, 3, 2, 2, 1,       # שורה שנייה
        0, 0                          # שאר הערכים הצפויים
    ]

    # חישוב היוריסטיקה בפועל
    actual_heuristic = []
    for x in range(len(test_state.map)):  # איטרציה על שורות
        for y in range(len(test_state.map[0])):  # איטרציה על עמודות
            test_neighbor_state = grid_robot_state(
                robot_location=(x, y),
                map=test_state.map,
                lamp_height=test_state.lamp_height,
                lamp_location=test_state.lamp_location,
                stairs_height=test_state.stairs_height,
                carrying=test_state.carrying
            )
            heuristic_value = base_heuristic(test_neighbor_state)
            actual_heuristic.append(heuristic_value)

    # השוואת התוצאה
    for index, (expected, actual) in enumerate(zip(expected_heuristic, actual_heuristic)):
        if expected != actual:
            print(f"Mismatch at index {index}: Expected = {expected}, Actual = {actual}")

    assert actual_heuristic == expected_heuristic, (
        f"Expected Heuristic: {expected_heuristic}, but got: {actual_heuristic}."
    )
    print("Heuristic test passed!")





if __name__ == "__main__":
    test_neighbors()
    test_pick_up_stairs()
    test_place_stairs()
    test_combine_stairs()
    test_blocked_map()
    test_no_stairs_to_pick_up()
    test_cannot_pick_up_when_carrying()
    test_base_heuristic()
    test_advanced_heuristic()
    test_heuristic_comparison()
    run_advanced_tests()
    test_stairs_combination()
    test_hash_function()
    test_heuristic()
    print("All tests passed!")
