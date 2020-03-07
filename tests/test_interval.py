# Released under Apache 2.0; refer to LICENSE.txt

from collections import Counter
from fractions import Fraction

import numpy

from discrete_sampling.flip import BitStream
from discrete_sampling.interval import sample_interval

def test_sample_interval_crash():
    rng = numpy.random.RandomState(1)
    k = 10
    bitstream = BitStream(k, rng)
    p_target = [Fraction(1, 3), Fraction(1, 3), Fraction(1, 3)]

    n = 10000
    samples = [sample_interval(p_target, k, bitstream) for _i in range(n)]
    # TODO: An incredibly hacky test for a fair 3-dice.
    low = Fraction(1,3) - Fraction(1, 100)
    high = Fraction(1,3) + Fraction(1, 100)
    assert low <= Counter(samples)[0] / n <= high
    assert low <= Counter(samples)[1] / n <= high
    assert low <= Counter(samples)[2] / n <= high
