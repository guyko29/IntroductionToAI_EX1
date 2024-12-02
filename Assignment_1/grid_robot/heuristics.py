from grid_robot_state import grid_robot_state

actual_h_values = []
def base_heuristic(_grid_robot_state):
    global actual_h_values
    h_value = abs(_grid_robot_state.robot_location[0] - _grid_robot_state.lamp_location[0]) + \
              abs(_grid_robot_state.robot_location[1] - _grid_robot_state.lamp_location[1])
    print("Adding h_value:", h_value)  # Debug
    actual_h_values.append(h_value)
    print("Current actual_h_values:", actual_h_values)  # Debug
    return h_value


def advanced_heuristic(_grid_robot_state):
   robot_row, robot_col = _grid_robot_state.robot_location
   lamp_row, lamp_col = _grid_robot_state.lamp_location

   # Calculate Manhattan distance to lamp
   manhattan_distance = abs(robot_row - lamp_row) + abs(robot_col - lamp_col)

   # Calculate remaining stairs needed
   current_height = _grid_robot_state.stairs_height if _grid_robot_state.carrying else 0
   cell_height = _grid_robot_state.map[lamp_row][lamp_col] if _grid_robot_state.map[lamp_row][lamp_col] > 0 else 0
   total_height = current_height + cell_height
   stairs_needed = _grid_robot_state.lamp_height - total_height

   # Add penalties based on stairs needed and distance
   if stairs_needed > 0:
       return manhattan_distance + stairs_needed * 2  # Higher penalty for missing stairs
   return manhattan_distance