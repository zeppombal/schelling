from schelling import *

# Put this part in a config folder or something
groups = {
    "blue": 0.45,
    "red": 0.45
}
shape = (50, 50)
empty = 0.1

player_kw = {
    "similar": 0.5,
    "resources": 200
}

sim = Simulation(groups, shape, empty, player_kw)

sim.generate_players()

sim.run_simulation()
