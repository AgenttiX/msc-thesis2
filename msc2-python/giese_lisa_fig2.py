import os

import matplotlib.pyplot as plt
import numpy as np

import const
from giese.lisa import kappaNuMuModel


def main():
    fig: plt.Figure = plt.figure()
    ax: plt.Axes = fig.add_subplot()

    alpha_thetabar_ns = [0.01, 0.03, 0.1, 0.3, 1, 3]
    colors = ["b", "y", "r", "g", "purple", "grey"]
    xi_ws = np.linspace(0.2, 0.95, 50)
    for alpha_tb_n, color in zip(alpha_thetabar_ns, colors):
        for cs2b in [1/3, 1/4]:
            for cs2s, ls in zip([1/3, 1/4], ["-", "--"]):
                kappas = np.zeros_like(xi_ws)
                for i, xi_w in enumerate(xi_ws):
                    try:
                        kappa, v_arr, wow_arr, xi_arr, mode = kappaNuMuModel(cs2s=cs2s, cs2b=cs2b, al=alpha_tb_n, vw=xi_w)
                        kappas[i] = kappa
                    except ValueError:
                        kappas[i] = np.nan
                ax.plot(xi_ws, kappas, ls=ls, color=color, alpha=0.5)

    ax.set_xlabel(r"$\xi_w$")
    ax.set_ylabel(r"$\kappa$")
    ax.set_yscale("log")
    fig.savefig(os.path.join(const.FIG_DIR, "giese_lisa_fig2.png"))

    # Reference values for PTtools unit tests
    alpha_thetabar_ns_test = np.array([0.01, 0.1, 0.3])
    xi_ws_test = np.linspace(0.2, 0.9, 8, endpoint=True)
    kappas_test = np.zeros((2, 2, alpha_thetabar_ns_test.size, xi_ws_test.size))
    for i_cs2s, cs2s in enumerate([1/3, 1/4]):
        for i_cs2b, cs2b in enumerate([1/3, 1/4]):
            for i_alpha, alpha_tb_n in enumerate(alpha_thetabar_ns_test):
                for i_xi_w, xi_w in enumerate(xi_ws_test):
                    try:
                        kappa, v_arr, wow_arr, xi_arr, mode = kappaNuMuModel(cs2s=cs2s, cs2b=cs2b, al=alpha_tb_n, vw=xi_w)
                        kappas_test[i_cs2s, i_cs2b, i_alpha, i_xi_w] = kappa
                    except ValueError:
                        print(f"Error with: cs2s={cs2s}, cs2b={cs2b}, alpha_tb_n={alpha_tb_n}, xi_w={xi_w}")
                        kappas_test[i_cs2s, i_cs2b, i_alpha, i_xi_w] = np.nan
            print(cs2s, cs2b)
            print(repr(kappas_test[i_cs2s, i_cs2b, :, :]))


if __name__ == "__main__":
    main()
    plt.show()
