from typing import *
from copy import deepcopy
from pathlib import Path
import os
import imageio
import numpy as np

def generate_kwargs(
    g_dict: Dict[str, float],
    similars: List[float],
    resourcess: List[int],
    adaptivities: List[float]
) -> Dict[str, Any]:
    """
    Generates player kwargs from group dictionary
    """
    kw = {}
    for g, s, a, r  in zip(g_dict.keys(), similars, adaptivities,resourcess):
        kw[f"{g}__similar"] = s
        kw[f"{g}__adaptivity"] = a
        kw[f"{g}__resources"] = r

    return kw


def handle_kwargs(g, kw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Changes player kw dictionary to assign different params to each group
    """
    out_dict = {}
    # assign group similarity to returned kwargs dict
    out_dict['similar'] = deepcopy(kw[f"{g}__similar"])
    out_dict['resources'] = deepcopy(kw[f"{g}__resources"])
    out_dict['adaptivity'] = deepcopy(kw[f"{g}__adaptivity"])

    return out_dict


def write_gif(name, folder: str = 'images'):
    """
    Writes gif with plots. 
    folder is folder in the repository where images are located
    """
    with imageio.get_writer(Path('.').absolute() / 'gifs' / f"{name}.gif", mode='I', fps=6) as writer:
        path = Path('.').absolute() / folder / name
        for p in sorted(path.iterdir(), key=os.path.getmtime):
            im = imageio.imread(p)
            writer.append_data(im)

def sample(center: float, std: float = 0.1) -> float:
    """
    """
    rng = np.random.default_rng()
    n = rng.normal(center, std, size=1)[0]

    if n < 0:
        n = 0
    elif n > 1:
        n = 1

    return n

def calc_cost(to_loc, from_loc) -> float:
    """
    """
    l1 = abs(to_loc[0] - from_loc[0])
    l2 = abs(to_loc[1] - from_loc[1])
    # Cost of moving. Not parameterizable
    cost = 1 + 3 * np.log(max(l1, l2))

    return cost
