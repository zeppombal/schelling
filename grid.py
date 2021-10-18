import numpy as np

class Grid:

    def __init__(self):
        pass

    def loc_exists(self, neighbor_loc):
        """
        """
        exists = True
        for i in [0, 1]:
            # Check whether location in grid exists, or square is empty
            if neighbor_loc[i] > self.array.shape[i] or neighbor_loc[i] < 0 or self.array[neighbor_loc] == 0:
                exists = False
                break

        return exists

    def get_neighbors(self, location: np.array()) -> float:
        """
        """
        neighbors = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if not (x == 0 and y == 0):
                    neighbor_loc = location + np.array([x, y])
                    
                    if self.loc_exists(neighbor_loc):
                        neighbors.append(self.array[neighbor_loc])

        return neighbors
