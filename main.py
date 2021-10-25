from schelling import *
import yaml
import sys

#with open(Path('.').absolute() / 'configs' / f'{sys.argv[1]}.yaml') as f:
#    config = yaml.safe_load(f)
with open(Path('.').absolute() / 'configs' / f'3groups_base.yaml') as f:
    config = yaml.safe_load(f)

sim = Simulation(**config)

sim.run_simulation()
