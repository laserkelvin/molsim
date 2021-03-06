
from molsim.mcmc.base import GaussianLikelihood, UniformLikelihood
from molsim.mcmc.models import SingleComponent, MultiComponent

import numpy as np


def test_likelihoods():
    source_size = UniformLikelihood.from_values("ss", 0., 400.)
    ncol = UniformLikelihood.from_values("ncol", 0., 1e16)
    vlsr = UniformLikelihood.from_values("vlsr", 0., 10.)
    Tex = GaussianLikelihood.from_values("tex", 5.8, 0.5, 0., 10.)
    dV = GaussianLikelihood.from_values("dV", 0.1, 1e-1, 0., 0.3)

    uniform_test = source_size.ln_likelihood(100.)
    assert uniform_test == 0.

    normal_test = Tex.ln_likelihood(5.87)
    assert np.round(
        np.abs(-0.23559135 - normal_test), 4
    ) == 0.

    fail_test = dV.ln_likelihood(-5.)
    assert not np.isfinite(fail_test)


def test_single_component():
    source_size = UniformLikelihood.from_values("ss", 0., 400.)
    ncol = UniformLikelihood.from_values("ncol", 0., 1e16)
    vlsr = UniformLikelihood.from_values("vlsr", 0., 10.)
    Tex = GaussianLikelihood.from_values("tex", 5.8, 0.5, 0., 10.)
    dV = GaussianLikelihood.from_values("dV", 0.1, 1e-1, 0., 0.3)

    model = SingleComponent(
        source_size,
        vlsr,
        ncol,
        Tex,
        dV,
        None,
        )
    initial = model.initialize_values()
    assert initial == [200., 5., 5e15, 5.8, 0.1]


def test_multi_component():
    source_sizes = [UniformLikelihood.from_values("ss", 0., 400.) for _ in range(4)]
    vlsrs = [UniformLikelihood.from_values("vlsr", 0., 10.) for _ in range(4)]
    ncols = [UniformLikelihood.from_values("ncol", 0., 1e16) for _ in range(4)]
    Tex = GaussianLikelihood.from_values("tex", 5.8, 0.5, 0., 10.)
    dV = GaussianLikelihood.from_values("dV", 0.1, 1e-1, 0., 0.3)

    model = MultiComponent(
        source_sizes,
        vlsrs,
        ncols,
        Tex,
        dV,
        None,
        )

    # should be 14 parameters total; 3 * 4 components + 2
    assert len(model) == 14

    model._get_components()

    # make sure the combined likelihood looks reasonable
    parameters = [100., 96, 20, 45, 5., 5.6, 6.44, 4.3, 1e10, 1e11, 1e9, 1e11, 5.87, 0.09216]
    likelihood = model.compute_prior_likelihood(parameters)
    assert np.round(abs(likelihood - 4.579927708578582)) == 0.
