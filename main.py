from schelling import *
import yaml

with open(Path('.').absolute() / 'configs' / 'base.yaml') as f:
    config = yaml.safe_load(f)

sim = Simulation(**config)

sim.generate_players()

sim.run_simulation()
