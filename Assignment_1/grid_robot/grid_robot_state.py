class grid_robot_state:
    def __init__(self, robot_location, map=None, lamp_height=-1, lamp_location=(-1, -1), stairs_height=0, carrying=False):
        self.robot_location = tuple(robot_location)
        self.map = map
        self.lamp_height = lamp_height
        self.lamp_location = tuple(lamp_location)
        self.stairs_height = stairs_height
        self.carrying = carrying  # Indicates whether the robot is carrying stairs

    @staticmethod
    def is_goal_state(state):
        # The robot is at the lamp location, and the stairs at the lamp location equal the lamp height.
        if state.robot_location != state.lamp_location:
            return False
        row, col = state.lamp_location
        return state.map[row][col] == state.lamp_height

    def get_neighbors(self):
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]
        current_row, current_col = self.robot_location

        # Move in four directions
        for row_step, col_step in directions:
            new_row = current_row + row_step
            new_col = current_col + col_step
            if 0 <= new_row < len(self.map) and 0 <= new_col < len(self.map[0]) and self.map[new_row][new_col] != -1:
                cost = 1 + (self.stairs_height if self.carrying else 0)
                neighbor = grid_robot_state(
                    robot_location=(new_row, new_col),
                    map=self.map,
                    lamp_height=self.lamp_height,
                    lamp_location=self.lamp_location,
                    stairs_height=self.stairs_height,
                    carrying=self.carrying
                )
                neighbors.append((neighbor, cost))

        # Pick up stairs
        if not self.carrying and self.map[current_row][current_col] > 0:
            neighbor = grid_robot_state(
                robot_location=self.robot_location,
                map=self.map,
                lamp_height=self.lamp_height,
                lamp_location=self.lamp_location,
                stairs_height=self.map[current_row][current_col],
                carrying=True
            )
            cost = 1  # Picking up stairs
            neighbors.append((neighbor, cost))

        # Place stairs
        if self.carrying and self.map[current_row][current_col] >= 0:
            new_map = [row[:] for row in self.map]
            new_map[current_row][current_col] += self.stairs_height
            neighbor = grid_robot_state(
                robot_location=self.robot_location,
                map=new_map,
                lamp_height=self.lamp_height,
                lamp_location=self.lamp_location,
                stairs_height=0,
                carrying=False
            )
            cost = 1  # Placing stairs
            neighbors.append((neighbor, cost))

        # Combine stairs
        if self.carrying and self.map[current_row][current_col] > 0:
            new_stairs_height = self.stairs_height + self.map[current_row][current_col]
            if new_stairs_height <= self.lamp_height:
                new_map = [row[:] for row in self.map]
                new_map[current_row][current_col] = 0  # Clear stairs after combining
                neighbor = grid_robot_state(
                    robot_location=self.robot_location,
                    map=new_map,
                    lamp_height=self.lamp_height,
                    lamp_location=self.lamp_location,
                    stairs_height=new_stairs_height,
                    carrying=True
                )
                cost = 1  # Combining stairs
                neighbors.append((neighbor, cost))

        return neighbors

    def get_state_str(self):
        carrying_str = "carrying" if self.carrying else "not_carrying"
        return f"{self.robot_location}_{self.lamp_location}_{carrying_str}"

    def __hash__(self):
        return hash((self.robot_location, self.lamp_location, self.carrying))

    def __eq__(self, other):
        if not isinstance(other, grid_robot_state):
            return False
        return (
            self.robot_location == other.robot_location
            and self.lamp_location == other.lamp_location
            and self.carrying == other.carrying
        )
