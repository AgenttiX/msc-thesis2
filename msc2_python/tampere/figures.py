import os

from matplotlib import rc_context
import matplotlib.pyplot as plt
import numpy as np

from examples.utils import save
from pttools.logging import setup_logging
from pttools.models import BagModel, ConstCSModel
from pttools.analysis.bubble_grid import BubbleGridVWAlpha
from pttools.analysis.plot_entropy_grid import EntropyPlot, compute

import const

FIG_DIR = os.path.join(const.FIG_DIR, "tampere")
if not os.path.exists(FIG_DIR):
    os.mkdir(FIG_DIR)


def main():
    n_points = 100

    models = [
        BagModel(g_s=123, g_b=120, V_s=0.9),
        ConstCSModel(css2=1/3 - 0.01, csb2=1/3 - 0.011, g_s=123, g_b=120, V_s=0.9)
    ]
    alpha_n_min = np.max([model.alpha_n_min for model in models])
    if alpha_n_min >= 0.05:
        raise ValueError

    v_walls = np.linspace(0.05, 0.95, n_points)
    alpha_ns = v_walls

    min_level = -0.3
    max_level = 0.4
    diff_level = 0.05

    with rc_context({"font.size": 16}):
        for model in models:
            grid = BubbleGridVWAlpha(model, v_walls, alpha_ns, compute)
            s_total_rel = grid.data[0]

            # figsize = (5, 4)
            figsize = None
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot()
            EntropyPlot(grid, s_total_rel, min_level, max_level, diff_level, fig, ax)
            fig.tight_layout()
            save(fig, os.path.join(FIG_DIR, f"entropy_{model.name}"), bbox_inches="tight", pad_inches=0)
            plt.close(fig)

            # KappaPlot is no longer available in PTtools
            # fig = plt.figure(figsize=figsize)
            # ax = fig.add_subplot()
            # KappaPlot(grid, fig, ax)
            # fig.tight_layout()
            # save(fig, os.path.join(FIG_DIR, f"kappa_{model.name}"), bbox_inches="tight", pad_inches=0)
            # plt.close(fig)


if __name__ == "__main__":
    setup_logging(const.LOG_DIR)
    main()
