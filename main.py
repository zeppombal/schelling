from schelling import *

# Put this part in a config folder or something
groups = {
    "blue": 0.3,
    "red": 0.3
}
grid = Grid()
shape = (5, 5)
empty = 0.25

player_kw = {
    "similar": 0.3,
    "resources": 200
}

sim = Simulation(groups, grid, shape, empty, player_kw)

sim.generate_players()

sim.run_simulation()
