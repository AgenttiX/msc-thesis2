"""
This is the example code from:
Model-independent energy budget for Lisa
by Giese et al.
https://arxiv.org/abs/2010.09744

Commented for better readability.
"""

import typing as tp

import numpy as np
from scipy.integrate import odeint
from scipy.integrate import simps


def mu(a, b):
    """Relative velocity (special relativistic)"""
    return (a-b)/(1.-a*b)


def getwow(a, b):
    """Ratio of enthalpies across the bubble wall, "w over w" """
    return a/(1.-a**2)/b*(1.-b**2)


def getvm(al: float, vw: float, cs2b: float) -> tp.Tuple[float, int]:
    """Fluid velocity behind the wall, $v_-$"""
    if vw**2 < cs2b:
        return vw, 0
    cc = 1. - 3. * al + vw**2 * (1./cs2b + 3.*al)
    disc = -4.*vw**2/cs2b + cc**2
    if disc < 0. or cc < 0.:
        return np.sqrt(cs2b), 1
    return cc + np.sqrt(disc), 2


def dfdv(xiw: tp.Union[tp.Tuple[float, float], np.ndarray], v: float, cs2: float) -> tp.List[float]:
    """The differential equation that is solved in the shock/rarefaction wave

    Rarefaction = the opposite of compression
    """
    xi, w = xiw
    dxidv = mu(xi, v)**2 / cs2 - 1.
    dxidv *= (1. - v*xi)*xi/2./v/(1.-v**2)
    dwdv = (1.+1./cs2) * mu(xi, v) * w/(1.-v**2)
    return [dxidv, dwdv]


def getKandWow(vw: float, v0: float, cs2: float) -> tp.Tuple[float, float]:
    """
    Returns two values
    - Enthalpy-weighted kinetic energy in the shock/rarefaction wave
    - Ratio between the enthalpy density at the start of the shock/rarefaction compared to its end"""
    if v0 == 0:
        return 0, 1
    n = 8*1024  # change accuracy here
    vs = np.linspace(v0, 0, n)
    # Get (xi, wow) for each v
    sol = odeint(dfdv, [vw, 1.], vs, args=(cs2, ))
    xis, wows = (sol[:, 0], sol[:, 1])
    # If the wall moves at less than the sound speed = is subsonic
    if mu(vw, v0) * vw <= cs2:
        ll = max(int(sum(np.heaviside(cs2 - (mu(xis, vs)*xis), 0.0))), 1)
        vs = vs[:ll]
        xis = xis[:ll]
        wows = wows[:ll] / wows[ll-1] * getwow(xis[-1], mu(xis[-1], vs[-1]))
    Kint = simps(wows*(xis*vs)**2/(1.-vs**2), xis)
    return Kint*4./vw**3, wows[0]


def alN(al, wow, cs2b, cs2s):
    r"""$\alpha_{\bar{theta}n}$ in the nucleation phase (in front of the shock)"""
    da = (1./cs2b - 1./cs2s)/(1./cs2s + 1.)/3.
    return (al + da)*wow - da


def getalNwow(vp, vm, vw, cs2b, cs2s):
    r"""Get
    - $\alpha_{\bar{\theta}}n}$ in the nucleation phase
    - Ratio of the enthalpies for fixed boundary conditions at the wall
    """
    Ksh, wow = getKandWow(vw, mu(vw, vp), cs2s)
    al = (vp/vm-1.)*(vp*vm/cs2b - 1.)/(1-vp**2)/3.
    return alN(al, wow, cs2b, cs2s), wow


def kappaNuMuModel(cs2b, cs2s, al, vw):
    r"""Calculate the efficiency factor $\kappa$.
    This uses the other functions."""
    vm, mode = getvm(al, vw, cs2b)
    if mode < 2:
        # Validate alpha
        almax, wow = getalNwow(0, vm, vw, cs2b, cs2s)
        if almax < al:
            print("alpha too large for shock")
            return 0
        vp = min(cs2s/vw, vw)
        almin, wow = getalNwow(vp, vm, vw, cs2b, cs2s)
        if almin > al:
            print("alpha too small for shock")
            return 0
        # Iterate to find v+ until the corresponding alpha matches the given value.
        iv = [[vp, almin], [0, almax]]
        while abs(iv[1][0] - iv[0][0]) > 1e-7:
            # mean v
            vpm = (iv[1][0] + iv[0][0])/2.
            alm = getalNwow(vpm, vm, vw, cs2b, cs2s)[0]
            if alm > al:
                # Update second component.
                iv = [iv[0], [vpm, alm]]
            else:
                # Update first component.
                iv = [[vpm, alm], iv[1]]
        # Use the mean as v+
        vp = (iv[1][0] + iv[0][0])/2.
        Ksh, wow = getKandWow(vw, mu(vw, vp), cs2s)
    else:
        Ksh, wow, vp = 0, 1, vw
    if mode > 0:
        # Fixed a typo here: wow3 -> wow
        Krf, wow = getKandWow(vw, mu(vw, vm), cs2b)
        Krf *= -wow*getwow(vp, vm)
    else:
        Krf = 0
    return (Ksh + Krf)/al