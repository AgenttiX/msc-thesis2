from pttools.bubble import Phase
from pttools.models import Model


def alpha_n_bar(model: Model, alpha_n: float):
    wn = model.w_n(alpha_n)
    return alpha_n + (1-1/(3*model.cs2(wn, Phase.BROKEN))) * (model.p(wn, Phase.SYMMETRIC) - model.p(wn, Phase.BROKEN))
