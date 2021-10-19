from .player import Player
from .grid import Grid
from typing import *
import numpy as np

# TO DO: cost para extensao dos resources

class Simulation:

    def __init__(self,
                 groups: Dict[str, float],
                 grid: Grid,
                 shape: Tuple[int],
                 empty: float,
                 player_kw: Dict[Any, Any],
                 seed=None):

        self.groups = groups
        self.grid = Grid(shape)
        self.shape = shape
        self.empty = empty
        self.player_kw = player_kw
        self.seed = seed
    
    def generate_players(self) -> None:
        """
        """
        n_squares = self.shape[0] * self.shape[1]
        players = []
        for g, f in self.groups.items():
            n = int(f * n_squares)

            if g == "empty":
                new_players = [0 for _ in range(n)]
            else:
                new_players = [Player(group=g, **self.player_kw) for _ in range(n)]

            players.extend(new_players)

        for i in range(n_squares - len(players)):
            players.append(0)

        rng = np.random.default_rng(self.seed)
        shuffled_players = rng.permutation(players)

        self.grid.array = np.reshape(shuffled_players, self.shape)


    def repopulate(self) -> None:
        # TO DO: ACCOUNT FOR RESOURCES
        rng = np.random.default_rng()
        shuffled_p = rng.permutation(len(self.unhappy_p) - 1)

        for i in shuffled_p:
            # Shuffle empty locs for no bias
            self.empty_locs = rng.permutation(self.empty_locs).tolist()
            new_i = self.empty_locs.pop(0)

            # Put player in an empty loc
            self.grid.array[new_i] = self.unhappy_p[i]
            # Put loc where player was in empty locs
            self.empty_locs.append(self.unhappy_locs[i])
            # Empty where the player was
            self.grid.array[self.unhappy_locs[i]] = 0


    def run_simulation(self):
        """
        """
        # Generate players in grid
        self.generate_players()
        # CHANGE TO WHILE LOOP
        for _ in range(100):
            self.empty_locs = []
            self.unhappy_locs = []
            self.unhappy_p = []

            # Iterate over grid squares
            for loc, p in np.ndenumerate(self.grid.array):
                # If square not empty, calculate player happiness
                if p != 0:
                    p.location = loc

                    neighbors = self.grid.get_neighbors(p.location)
                    is_happy = p.calc_happy(neighbors)

                    self.unhappy_locs.append(loc)
                    self.unhappy_p.append(p)

                # If square empty, store its location for repopulate
                else:
                    self.empty_locs.append(loc)

            ### DEBUG PRINT
            elements = []
            for j in self.grid.array:
                for i in j:
                    if i != 0:
                        g = i.group
                    else:
                        g = i
                    elements.append(g)
            display = np.array(elements).reshape(self.shape)
            print(display)
            self.repopulate()

            



            