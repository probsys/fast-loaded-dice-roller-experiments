# Released under Apache 2.0; refer to LICENSE.txt

from fractions import Fraction
from itertools import product

import pytest

import numpy

from numpy.random import RandomState

from discrete_sampling.construct import construct_sample_alias
from discrete_sampling.construct import construct_sample_interval
from discrete_sampling.construct import construct_sample_rejection_binary_search
from discrete_sampling.construct import construct_sample_rejection_encoding
from discrete_sampling.construct import construct_sample_rejection_hash_table
from discrete_sampling.construct import construct_sample_rejection_matrix
from discrete_sampling.construct import construct_sample_rejection_matrix_cached
from discrete_sampling.construct import construct_sample_rejection_uniform

from discrete_sampling.flip import BitStream

from discrete_sampling.rejection import get_common_denominator
from discrete_sampling.rejection import get_rejection_num_trials
from discrete_sampling.rejection import get_rejection_p_success
from discrete_sampling.rejection import get_rejection_precision
from discrete_sampling.rejection import get_rejection_probabilities
from discrete_sampling.rejection import make_rejection_ddg_matrix

from discrete_sampling.sample import sample_alias
from discrete_sampling.sample import sample_interval
from discrete_sampling.sample import sample_rejection_binary_search
from discrete_sampling.sample import sample_rejection_encoding
from discrete_sampling.sample import sample_rejection_hash_table
from discrete_sampling.sample import sample_rejection_matrix
from discrete_sampling.sample import sample_rejection_matrix_cached
from discrete_sampling.sample import sample_rejection_uniform

from discrete_sampling.tests.utils import get_chisquare_pval

def test_get_common_denominator():
    p_target = [Fraction(2, 7), Fraction(13, 21), Fraction(2, 21)]
    Z = get_common_denominator(p_target)
    assert Z == 21

def test_get_rejection_precision():
    p_target = [Fraction(2, 7), Fraction(13, 21), Fraction(2, 21)]
    k = get_rejection_precision(p_target)
    assert k == 5

    p_target = [Fraction(1, 4), Fraction(3, 4)]
    k = get_rejection_precision(p_target)
    assert k == 2

def test_get_rejection_p_success_num_trials():
    p_target = [Fraction(3, 7), Fraction(1, 7), Fraction(4, 7)]
    p_success = get_rejection_p_success(p_target)
    num_trials = get_rejection_num_trials(p_target)
    assert p_success == Fraction(7, 8)
    assert num_trials == Fraction(8, 7)

    p_target = [Fraction(3, 16), Fraction(9, 16), Fraction(4, 16)]
    p_success = get_rejection_p_success(p_target)
    num_trials = get_rejection_num_trials(p_target)
    assert p_success == Fraction(1, 1)
    assert num_trials == Fraction(1, 1)

def test_get_rejection_probabilities():
    p_target = [Fraction(10, 15), Fraction(1, 15), Fraction(4, 15)]
    p_rejection = get_rejection_probabilities(p_target)
    assert p_rejection == [
        Fraction(10, 16),
        Fraction(1, 16),
        Fraction(4, 16),
        Fraction(1, 16),
    ]

    p_target = [Fraction(5, 32), Fraction(10, 32), Fraction(17, 32)]
    p_rejection = get_rejection_probabilities(p_target)
    assert p_rejection == p_target + [Fraction(0, 1)]

def make_sample_rejection_encoding(p_target):
    enc, n, k = construct_sample_rejection_encoding(p_target)
    def sampler(bitstream):
        return sample_rejection_encoding(enc, n, bitstream)
    return sampler, k

def make_sample_rejection_matrix(p_target):
    P, k, l = construct_sample_rejection_matrix(p_target)
    def sampler(bitstream):
        return sample_rejection_matrix(P, k, l, bitstream)
    return sampler, k

def make_sample_rejection_matrix_cached(p_target):
    k, l, h, T = construct_sample_rejection_matrix_cached(p_target)
    def sampler(bitstream):
        return sample_rejection_matrix_cached(k, l, h, T, bitstream)
    return sampler, k

def make_sample_rejection_uniform(p_target):
    Ms, M, n = construct_sample_rejection_uniform(p_target)
    k = 32
    def sampler(bitstream):
        return sample_rejection_uniform(Ms, M, n, bitstream)
    return sampler, k

def make_sample_rejection_hash_table(p_target):
    T, Z, k = construct_sample_rejection_hash_table(p_target)
    def sampler(bitstream):
        return sample_rejection_hash_table(T, Z, k, bitstream)
    return sampler, k

def make_sample_rejection_binary_search(p_target):
    cdf, Z, k = construct_sample_rejection_binary_search(p_target)
    def sampler(bitstream):
        return sample_rejection_binary_search(cdf, Z, k, bitstream)
    return sampler, k

def make_sample_interval(p_target):
    cdf, Z, k = construct_sample_interval(p_target)
    def sampler(bitstream):
        return sample_interval(cdf, Z, bitstream)
    return sampler, k

def make_sample_alias(p_target):
    n, qs, Ms, j = construct_sample_alias(p_target)
    k = 32
    def sampler(bitstream):
        return sample_alias(n, qs, Ms, j, bitstream)
    return sampler, k

makers = [
    make_sample_rejection_encoding,
    make_sample_rejection_matrix,
    make_sample_rejection_matrix_cached,
    make_sample_rejection_uniform,
    make_sample_rejection_hash_table,
    make_sample_rejection_binary_search,
    make_sample_interval,
    make_sample_alias,
]
p_targets = [
    [Fraction(1, 2), Fraction(1, 2)],
    [Fraction(1, 7), Fraction(6, 7)],
    [Fraction(1, 19), Fraction(6, 19), Fraction(10, 19), Fraction(2, 19)],
    [Fraction(10, 15), Fraction(1, 15), Fraction(4, 15)]
]
@pytest.mark.parametrize('maker, p_target', product(makers, p_targets))
def test_rejection_samplers(maker, p_target):
    sampler, k = maker(p_target)
    rng = RandomState(1)
    bitstream = BitStream(k, rng)
    N_sample = 10000
    samples = [sampler(bitstream) for _i in range(N_sample)]
    pval = get_chisquare_pval(p_target, samples)
    assert 0.05 < pval

@pytest.mark.parametrize('p_target', p_targets)
def test_make_rejection_ddg_matrix(p_target):
    k, l, h, T = construct_sample_rejection_matrix_cached(p_target)
    assert k == l == get_rejection_precision(p_target)

    h_rj, T_rej = make_rejection_ddg_matrix(p_target)
    assert h_rj == h

    T_rej_reshape = numpy.reshape(T_rej, (len(T), k))
    assert numpy.all(T_rej_reshape == T)
