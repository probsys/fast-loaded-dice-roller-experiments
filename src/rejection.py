# Released under Apache 2.0; refer to LICENSE.txt

from fractions import Fraction
from math import ceil
from math import log2

from numpy import cumsum

from discrete_sampling.entropy import compute_entropy
from discrete_sampling.utils import get_binary_expansion
from discrete_sampling.utils import get_common_denominator
from discrete_sampling.utils import get_common_numerators

def get_rejection_precision(p_target):
    Z = get_common_denominator(p_target)
    return ceil(log2(Z))

def get_rejection_p_success(p_target):
    Z = get_common_denominator(p_target)
    k = get_rejection_precision(p_target)
    return Fraction(Z, 2**k)

def get_rejection_num_trials(p_target):
    p_success = get_rejection_p_success(p_target)
    return 1 / p_success

def get_rejection_num_bits_per_trial(p_rejection):
    return compute_entropy(p_rejection)

def get_rejection_probabilities(p_target):
    Z = get_common_denominator(p_target)
    k = get_rejection_precision(p_target)
    numerators = get_common_numerators(Z, p_target)
    p_reject = 1 - get_rejection_p_success(p_target)
    return [Fraction(n, 2**k) for n in numerators] + [p_reject]

def get_rejection_Ms_k(p_target):
    # TODO: Use get_common_numerators from utils.
    p_rejection = get_rejection_probabilities(p_target)
    k = get_rejection_precision(p_target)
    return [int(2**k * p) for p in p_rejection], k

def get_rejection_table(p_target):
    Z = get_common_denominator(p_target)
    numerators = get_common_numerators(Z, p_target)
    T = [0] * Z
    j = 0
    for i, n in enumerate(numerators):
        T[j:j+n] = [i+1]*n
        j += n
    assert sum(1 for x in T if x > 0) == Z
    return T

def get_rejection_cdf(p_target):
    Z = get_common_denominator(p_target)
    numerators = get_common_numerators(Z, p_target)
    cdf = [0] + list(cumsum(numerators))
    return cdf

def make_rejection_ddg_matrix(p_target):
    n = len(p_target)
    Z = get_common_denominator(p_target)
    k = get_rejection_precision(p_target)
    Ms = get_common_numerators(Z, p_target)
    M_reject = (1 << k) - Z

    h = [0] * k
    H = [-1] * ((n+1)*k)

    for j in range(k):
        d = 0
        for i in range(n):
            w = (Ms[i] >> ((k-1) -j)) & 1
            h[j] += (w > 0)
            if w > 0:
                H[d*k + j] = i
                d += 1
        w = (M_reject >> ((k-1) -j)) & 1
        h[j] += (w > 0)
        if w > 0:
            H[d*k +j] = n

    return h, H
