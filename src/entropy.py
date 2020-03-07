# Released under Apache 2.0; refer to LICENSE.txt

from math import log2

import multiprocessing
import numpy

from discrete_sampling.utils import sample_dirichlet

def get_nearest_neighbors(k, values, x):
    """Return indexes of k nearest items in values to x."""
    values_idx = list(enumerate(values))
    values_sorted = sorted(values_idx, key=lambda v: abs(v[1] - x))
    result = values_sorted[:k]
    return [r[0] for r in result]

def compute_entropy(ps):
    """Compute binary entropy of the probability vector ps."""
    return sum(-log2(p)*p for p in ps if p != 0)

def get_alpha_entropies(n, maxalpha=5, numalpha=1000, parallel=None):
    """Get alphas for generating dists with entropies [0, ..., log(n)]."""
    rng = numpy.random.RandomState(1)
    # Simulate categorical distributions.
    low = -5 if n < 10000 else -7
    high = numpy.log10(maxalpha)
    alphas = numpy.logspace(low, high, numalpha)
    dists = [sample_dirichlet(alpha, n, rng) for alpha in alphas]
    # Determine the mapper.
    if parallel:
        with multiprocessing.Pool() as pool:
            entropies_list = pool.map(compute_entropy, dists)
    else:
        entropies_list = list(map(compute_entropy, dists))
    # Get the indexes of the nearest entropies to the target.
    entropies = numpy.asarray(entropies_list)
    entropies[numpy.isnan(entropies)] = 1e-10
    entropies_desired = numpy.linspace(0.001, log2(n), numalpha)
    idxs = [get_nearest_neighbors(1, entropies, e) for e in entropies_desired]
    return [alphas[i[0]] for i in idxs]
