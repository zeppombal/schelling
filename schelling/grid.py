import numpy as np
from typing import *

class Grid:

    def __init__(self, shape: Tuple[int] = (50, 50)):
        
        self.array = np.zeros(shape)

    def loc_exists(self, neighbor_loc):
        """
        """
        exists = True
        for i in [0, 1]:
            try:
                if self.array[neighbor_loc[0], neighbor_loc[1]] == 0 or neighbor_loc[i] >= self.array.shape[i] or neighbor_loc[i] < 0:
                    exists = False
                    break
            except IndexError:
                exists = False
                break

        return exists

    def get_neighbors(self, location: np.array) -> List[Any]:
        """
        Returns list of player neighbors for a given location
        """
        location = np.array(location)
        neighbors = []
        for x in [-2, -1, 0, 1, 2]:
            for y in [-2, -1, 0, 1, 2]:
                if not (x == 0 and y == 0):
                    neighbor_loc = location + np.array([x, y])
                    
                    if self.loc_exists(neighbor_loc):
                        neighbors.append(self.array[neighbor_loc[0], neighbor_loc[1]])

        return neighbors
