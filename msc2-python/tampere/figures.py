import os.path

import matplotlib.pyplot as plt
import numpy as np

from pttools.logging import setup_logging
from pttools.models import BagModel, ConstCSModel
from pttools.analysis.plot_entropy import BubbleGridVWAlpha, EntropyPlot, compute

import const


def main():
    n_points = 5

    models = [
        BagModel(g_s=123, g_b=120, V_s=0.9),
        ConstCSModel(css2=1/3 - 0.01, csb2=1/3 - 0.011, g_s=123, g_b=120, V_s=0.9)
    ]
    # alpha_n_min = np.max([model.alpha_n_min for model in models]) + 0.01

    v_walls = np.linspace(0.05, 0.95, n_points)
    alpha_ns = v_walls

    min_level = -0.3
    max_level = 0.4
    diff_level = 0.05

    for model in models:
        grid = BubbleGridVWAlpha(model, v_walls, alpha_ns, compute)
        s_total_rel = grid.data[0]

        fig = plt.figure()
        ax = fig.add_subplot()
        EntropyPlot(grid, s_total_rel, min_level, max_level, diff_level, fig, ax)
        fig.savefig(os.path.join(os.path.abspath(const.FIG_DIR)))
        plt.close(fig)


if __name__ == "__main__":
    setup_logging(const.LOG_DIR)
    main()
