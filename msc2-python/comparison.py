import concurrent.futures as fut
import logging
import matplotlib.pyplot as plt
import time
import typing as tp

import numpy as np
import plotly.graph_objects as go

# import loader
# loader.load()

from pttools.bubble.quantities import get_kappa
from pttools.bubble.bubble import Bubble
from pttools.logging import setup_logging
from pttools.models import BagModel, ConstCSModel, Model
from giese import lisa

setup_logging()
logger = logging.getLogger(__name__)


class GieseComparison:
    def __init__(
            self,
            models: tp.List[Model], v_walls: np.ndarray, alpha_ns: np.ndarray,
            i_v_walls_fig: np.ndarray, i_alpha_ns_fig: np.ndarray
    ):
        self.models = models
        self.v_walls = v_walls
        self.alpha_ns = alpha_ns
        self.i_v_walls_fig = i_v_walls_fig
        self.i_alpha_ns_fig = i_alpha_ns_fig

    def compute_bubble(self, model: ConstCSModel, v_wall: float, alpha_n: float):
        bubble = Bubble(model, v_wall, alpha_n) # , n_points=100000)
        bubble.solve()
        alpha_n_bar = model.alpha_n_bar(alpha_n)
        # kappa_old = get_kappa(v_wall, alpha_n) if model.css2 == 1/3 and model.csb2 == 1/3 else None
        kappa_old = None
        giese_params = lisa.kappaNuMuModel(model.csb2, model.css2, alpha_n_bar, v_wall)
        return bubble, kappa_old, giese_params

    def process(self):
        start_time = time.perf_counter()
        futs = np.zeros((len(self.models), self.v_walls.size, self.alpha_ns.size), dtype=object)

        fig: plt.Figure
        axs: np.ndarray
        fig, axs = plt.subplots(
            self.i_v_walls_fig.size, self.i_alpha_ns_fig.size,
            figsize=(29.7, 21)
        )

        with fut.ProcessPoolExecutor() as executor:
            logger.info("Submitting computations")
            for i_model, model in enumerate(self.models):
                for i_v_wall, v_wall in enumerate(self.v_walls):
                    for i_alpha_n, alpha_n in enumerate(self.alpha_ns):
                        futs[i_model, i_v_wall, i_alpha_n] = \
                            executor.submit(self.compute_bubble, model, v_wall, alpha_n)

            logger.info("Processing data")
            for i_model, model in enumerate(self.models):
                data_new = np.zeros((self.v_walls.size, self.alpha_ns.size))
                data_old = np.zeros_like(data_new)
                data_giese = np.zeros_like(data_new)
                for i_v_wall, v_wall in enumerate(self.v_walls):
                    i_v_wall_fig_arr = np.argwhere(i_v_wall == self.i_v_walls_fig)
                    i_v_wall_fig = i_v_wall_fig_arr[0, 0] if i_v_wall_fig_arr.size else None

                    for i_alpha_n, alpha_n in enumerate(self.alpha_ns):
                        logger.debug("Processing indices %s %s %s", i_model, i_v_wall, i_alpha_n)
                        i_alpha_n_fig_arr = np.argwhere(i_alpha_n == self.i_alpha_ns_fig)
                        i_alpha_n_fig = i_alpha_n_fig_arr[0, 0] if i_alpha_n_fig_arr.size else None

                        bubble, kappa_old, giese_params = futs[i_model, i_v_wall, i_alpha_n].result()

                        # Plotly plot
                        if bubble.failed or bubble.invalid:
                            data_new[i_v_wall, i_alpha_n] = np.nan
                        else:
                            data_new[i_v_wall, i_alpha_n] = bubble.kappa
                        data_old[i_v_wall, i_alpha_n] = kappa_old
                        data_giese[i_v_wall, i_alpha_n] = giese_params[0]

                        # For debugging the axes
                        # if i_alpha_n == 0:
                        #     data[i_v_wall, i_alpha_n] = 0.9

                        # Matplotlib plot
                        if i_v_wall_fig is not None and i_alpha_n_fig is not None:
                            ax: plt.Axes = axs[i_v_wall_fig, i_alpha_n_fig]
                            ax.plot(bubble.xi, bubble.v)
                            ax.plot(giese_params[3], giese_params[1])
                            ax.set_xlim(0, 1)
                            ax.set_ylim(0, 1)
                            ax.set_xlabel(r"$\xi$")
                            ax.set_ylabel("$v$")
                            ax.set_title(
                                rf"$v_w={v_wall:.3f}, \alpha_n={alpha_n:.3f}, "
                                rf"\kappa_{{new}}={bubble.kappa:.3f}, \kappa_G={giese_params[0]:.3f}$")

                # https://plotly.com/python/builtin-colorscales/
                colors = ["viridis", "YlOrRd"]

                plots = [
                    go.Surface(
                        x=self.alpha_ns, y=self.v_walls, z=data_new,
                        name=f"New {i_model+1}",
                        opacity=0.5,
                        colorscale=colors[i_model],
                        showscale=False
                    ),
                    # go.Surface(
                    #     x=self.alpha_ns, y=self.v_walls, z=data_old,
                    #     name=f"Old {i_model + 1}",
                    #     opacity=0.5,
                    #     colorscale=colors[i_model],
                    #     showscale=False
                    # ),
                    go.Surface(
                        x=self.alpha_ns, y=self.v_walls, z=data_giese,
                        name=f"Giese {i_model+1}",
                        opacity=0.5,
                        colorscale=colors[i_model],
                        showscale=False
                    )
                ]

        fig_3d = go.Figure(
            data=[
                *plots
            ],
        )
        fig_3d.update_layout(
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

        fig.tight_layout()

        logger.info(f"Computation took {time.perf_counter() - start_time:.3f} s")

        return fig_3d, fig


def main():
    plot = GieseComparison(
        models=[
            # ConstCSModel(css2=1/3, csb2=1/3, a_s=1.5, a_b=1, V_s=1),
            ConstCSModel(css2=1/3 - 0.01, csb2=1/3 - 0.02, a_s=1.5, a_b=1, V_s=1)
        ],
        v_walls=np.linspace(0.2, 0.9, 20),
        alpha_ns=np.linspace(0.15, 0.5, 20),
        i_alpha_ns_fig=np.array([0, 10, 19]),
        i_v_walls_fig=np.array([0, 10, 15]),
    )
    fig_3d, fig = plot.process()
    fig_3d.write_html("test.html")
    fig_3d.write_image("test.png")

    fig.savefig("test2.png")

    fig_3d.show()
    plt.show()


if __name__ == "__main__":
    main()
