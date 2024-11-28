from grid_robot_state import grid_robot_state

def base_heuristic(_grid_robot_state):
    robot_row, robot_col = _grid_robot_state.robot_location
    lamp_row, lamp_col = _grid_robot_state.lamp_location
    return abs(robot_row - lamp_row) + abs(robot_col - lamp_col)


def advanced_heuristic(_grid_robot_state):
    robot_row, robot_col = _grid_robot_state.robot_location
    lamp_row, lamp_col = _grid_robot_state.lamp_location
    manhattan_distance = abs(robot_row - lamp_row) + abs(robot_col - lamp_col)
    if _grid_robot_state.carrying:
        return manhattan_distance + _grid_robot_state.stairs_height
    else:
        return manhattan_distance + (_grid_robot_state.lamp_height - _grid_robot_state.stairs_height)
