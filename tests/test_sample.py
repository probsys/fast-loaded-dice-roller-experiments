# Released under Apache 2.0; refer to LICENSE.txt

from collections import Counter
from fractions import Fraction
from itertools import product

import numpy
import pytest

from discrete_sampling.matrix import make_ddg_matrix
from discrete_sampling.matrix import make_hamming_matrix
from discrete_sampling.matrix import make_hamming_vector
from discrete_sampling.packing import pack_tree
from discrete_sampling.tree import make_ddg_tree

from discrete_sampling.sample import sample_fdr
from discrete_sampling.sample import sample_inversion_bernoulli
from discrete_sampling.sample import sample_ky_encoding
from discrete_sampling.sample import sample_ky_matrix
from discrete_sampling.sample import sample_ky_matrix_cached

from discrete_sampling.flip import BitStream
from discrete_sampling.utils import frac_to_bits_rat
from discrete_sampling.utils import get_bitstrings

from discrete_sampling.tests.utils import get_chisquare_pval

@pytest.mark.parametrize('seed', [10, 20, 100123])
def test_deterministic(seed):
    rng = numpy.random.RandomState(seed)

    Ms, k, l = [0, 31], 5, 0
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    root = make_ddg_tree(P, kp, lp)
    encoding = {}
    pack_tree(encoding, root, 0)

    bits = BitStream(kp, rng)
    N_sample = 10000
    samples_mat = [sample_ky_matrix(P, kp, lp, bits) for _i in range(N_sample)]
    samples_enc = [sample_ky_encoding(encoding, bits) for _i in range(N_sample)]
    assert Counter(samples_mat)[1] == N_sample
    assert Counter(samples_enc)[1] == N_sample

@pytest.mark.parametrize('seed', [10, 20, 100123])
def test_nondetermistic(seed):
    rng = numpy.random.RandomState(seed)

    Ms, k, l = [3, 12], 4, 0
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    root = make_ddg_tree(P, kp, lp)
    encoding = {}
    pack_tree(encoding, root, 0)

    bits = BitStream(kp, rng)
    N_sample = 10000
    samples_mat = [sample_ky_matrix(P, kp, lp, bits) for _i in range(N_sample)]
    samples_enc = [sample_ky_encoding(encoding, bits) for _i in range(N_sample)]

    pval_mat = get_chisquare_pval([3/15, 12/15], samples_mat)
    assert 0.05 < pval_mat

    pval_enc = get_chisquare_pval([3/15, 12/15], samples_enc)
    assert 0.05 < pval_enc

def test_sample_ky_matrix_cached():
    Ms, k, l = [3, 2, 1, 7, 2, 1], 4, 4
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    h = make_hamming_vector(P)
    T = make_hamming_matrix(P)

    samples = []
    bitstrings = get_bitstrings(4)
    for bits in bitstrings:
        result0 = sample_ky_matrix(P, kp, lp, (int(b) for b in bits))
        result1 = sample_ky_matrix_cached(kp, lp, h, T, (int(b) for b in bits))
        assert result0 == result1
        samples.append(result0)

    counter = Counter(samples)
    assert counter[1] == 3
    assert counter[2] == 2
    assert counter[3] == 1
    assert counter[4] == 7
    assert counter[5] == 2
    assert counter[6] == 1

fractions = [
    Fraction(1, 2),
    Fraction(3, 8),
    Fraction(2, 13),
    Fraction(19, 21),
]
seeds = [2, 10, 131]
args = list(product(fractions, seeds))
@pytest.mark.parametrize('p, seed', args)
def test_inversion_bernoulli(p, seed):
    rng = numpy.random.RandomState(seed)
    bits = BitStream(10, rng)
    N = 200000
    (a, M) = (p.numerator, p.denominator)
    samples = [sample_inversion_bernoulli(a, M, bits) for i in range(N)]
    pval = get_chisquare_pval([1-p, p], samples)
    assert 0.05 < pval

@pytest.mark.parametrize('n', range(2, 20, 2))
def test_fdr(n):
    rng = numpy.random.RandomState(2)
    bits = BitStream(n, rng)
    N_sample = 10000
    samples = [sample_fdr(n, bits) for i in range(N_sample)]
    pval = get_chisquare_pval([1/n]*n, samples)
    assert pval > 0.05
