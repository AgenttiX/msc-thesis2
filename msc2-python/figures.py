import os.path
import time

from docs.fig.relativistic_combustion import main as rel_combustion
from examples.const_cs_gw import main as const_cs_gw
from examples.giese_lisa_fig2 import main as giese_lisa_fig2
from examples.utils import save
from examples.vm_vp_plane import main as vm_vp_plane
import const


def gen_vm_vp_fig():
    print("Generating vm-vp plane figure")
    vm_vp_fig = vm_vp_plane()
    save(vm_vp_fig, os.path.join(const.FIG_DIR, "vm_vp_plane"))


def gen_rel_combustion_fig():
    print("Generating relativistic combustion figure")
    rel_combustion(path=os.path.join(const.FIG_DIR, "relativistic_combustion"))


def gen_const_cs_gw_figs():
    print("Generating const_cs_gw figures")
    gw_figs = const_cs_gw()
    save(gw_figs[0], os.path.join(const.FIG_DIR, "const_cs_gw_v"))
    save(gw_figs[1], os.path.join(const.FIG_DIR, "const_cs_gw"))
    save(gw_figs[2], os.path.join(const.FIG_DIR, "const_cs_gw_omgw0"))


def gen_giese_lisa_fig2():
    print("Generating Giese LISA figure 2")
    fig3 = giese_lisa_fig2()
    save(fig3, os.path.join(const.FIG_DIR, "giese_lisa_fig2"))


def main():
    start_time = time.perf_counter()
    gen_vm_vp_fig()
    gen_rel_combustion_fig()
    gen_const_cs_gw_figs()
    gen_giese_lisa_fig2()
    print(f"Generating the figures took {time.perf_counter() - start_time:.2f} s.")


if __name__ == "__main__":
    main()