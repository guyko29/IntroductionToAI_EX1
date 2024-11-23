class grid_robot_state:
    # you can add global params

    def __init__(self, robot_location, map=None, lamp_height=-1, lamp_location=(-1, -1)):
        # you can use the init function for several purposes
        self.robot_location = tuple(robot_location)
        self.map = map
        self.lamp_height = lamp_height
        self.lamp_location = lamp_location

    @staticmethod
    def is_goal_state(_grid_robot_state):
        if _grid_robot_state.lamp_location == _grid_robot_state.robot_location:
            return True
        return False

    def get_neighbors(self):
        neighbors = []
        down = (1,0)
        up = (-1,0)
        left = (0,-1)
        right = (0,1)
        directions = [down, up, left, right]
        current_row , current_col = self.robot_location

        #Generate the new neighbors if possible
        for row_delta, col_delta in directions:
            new_row = current_row + row_delta
            new_col = current_col + col_delta

            if 0 <= new_row < len(self.map) and 0 <= new_col < len(self.map[0]):
                if self.map[new_row][new_col] != -1:
                    new_state = grid_robot_state(
                        robot_location=(new_row, new_col),
                        map=self.map,
                        lamp_height=self.lamp_height,
                        lamp_location=self.lamp_location
                    )
                    cost = 1
                    neighbors.append((new_state, cost))

        return neighbors

        # you can change the body of the function if you want
        # def __hash__(self):

        # you can change the body of the function if you want
        # def __eq__(self, other):
        # you can change the body of the function if you want

    def get_state_str(self):
        pass


    def get_lamp_location(self):
        return self.lamp_location
    #you can add helper functions