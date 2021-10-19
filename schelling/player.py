import numpy as np
from typing import *

class Player:

    def __init__(self,
                 group: str,
                 similar: float,
                 resources: int
                 ):
        
        self.group = group
        self.similar = similar
        self.resources = resources
        self.location = np.array([0, 0])

    def calc_happy(self, neighbors: List[Any]) -> float:
        """
        """
        happy = False
        same = 0
        dif = 0
        for n in neighbors:
            if n.group == self.group:
                same += 1
            else:
                dif += 1

        if same / (same + dif) < self.similar:
            happy = True

        return happy

    def update_similar(grid: np.array) -> float:
        """
        """
        pass


