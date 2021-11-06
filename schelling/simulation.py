from .player import Player
from .grid import Grid
from .utils import *

from typing import *
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BASE_COLORS
from statistics import mean


class Simulation:

    def __init__(self,
                 groups: Dict[str, float],
                 shape: List[int],
                 empty: float,
                 is_costs: bool,
                 is_smart: bool,
                 max_iters: int,
                 similar_list: List[float],
                 resources_list: List[int],
                 adaptivities_list: List[float],
                 path: str,
                 seed=None,
                 animate=True):

        self.groups = groups
        self.grid = Grid(shape)
        self.shape = tuple(shape)
        self.empty = empty
        self.is_costs = is_costs
        self.is_smart = is_smart
        self.max_iters = max_iters

        assert len(groups) == len(similar_list) == len(resources_list) == len(adaptivities_list), "Length of groups and params lists are not equal."
        self.player_kw = generate_kwargs(groups, similar_list, resources_list, adaptivities_list)
        
        self.path = path
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


    def resource_filter(self, empty_locs, player):
        """
        Filters location, given resource availability
        """
        out_locs = []
        for l in empty_locs:
            cost = calc_cost(l, player.location)
            if player.resources >= cost:
                out_locs.append(l)
        
        return out_locs


    def smart_ranker(self, empty_locs, player):
        """
        Chooses the location with highest neighbor happiness
        """
        same = 0
        best_ratio = 0
        best_loc = empty_locs[0]
        for l in empty_locs:
            # Get neigbouring locations
            neighbors = self.grid.get_neighbors(l)
            for n in neighbors:
                if n.group == player.group:
                    same += 1

            try:
                ratio = same / len(neighbors)
            except ZeroDivisionError:
                ratio = 0
            
            if ratio > best_ratio:
                best_loc = l
        
        return best_loc


    def repopulate(self) -> None:
        
        rng = np.random.default_rng()
        shuffled_p = rng.permutation(range(len(self.unhappy_p)))

        resourceless = 0

        for i in shuffled_p:
            # Shuffle empty locs for no bias
            subset_locs = rng.choice(self.empty_locs, size=min(len(self.empty_locs), 20), replace=False).tolist()

            # determine which locations are accessible to player, given resources
            if self.is_costs:
                subset_locs = self.resource_filter(subset_locs, self.unhappy_p[i])

            # Player can afford some move
            if len(subset_locs) > 0:
            # Determine which location has highest same-group density
                if self.is_smart:
                    loc = self.smart_ranker(subset_locs, self.unhappy_p[i])
                else:
                    loc = subset_locs[0]

                # take loc from empty locs
                self.empty_locs = [l for l in self.empty_locs if l != tuple(loc)]
                unhappy_location = deepcopy(self.unhappy_locs[i])
                # Put player in an empty loc
                self.grid.array[tuple(loc)] = deepcopy(self.unhappy_p[i])
                # Put loc where player was in empty locs
                self.empty_locs.append(unhappy_location)
                # Empty where the player was
                if self.is_costs:
                    # Deduct cost of moving from player resources
                    cost = calc_cost(loc, self.unhappy_p[i].location)
                    self.grid.array[tuple(loc)].resources -= cost
                self.grid.array[unhappy_location] = 0
            
            # Player cannot afford a move
            else:
                resourceless += 1
        
        if len(self.unhappy_p) == resourceless:
            self.end()


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
        p = Path('.').absolute() / 'images' / self.path
        p.mkdir(parents=True, exist_ok=True)
        plt.matshow(display, cmap=cmap)
        plt.title(f"Iteration: {iteration}")
        plt.savefig(p / f"{self.path}-{iteration}.png")


    def run_simulation(self):
        """
        """
        # Generate players in grid
        self.generate_players()
        self.moving = True
        iteration = 1
        while self.moving:
            if self.animate:
                self.display(iteration)

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
            
            c1 = len(self.unhappy_locs) > 0
            c2 = len(self.empty_locs) > 0
            c3 = iteration <= self.max_iters
            if c1 and c2 and c3:
                print(f"Iter {iteration}: {len(self.unhappy_locs)}")
                self.repopulate()
                iteration += 1
            else:
                results = self.end(iteration)
                return results


    def evaluate(self, last_iter) -> Tuple[Any]:
        """
        Collects and outputs relevant statistics of the final grid
        """
        sims = {k: [] for k in self.groups.keys()}
        resources = {k: [] for k in self.groups.keys()}

        dif_edges = 0
        total_edges = 0
        visited_pairs = {}
        for p in self.grid.array.flatten():
            if p != 0:
                g = p.group
                sims[g].append(p.similar)
                resources[g].append(p.resources)
                neighbors = self.grid.get_neighbors(p.location)
                for n in neighbors:
                    # If pair has been visited, do not count
                    try:
                        if visited_pairs[tuple([p, n])] == "visited" and visited_pairs[tuple([n, p])] == "visited":
                            continue
                    except KeyError:
                        # Pair visited
                        visited_pairs[tuple([p, n])] = "visited"
                        visited_pairs[tuple([n, p])] = "visited"
                        
                        total_edges += 1
                        if n.group != g:
                            dif_edges += 1      
            else:
                continue
        
        results = dict()

        results['last_iter'] = last_iter
        results['interface_density'] = dif_edges / total_edges
        print(f"Interface density: {results['interface_density']}")

        results['unhappy'] = len(self.unhappy_locs)

        results['avg_sims'] = dict()
        results['avg_resources'] = dict()
        for k in sims.keys():
            results['avg_sims'][k] = mean(sims[k])
            results['avg_resources'][k] = mean(resources[k])
            print(f"Avg sims {k}: {results['avg_sims'][k]}")
            print(f"Avg resources {k}: {results['avg_resources'][k]}")

        return results



    def end(self, last_iter):
        """
        Ends simulation, and writes gif.
        """
        results = self.evaluate(last_iter)
        self.moving = False
        if self.animate:
            write_gif(name=self.path)
        return results