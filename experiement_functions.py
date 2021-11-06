from schelling import *
import yaml
from statistics import mean, stdev


def summarize_results(path, groups, results_dicts):
    
    exp_results = dict()

    measures = results_dicts[0].keys()
    per_group_measures, overarching_measures = [], []
    for m in measures:
        if isinstance(results_dicts[0][m], dict):
            per_group_measures.append(m)
        else:
            overarching_measures.append(m)

    for m in overarching_measures:
        m_list = [r[m] for r in results_dicts]
        exp_results[m] = {'mean': mean(m_list), 'stdev': stdev(m_list)}
    for m in per_group_measures:
        exp_results[m] = dict()
        for g in groups:
            m_g_list = [r[m][g] for r in results_dicts]
            exp_results[m][g] = {'mean': mean(m_g_list), 'stdev': stdev(m_g_list)}

    with open(Path('.').absolute() / 'results' / f"{path}.yaml", 'w') as outfile:
        yaml.dump(exp_results, outfile, default_flow_style=False)
    
    return(exp_results)

def run_experiment(path, runs):
    with open(Path('.').absolute() / 'configs' / f"{path}.yaml") as f:
        config = yaml.safe_load(f)
    results_dicts = list()
    for r in range(runs):
        print(f'exp {path}, run {r+1}/{runs} ---------------------------------')
        sim = Simulation(**config, path=path)
        if r == 0:
            sim.animate = True
        else:
            sim.animate = False
        results = sim.run_simulation()
        results_dicts.append(results)
    res = summarize_results(
        path=path,
        groups=list(config['groups'].keys()),
        results_dicts=results_dicts)
    return res
