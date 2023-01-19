import concurrent.futures as fut
import logging
import time
import typing as tp

import numpy as np
import plotly.graph_objects as go

# import loader
# loader.load()

from pttools.analysis.plot_plotly import PlotlyPlot
from pttools.bubble.bubble import Bubble
from pttools.logging import setup_logging
from pttools.models import BagModel, ConstCSModel, Model
from giese import alpha, lisa

setup_logging()
logger = logging.getLogger(__name__)


class GieseComparison(PlotlyPlot):
    def __init__(self, models: tp.List[Model], v_walls: np.ndarray, alpha_ns: np.ndarray):
        self.models = models
        self.v_walls = v_walls
        self.alpha_ns = alpha_ns
        super().__init__()

    def compute(self, model: ConstCSModel, v_wall: float, alpha_n: float):
        bubble = Bubble(model, v_wall, alpha_n)
        bubble.solve()
        alpha_n_bar = alpha.alpha_n_bar(model, alpha_n)
        kappa_giese = lisa.kappaNuMuModel(model.csb2, model.css2, alpha_n_bar, v_wall)
        return bubble, kappa_giese

    def create_fig(self):
        start_time = time.perf_counter()
        futs = np.zeros((len(self.models), self.v_walls.size, self.alpha_ns.size), dtype=object)
        plots = []
        with fut.ProcessPoolExecutor() as executor:
            logger.info("Submitting computations")
            for i_model, model in enumerate(self.models):
                for i_v_wall, v_wall in enumerate(self.v_walls):
                    for i_alpha_n, alpha_n in enumerate(self.alpha_ns):
                        futs[i_model, i_v_wall, i_alpha_n] = executor.submit(self.compute, model, v_wall, alpha_n)

            logger.info("Processing data")
            for i_model, model in enumerate(self.models):
                data = np.zeros((self.v_walls.size, self.alpha_ns.size))
                ref = np.zeros_like(data)
                for i_v_wall, v_wall in enumerate(self.v_walls):
                    for i_alpha_n, alpha_n in enumerate(self.alpha_ns):
                        logger.debug("Processing indices %s %s %s", i_model, i_v_wall, i_alpha_n)
                        bubble, kappa_giese = futs[i_model, i_v_wall, i_alpha_n].result()
                        if bubble.failed:
                            data[i_v_wall, i_alpha_n] = np.nan
                        else:
                            data[i_v_wall, i_alpha_n] = bubble.kappa
                        ref[i_v_wall, i_alpha_n] = kappa_giese

                        # For debugging the axes
                        # if i_alpha_n == 0:
                        #     data[i_v_wall, i_alpha_n] = 0.9

                # https://plotly.com/python/builtin-colorscales/
                colors = ["viridis", "YlOrRd"]

                plots.extend([
                    go.Surface(
                        x=self.alpha_ns, y=self.v_walls, z=data,
                        name=f"PTtools {i_model+1}",
                        opacity=0.5,
                        colorscale=colors[i_model],
                        showscale=False
                    ),
                    go.Surface(
                        x=self.alpha_ns, y=self.v_walls, z=ref,
                        name=f"Giese {i_model+1}",
                        opacity=0.5,
                        colorscale=colors[i_model],
                        showscale=False
                    )
                ])

        fig = go.Figure(
            data=[
                *plots
            ],
        )
        fig.update_layout(
            scene={
                "xaxis": {
                    "title": "alpha_n"
                },
                "yaxis": {
                    "title": "v_wall"
                },
                "zaxis": {
                    "title": "kappa",
                    "range": [0, 1],
                }
            }
        )
        logger.info(f"Creating the figure took {time.perf_counter() - start_time:.3f} s")
        return fig


def main():
    plot = GieseComparison(
        models=[
            ConstCSModel(css2=1/3, csb2=1/3, a_s=1.5, a_b=1, V_s=1),
            ConstCSModel(css2=1/3 - 0.01, csb2=1/3 - 0.02, a_s=1.5, a_b=1, V_s=1)
        ],
        v_walls=np.linspace(0.2, 0.9, 20),
        alpha_ns=np.linspace(0.15, 0.5, 20)
    )
    plot.save("test")
    plot.show()


if __name__ == "__main__":
    main()
