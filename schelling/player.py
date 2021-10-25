import numpy as np
from typing import *
from .utils import sample

class Player:

    def __init__(self,
                 group: str,
                 similar: float,
                 adaptivity: float,
                 resources: int
                 ):
        
        self.group = group
        self.similar = sample(similar)
        self.resources = resources
        self.adaptivity = adaptivity
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

        try:
            if same / (same + dif) >= self.similar:
                happy = True
        except ZeroDivisionError:
            happy = True

        self.similar = self.update_similar(dif, happy)

        return happy

    def update_similar(self, dif: int, happy: bool) -> float:
        """
        """
        new_sim = self.similar
        if dif == 0:
            new_sim = max(self.similar - self.adaptivity, 0)
        if happy:
            new_sim = min(self.similar + self.adaptivity, 1)

        return new_sim
