from .player import Player
from .grid import Grid
from .utils import *

from typing import *
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BASE_COLORS

# TO DO: cost para extensao dos resources

class Simulation:

    def __init__(self,
                 groups: Dict[str, float],
                 shape: List[int],
                 empty: float,
                 is_costs: bool,
                 similar_list: List[float],
                 resources_list: List[int],
                 adaptivities_list: List[float],
                 seed=None,
                 animate=True):

        self.groups = groups
        self.grid = Grid(shape)
        self.shape = tuple(shape)
        self.empty = empty
        self.is_costs = is_costs

        assert len(groups) == len(similar_list) == len(resources_list) == len(adaptivities_list), "Length of groups and params lists are not equal."
        self.player_kw = generate_kwargs(groups, similar_list, resources_list, adaptivities_list)
        
        self.seed = seed
        self.animate = animate
        self.frames = []

    def generate_players(self) -> None:
        """
        """
        assert round((sum(self.groups.values()) + self.empty), 5) == 1, "Group percentages and empty do not sum to 1."

        n_squares = self.shape[0] * self.shape[1]
        players = []
        for g, f in self.groups.items():
            n = int(f * n_squares)

            if g == "empty":
                new_players = [0 for _ in range(n)]
            else:
                p_kw = handle_kwargs(g, self.player_kw)
                new_players = [Player(group=g, **p_kw) for _ in range(n)]

            players.extend(new_players)

        for i in range(n_squares - len(players)):
            players.append(0)

        rng = np.random.default_rng(self.seed)
        shuffled_players = rng.permutation(players)

        self.grid.array = np.reshape(shuffled_players, self.shape)

    def filter_locs(self, player):
        """
        """
        out_locs = []
        for l in self.empty_locs:
            l1 = abs(l[0] - player.location[0])
            l2 = abs(l[1] - player.location[1])
            # Cost of moving. Not parameterizable
            cost = 1 + 3 * np.log(max(l1, l2))

            if player.resources >= cost:
                out_locs.append(l)
        
        return out_locs

    def repopulate(self) -> None:
        # TO DO: ACCOUNT FOR RESOURCES
        rng = np.random.default_rng()
        shuffled_p = rng.permutation(range(len(self.unhappy_p)))

        for i in shuffled_p:
            # Shuffle empty locs for no bias
            self.empty_locs = rng.permutation(self.empty_locs).tolist()

            # determine which locations are accessible to player, given resources
            if self.is_costs:
                filtered_locs = self.filter_locs(self.unhappy_p[i])
                loc = filtered_locs.pop(0)
            else:
                loc = self.empty_locs[0]
                
            # take loc from empty locs
            new_i = tuple(self.empty_locs.pop(self.empty_locs.index(loc)))
            # Put player in an empty loc
            self.grid.array[new_i] = deepcopy(self.unhappy_p[i])
            # Put loc where player was in empty locs
            self.empty_locs.append(deepcopy(self.unhappy_locs[i]))
            # Empty where the player was
            self.grid.array[deepcopy(self.unhappy_locs[i])] = 0


    def display(self, iteration: int):
        """
        Displays array with matshow
        """
        ### Colors
        cdict = {
            "0": 0
        }
        cdict.update({
            k: i + 1 for i, k in enumerate(self.groups.keys())
            })
        tab_col = list(BASE_COLORS.values())
        # Switch red and orange
        tab_col[1] = "r"
        tab_col[2] = "g"
        colors = ["w"] + [c for c in tab_col[:len(self.groups)]]
        cmap = ListedColormap(colors)

        ### Make grid showable
        elements = []
        for j in self.grid.array:
            for t in j:
                if t != 0:
                    g = t.group
                else:
                    g = t
                elements.append(g)
        display = np.array(elements).reshape(self.shape)
        # Convert strings into digits
        for k, v in cdict.items():
            display[display == k] = v
        display = display.astype(np.int64)

        ### Plot grid
        plt.matshow(display, cmap=cmap)
        plt.title(f"Iteration: {iteration}")
        plt.savefig(f"images/{iteration}.png")


    def run_simulation(self):
        """
        """
        # Generate players in grid
        self.generate_players()
        # CHANGE TO WHILE LOOP
        # TO DO: account for case when empty=0?
        moving = True
        iteration = 1
        while moving:
            if self.animate:
                self.display(iteration)
                iteration += 1

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

                    if not is_happy:
                        self.unhappy_locs.append(loc)
                        self.unhappy_p.append(p)

                # If square empty, store its location for repopulate
                else:
                    self.empty_locs.append(loc)
            
            if len(self.unhappy_locs) > 0:
                print(f"Iter {iteration}: {len(self.unhappy_locs)}")
                self.repopulate()
            else:
                moving = False
                # Create gif
                if self.animate:
                    write_gif()
