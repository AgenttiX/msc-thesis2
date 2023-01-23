import matplotlib.pyplot as plt

from giese.lisa import kappaNuMuModel


kappa, v, wow, xi, mode = kappaNuMuModel(cs2b=1/3, cs2s=1/3, al=0.1, vw=0.75)
print(mode)

fig: plt.Figure = plt.figure()
ax: plt.Axes = fig.add_subplot()
ax.plot(xi, v)
ax.set_xlabel("xi")
ax.set_ylabel("v")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

plt.show()
