from schelling import *
import yaml
import sys

#with open(Path('.').absolute() / 'configs' / f'{sys.argv[1]}.yaml') as f:
#    config = yaml.safe_load(f)
path = 'base'
with open(Path('.').absolute() / 'configs' / f"{path}.yaml") as f:
    config = yaml.safe_load(f)

sim = Simulation(**config, path=path)

sim.run_simulation()
