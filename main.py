from schelling import *
from experiement_functions import *

import yaml

path = 'base'
#run_experiment(path, runs=50)

path = 'basemin02'
#run_experiment(path, runs=50)

path = 'basemin03'
#run_experiment(path, runs=50)

path = 'basemin04'
#run_experiment(path, runs=50)

path = 'adaptivity02'
run_experiment(path, runs=50)

path = 'adaptivity03'
run_experiment(path, runs=50)

path = 'adaptivity04'
run_experiment(path, runs=50)

path = 'base_resource_smart'
#run_experiment(path, runs=500)

path = '3groups_base'
#run_experiment(path, runs=500)
