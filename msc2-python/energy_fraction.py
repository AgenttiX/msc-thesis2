import giese_lisa


def main():
    cs2b = 1/3
    cs2s = 1/3
    al = 0.1
    vw = 0.5
    kappa = giese_lisa.kappaNuMuModel(cs2b, cs2s, al, vw)
    print(kappa)


if __name__ == "__main__":
    main()
