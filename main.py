from schelling import *

# Put this part in a config folder or something
groups = {
    "blue": 0.3,
    "red": 0.3,
    "green": 0.3
}
shape = (50, 50)
empty = 0.10
similar_list = [0.4, 0.4, 0.4]
resources_list = [200, 200, 200]

sim = Simulation(groups=groups, 
                 shape=shape,
                 empty=empty,
                 similar_list=similar_list,
                 resources_list=resources_list)

sim.generate_players()

sim.run_simulation()
