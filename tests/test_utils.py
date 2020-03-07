# Released under Apache 2.0; refer to LICENSE.txt

import pytest

from discrete_sampling.utils import binary_search_interval
from discrete_sampling.utils import bits_to_frac
from discrete_sampling.utils import encode_binary
from discrete_sampling.utils import frac_to_bits
from discrete_sampling.utils import frac_to_bits_dyadic
from discrete_sampling.utils import frac_to_bits_rat
from discrete_sampling.utils import get_Zkl
from discrete_sampling.utils import get_binary_expansion
from discrete_sampling.utils import get_binary_expansion_length
from discrete_sampling.utils import get_k_bit_prefixes
from discrete_sampling.utils import reduce_fractions

def test_binary_search():
    arr = [0, 3, 5, 8]
    assert binary_search_interval(arr, 0) == 0
    assert binary_search_interval(arr, 1) == 0
    assert binary_search_interval(arr, 2) == 0
    assert binary_search_interval(arr, 3) == 1
    assert binary_search_interval(arr, 4) == 1
    assert binary_search_interval(arr, 5) == 2
    assert binary_search_interval(arr, 6) == 2
    assert binary_search_interval(arr, 7) == 2
    assert binary_search_interval(arr, 8) is None

def test_orderm2():
    assert get_binary_expansion_length(2) == (1,1)
    # 2^1 = 1
    assert get_binary_expansion_length(3) == (2,0)
    # 2^2-2^0 = 3 = 1*3
    assert get_binary_expansion_length(4) == (2,2)
    # 2^2 = 2
    assert get_binary_expansion_length(5) == (4,0)
    # 2^4-2^0 = 15 = 3*5
    assert get_binary_expansion_length(6) == (3,1)
    # 2^3-2^1 = 6 = 1*6
    assert get_binary_expansion_length(7) == (3,0)
    # 2^3-2^0 = 7 = 1*7
    assert get_binary_expansion_length(8) == (3,3)
    # 2^3 = 8 = 1*7
    assert get_binary_expansion_length(9) == (6,0)
    # 2^6-2^0 = 63 = 7*9
    assert get_binary_expansion_length(10) == (5,1)
    # 2^5-2^1 = 30 = 3*10
    assert get_binary_expansion_length(11) == (10,0)
    # 2^10 - 2^0 = 1023 = 93*11
    assert get_binary_expansion_length(12) == (4,2)
    # 2^4-2^2 = 12 = 1*12
    assert get_binary_expansion_length(13) == (12,0)
    # 2^12 - 2^0 = 4095 = 315*13
    assert get_binary_expansion_length(14) == (4,1)
    # 2^4-2^1 = 14 = 1*14
    assert get_binary_expansion_length(15) == (4,0)
    # 2^4-2^0 = 15 = 1*15
    assert get_binary_expansion_length(16) == (4,4)
    # 2^4 = 16 = 1*16

def test_frac_to_bits_to_frac():
    for k in range(1, 12):
        ls = get_k_bit_prefixes(k)
        for l in ls:
            Zkl = get_Zkl(k, l)
            for M in range(Zkl + 1*(k==1 and l==0)):
                bits = frac_to_bits(M, k, l)
                frac = bits_to_frac(bits, k, l)
                assert frac[0] == M

def test_reduce_fractions_unit():
    for k in [2, 5, 8, 10]:
        Ms = [2**k-1, 0, 0, 0]
        (k, l) = (k, 0)
        Mp, kp, lp = reduce_fractions(Ms, k, l)
        assert Mp == [1, 0, 0, 0]
        assert kp == 1
        assert lp == 0

def test_reduce_fraction_dyadic_simplify():
    Ms, k, l = [2, 2], 2, 2
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert Mp == [1, 1]
    assert kp == 1
    assert lp == 1

    Ms, k, l = [4, 8, 4], 4, 4
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert Mp == [1, 2, 1]
    assert kp == 2
    assert lp == 2

    Ms, k, l = [8, 16, 2, 4, 2], 5, 5
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert Mp == [4, 8, 1, 2, 1]
    assert kp == 4
    assert lp == 4

    Ms, k, l = [2, 22, 2, 4, 2], 5, 5
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert Mp == [1, 11, 1, 2, 1]
    assert kp == 4
    assert lp == 4

def test_reduce_fraction_dyadic_nosimplify():
    Ms, k, l = [3, 1], 2, 2
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert (Mp, kp, lp) == (Ms, k, l)

    Ms, k, l = [5, 7, 4], 4, 4
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert (Mp, kp, lp) == (Ms, k, l)

    Ms, k, l = [8, 16, 2, 5, 1], 5, 5
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert (Mp, kp, lp) == (Ms, k, l)

    Ms, k, l = [2, 22, 2, 5, 1], 5, 5
    Mp, kp, lp = reduce_fractions(Ms, k, l)

def test_reduce_fraction_uniform():
    Ms, k, l = [4, 4, 4], 4, 2
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert Mp == [1, 1, 1]
    assert kp == 2
    assert lp == 0

    Ms, k, l = [6, 6, 6, 6], 5, 3
    Mp, kp, lp = reduce_fractions(Ms, k, l)
    assert Mp == [1, 1, 1, 1]
    assert kp == 2
    assert lp == 2

def test_encode_binary():
    with pytest.raises(AssertionError):
        encode_binary(3, 0)
    with pytest.raises(AssertionError):
        encode_binary(3, 1)
    assert encode_binary(3, 2) == '11'
    assert encode_binary(3, 3) == '011'
    assert encode_binary(3, 4) == '0011'
    assert encode_binary(3, 5) == '00011'

    assert encode_binary(0, 0) == ''
    assert encode_binary(0, 1) == '0'
    assert encode_binary(0, 2) == '00'

    assert encode_binary(255, 10) == '0011111111'
    assert encode_binary(108, 10) == '0001101100'

def test_frac_to_bits_dyadic():
    for (x, k) in [(10, 5), (1, 11), (18, 10), (123, 9)]:
        a = frac_to_bits(x, k, k)
        b = frac_to_bits_dyadic(x, k)
        assert a == b

@pytest.mark.parametrize('a, b', [(1,2), (1,3), (7,8), (3,199)])
def test_frac_to_bits(a, b):
    assert frac_to_bits_rat(a, b) == get_binary_expansion(a, b)
