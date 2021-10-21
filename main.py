from schelling import *

# Put this part in a config folder or something
groups = {
    "blue": 0.3,
    "red": 0.3,
    "green": 0.3
}
shape = (50, 50)
empty = 0.10

player_kw = {
    "similar": 0.5,
    "resources": 200
}

sim = Simulation(groups, shape, empty, player_kw)

sim.generate_players()

sim.run_simulation()
