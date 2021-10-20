from schelling import *

# Put this part in a config folder or something
groups = {
    "blue": 0.4,
    "red": 0.4
}
grid = Grid()
shape = (50, 50)
empty = 0.2

player_kw = {
    "similar": 0.3,
    "resources": 200
}

sim = Simulation(groups, grid, shape, empty, player_kw)

sim.generate_players()

sim.run_simulation()
