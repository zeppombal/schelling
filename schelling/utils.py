from typing import *
from copy import deepcopy
from pathlib import Path
import os
import imageio

def generate_kwargs(
    g_dict: Dict[str, float],
    similars: List[float],
    resourcess: List[int]
) -> Dict[str, Any]:
    """
    Generates player kwargs from group dictionary
    """
    kw = {}
    for g, s, r  in zip(g_dict.keys(), similars, resourcess):
        kw[f"{g}__similar"] = s
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

    return out_dict


def write_gif(folder: str = 'images'):
    """
    Writes gif with plots. 
    folder is folder in the repository where images are located
    """
    with imageio.get_writer('sim.gif', mode='I', fps=6) as writer:
        path = Path('.').absolute() / folder
        for p in sorted(path.iterdir(), key=os.path.getmtime):
            im = imageio.imread(p)
            writer.append_data(im)
            p.unlink()
