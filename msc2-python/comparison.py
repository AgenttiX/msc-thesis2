import concurrent.futures as fut
import typing as tp

import numpy as np
import plotly.graph_objects as go

from pttools.analysis.plot_plotly import PlotlyPlot
from pttools.bubble.bubble import Bubble
from pttools.models import BagModel, ConstCSModel, Model
from giese import alpha, lisa


class GieseComparison(PlotlyPlot):
    def __init__(self, models: tp.List[Model], alpha_ns: np.ndarray, v_walls: np.ndarray):
        self.models = models
        self.alpha_ns = alpha_ns
        self.v_walls = v_walls
        super().__init__()

    def compute(self, model: ConstCSModel, alpha_n: float, v_wall: float):
        bubble = Bubble(model, alpha_n, v_wall)
        bubble.solve()
        alpha_n_bar = alpha.alpha_n_bar(model, alpha_n)
        kappa_giese = lisa.kappaNuMuModel(model.csb2, model.css2, alpha_n_bar, v_wall)
        return bubble, kappa_giese

    def create_fig(self):
        futs = np.zeros((len(self.models), self.alpha_ns.size, self.v_walls.size), dtype=object)
        plots = []
        with fut.ProcessPoolExecutor() as executor:
            print("Submitting")
            for i_model, model in enumerate(self.models):
                for i_alpha_n, alpha_n in enumerate(self.alpha_ns):
                    for i_v_wall, v_wall in enumerate(self.v_walls):
                        futs[i_model, i_alpha_n, i_v_wall] = executor.submit(self.compute, model, alpha_n, v_wall)

            print("Processing")
            for i_model, model in enumerate(self.models):
                data = np.zeros((self.alpha_ns.size, self.v_walls.size))
                ref = np.zeros_like(data)
                for i_alpha_n, alpha_n in enumerate(self.alpha_ns):
                    for i_v_wall, v_wall in enumerate(self.v_walls):
                        print(i_model, i_alpha_n, i_v_wall)
                        bubble, kappa_giese = futs[i_model, i_alpha_n, i_v_wall].result()
                        data[i_alpha_n, i_v_wall] = bubble.kappa
                        ref[i_alpha_n, i_v_wall] = kappa_giese

                plots.extend([
                    go.Surface(
                        x=self.alpha_ns, y=self.v_walls, z=data,
                        name=f"PTtools: {model.label_unicode}",
                        opacity=0.5,
                        showscale=False
                    ),
                    go.Surface(
                        x=self.alpha_ns, y=self.v_walls, z=ref,
                        name=f"Giese: {model.label_unicode}",
                        opacity=0.5,
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
        return fig


def main():
    plot = GieseComparison(
        models=[
            ConstCSModel(css2=1/3, csb2=1/3, a_s=1.5, a_b=1, V_s=1),
            ConstCSModel(css2=1/3, csb2=(1/np.sqrt(3) - 0.01) ** 2, a_s=1.5, a_b=1, V_s=1)
        ],
        alpha_ns=np.linspace(0.1, 0.6, 5),
        v_walls=np.linspace(0.5, 0.8, 5)
    )
    plot.save("test")
    plot.show()


if __name__ == "__main__":
    main()
