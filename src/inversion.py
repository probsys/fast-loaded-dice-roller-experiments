# Released under Apache 2.0; refer to LICENSE.txt

from fractions import Fraction
from math import ceil
from math import floor

import numpy

from discrete_sampling.utils import cumsum
from discrete_sampling.utils import randint

# ==============================================================================
# Floating point inversion sampling

def count_num_integers_between_lt(l):
    """Count the number of integers between list of values using <."""
    assert all(x>=0 for x in l)
    v = [0] * len(l)
    v[0] = ceil(l[0])
    for i in range(1, len(v)):
        right = ceil(l[i])
        left = floor(l[i-1])
        offset = (l[i-1] != int(l[i-1]))
        v[i] = max(0, right - left - offset)
    assert sum(v) == l[-1]
    return v

def count_num_integers_between_lte(l):
    """Count the number of integers between list of values using <=."""
    assert all(x>=0 for x in l)
    v = [0] * len(l)
    v[0] = ceil(l[0]) + 1*(l[0] == 0)
    for i in range(1, len(v)):
        right = ceil(l[i])
        left = floor(l[i-1])
        offset = (l[i] != int(l[i]) or l[i] == l[-1])
        v[i] = max(0, right - left - offset)
    assert sum(v) == l[-1]
    return v

def sample_inversion(p_target, k, f_comp, bitstream):
    """Sample using linear inversion sampling."""
    W = randint(k, bitstream)
    x = 0
    for i, p in enumerate(p_target):
        x += 2**k * p
        if f_comp(W, x):
            return i

def get_inversion_probabilities(Z, p_target, f_counter):
    """Return probabilities of Z-type inversion sampler."""
    n = len(p_target)
    cdf = cumsum(p_target)
    assert numpy.allclose(float(cdf[-1]), 1)
    cdf[-1] = 1

    endpoints = [Z*c for c in cdf]
    assert endpoints[-1] == Z
    counts = f_counter(endpoints)

    assert sum(counts) == Z
    assert len(counts) == n
    return [Fraction(int(d), int(Z)) for d in counts]

def sample_inversion_lt(p_target, k, bitstream):
    f_comp = lambda W, x: W < x
    return sample_inversion(p_target, k, f_comp, bitstream)

def sample_inversion_lte(p_target, k, bitstream):
    f_comp = lambda W, x: W <= x
    return sample_inversion(p_target, k, f_comp, bitstream)

def get_inversion_probabilities_lt(Z, p_target):
    f_counter = count_num_integers_between_lt
    return get_inversion_probabilities(Z, p_target, f_counter)

def get_inversion_probabilities_lte(Z, p_target):
    f_counter = count_num_integers_between_lte
    return get_inversion_probabilities(Z, p_target, f_counter)
