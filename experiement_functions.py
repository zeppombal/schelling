from schelling import *
import yaml
from statistics import mean, stdev


def summarize_results(path, results_dicts):
    
    exp_results = dict()
    exp_results['avg_interface_density'] = mean(
        [r['interface_density'] for r in results_dicts])
    keys = ['blue', 'red']
    exp_results['avg_sims'] = dict()
    exp_results['stdev_sims'] = dict()
    exp_results['avg_resources'] = dict()
    exp_results['stdev_resources'] = dict()

    for k in keys:
        avg_sims_list_k = [r['avg_sims'][k] for r in results_dicts]
        exp_results['avg_sims'][k] = mean(avg_sims_list_k)
        exp_results['stdev_sims'][k] = stdev(avg_sims_list_k)

        avg_resources_list_k = [r['avg_resources'][k] for r in results_dicts]
        exp_results['avg_resources'][k] = mean(avg_resources_list_k)
        exp_results['stdev_resources'][k] = stdev(avg_resources_list_k)

    with open(Path('.').absolute() / 'results' / f"{path}.yaml", 'w') as outfile:
        yaml.dump(exp_results, outfile, default_flow_style=False)
    
    return(exp_results)

def run_experiment(path, runs):
    with open(Path('.').absolute() / 'configs' / f"{path}.yaml") as f:
        config = yaml.safe_load(f)
    results_dicts = list()
    for r in range(runs):
        sim = Simulation(**config, path=path)
        if r == 0:
            sim.animate = True
        else:
            sim.animate = False
        results = sim.run_simulation()
        results_dicts.append(results)
    res = summarize_results(path, results_dicts)
    return res
