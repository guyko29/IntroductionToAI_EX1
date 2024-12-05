from grid_robot_state import grid_robot_state


def base_heuristic(_grid_robot_state):
    actual_h_values = []
    h_value = abs(_grid_robot_state.robot_location[0] - _grid_robot_state.lamp_location[0]) + \
              abs(_grid_robot_state.robot_location[1] - _grid_robot_state.lamp_location[1])
    actual_h_values.append(h_value)
    return h_value


def advanced_heuristic(_grid_robot_state):
    robot_row, robot_col = _grid_robot_state.robot_location
    lamp_row, lamp_col = _grid_robot_state.lamp_location
    lamp_height = _grid_robot_state.lamp_height
    stairs_height = _grid_robot_state.stairs_height
    actual_h_values = lamp_height - stairs_height
    manhattan_dis = (abs(robot_row - lamp_row) + abs(robot_col - lamp_col))
    if actual_h_values != 0:
        return manhattan_dis * ((actual_h_values + lamp_height) / actual_h_values)
    return manhattan_dis * lamp_height
