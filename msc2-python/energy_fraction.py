import numpy as np

from giese import lisa


def main():
    cs2s = 1/3
    cs2b = (1/np.sqrt(3) - 0.01)**2
    alpha_ns = [0.578, 0.151, 0.1]
    v_walls = [0.5, 0.7, 0.8]

    # cs2s = 1/3
    # cs2b = 1/3
    # alpha_ns = [0.578, 0.151, 0.091]
    # v_walls = [0.5, 0.7, 0.77]

    for alpha_n, v_wall in zip(alpha_ns, v_walls):
        kappa = lisa.kappaNuMuModel(cs2b, cs2s, alpha_n, v_wall)
        print(kappa)


if __name__ == "__main__":
    main()
