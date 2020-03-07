# Released under Apache 2.0; refer to LICENSE.txt

from math import log2

import numpy
import pytest

from discrete_sampling.entropy import compute_entropy
from discrete_sampling.entropy import get_alpha_entropies
from discrete_sampling.entropy import sample_dirichlet

rng = numpy.random.RandomState(1)

@pytest.mark.parametrize('N', [10, 100, 1000])
def test_simulated_entropies(N):
    alphas = get_alpha_entropies(N, parallel=True)
    distributions = [sample_dirichlet(alpha, N, rng) for alpha in alphas]
    entropies = [compute_entropy(dist) for dist in distributions]

    endpoints = numpy.linspace(0, log2(N), 40)
    for i in range(1, len(endpoints)):
        start = endpoints[i-1]
        end = endpoints[i]
        vals = [e for e in entropies if start <= e <= end]
        assert len(vals) > 10

    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax.hist(entropies, bins=100)
    # ax.set_xlim([0, log2(N)])
    # plt.show()
