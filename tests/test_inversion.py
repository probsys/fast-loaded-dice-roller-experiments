# Released under Apache 2.0; refer to LICENSE.txt

from fractions import Fraction

import numpy

from discrete_sampling.flip import BitStream

from discrete_sampling.inversion import count_num_integers_between_lt
from discrete_sampling.inversion import count_num_integers_between_lte
from discrete_sampling.inversion import get_inversion_probabilities_lt
from discrete_sampling.inversion import get_inversion_probabilities_lte
from discrete_sampling.inversion import sample_inversion_lt
from discrete_sampling.inversion import sample_inversion_lte

def test_count_num_integers_between():
    l = [1.8, 4.3, 4.7, 5, 7.4, 8.0,]
    between_lt = count_num_integers_between_lt(l)
    assert between_lt == [
        len([0,1]),
        len([2,3,4]),
        len([]),
        len([]),
        len([5,6,7]),
        len([]),
        ]

    between_lte = count_num_integers_between_lte(l)
    assert between_lte == [
        len([0,1]),
        len([2,3,4]),
        len([]),
        len([5]),
        len([6,7]),
        len([]),
        ]

    l = [0, .7, 1, 1.9, 2., 5.7, 8.0]
    between_lt = count_num_integers_between_lt(l)
    assert between_lt == [
        len([]),
        len([0]),
        len([]),
        len([1]),
        len([]),
        len([2,3,4,5]),
        len([6,7]),
        ]

    between_lte = count_num_integers_between_lte(l)
    assert between_lte == [
        len([0]),
        len([]),
        len([1]),
        len([]),
        len([2]),
        len([3,4,5]),
        len([6,7]),
        ]

    l = [0, 0, 1, 1.9, 2., 4, 4]
    between_lt = count_num_integers_between_lt(l)
    assert between_lt == [
        len([]),
        len([]),
        len([0]),
        len([1]),
        len([]),
        len([2,3]),
        len([]),
        ]

    between_lte = count_num_integers_between_lte(l)
    assert between_lte == [
        len([0]),
        len([]),
        len([1]),
        len([]),
        len([2]),
        len([3]),
        len([]),
        ]

def test_inversion_exact():
    # TODO: Run some statistical GOF tests.
    rng = numpy.random.RandomState(10)
    p_target = [0, Fraction(1, 4), Fraction(2, 4), Fraction(0), Fraction(1,4)]
    for k in range(2, 10):
        bitstream = BitStream(k, rng)
        Z = 2**k
        p_inv_lt = get_inversion_probabilities_lt(Z, p_target)
        assert p_inv_lt == p_target
        for _j in range(10):
            sample_inversion_lt(p_target, k, bitstream)

        p_inv_lte = get_inversion_probabilities_lte(Z, p_target)
        assert p_inv_lte != p_target
        for _j in range(10):
            sample_inversion_lte(p_target, k, bitstream)
