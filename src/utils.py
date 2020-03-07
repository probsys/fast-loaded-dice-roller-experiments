# Released under Apache 2.0; refer to LICENSE.txt

import itertools
import os
import subprocess

from fractions import Fraction
from math import isinf
from math import isnan
from math import log2

from numpy import lcm

PATH = os.path.dirname(os.path.abspath(__file__))
ORDERM2 = os.path.join(PATH, 'orderm2')
BINEXP = os.path.join(PATH, 'binexp')

def get_common_denominator(probabilities):
    """Return least Z such that each probability is a multiple of 1/Z."""
    denominators = [p.denominator for p in probabilities]
    return lcm.reduce(denominators)

def get_common_numerators(Z, probabilities):
    """Return numerator of probabilities expresses in the common base Z."""
    return [int(Z*p) for p in probabilities]

def get_bitstrings(k):
    """Return all length-k binary strings."""
    tuples = itertools.product(*[(0,1) for _i in range(k)])
    strings = [''.join(map(str, t)) for t in tuples]
    return strings

def get_enumeration_tuples(Z, n):
    """Get all length-n tuples of nonnegative integers which sum to Z."""
    sequences = itertools.product(*[range(Z+1) for _i in range(n)])
    return filter(lambda s: sum(s)==Z, sequences)

def sample_dirichlet(alpha, N, rng):
    """Hacky (but table) sampler for Dirichlet."""
    MAXITER = 1000
    for i in range(MAXITER):
        try:
            dist = rng.dirichlet([alpha] * N)
            nans = any(map(isnan, dist))
            infs = any(map(isinf, dist))
            if not (nans or infs):
                return dist
        except ZeroDivisionError:
            continue
    else:
        assert False, 'Failed to generate dirichlet distribution.'

def sample_dirichlet_multinomial(alpha, N, Z, rng):
    """Hacky (but stable) sampler for Dirichlet-Multinomial."""
    probabilities = sample_dirichlet(alpha, N, rng)
    numerators = rng.multinomial(Z, probabilities)
    return [Fraction(int(n), Z) for n in numerators]

def sample_dirichlet_multinomial_positive(alpha, N, Z, rng):
    """Hack (but stable) sampler for positive Dirichlet-Multinomial."""
    assert N <= Z
    probabilities = sample_dirichlet(alpha, N, rng)
    numerators = rng.multinomial(Z-N, probabilities)
    numerators += [1] * N
    return [Fraction(int(n), Z) for n in numerators]

def sample_simplex(Z, n, alpha, rng, strict=None):
    """Get a random length-n Z-type probability vector"""
    if strict and Z < n:
        raise ValueError('Cannot sample from simplex strictly, increase Z.')
    low = 0 if strict is None else 1
    probs = sample_dirichlet(alpha, n, rng)
    numerators = [max(low, int(Z*p)) for p in probs]
    shortfall = sum(numerators) - Z
    delta = 1 if shortfall < 0 else -1
    while shortfall != 0:
        idxs = [i for i, n in enumerate(numerators) if low <= n + delta <= Z]
        i = rng.choice(idxs)
        numerators[i] += delta
        shortfall += delta
    assert sum(numerators) == Z
    return [Fraction(n, Z) for n in numerators]

def normalize_vector(Z, Ms):
    """Normalize list of Ms by Z."""
    assert all(0 <= M <= Z for M in Ms)
    assert sum(Ms) <= Z
    return [Fraction(M, Z) for M in Ms]

def get_k_bit_prefixes(k):
    """Return list of prefix lengths using k-bit precision."""
    return list(range(k, -1, -1))

def get_Zb(k, l):
    """Return Z for k-l length suffix."""
    assert 0 < k and 0 <= l <= k
    return pow(2, k-l) - 1*(l<k)

def get_Zkl(k, l):
    """Return Z for k-bit precision and prefix length l."""
    assert 0 < k and 0 <= l <= k
    return pow(2, k) - pow(2, l)*(l<k)

def get_Zkl_list(k):
    """Return list of Z for k-bit precision and prefix lengths k, ..., 0."""
    ls = get_k_bit_prefixes(k)
    return [get_Zkl(k, l) for l in ls]

def argmin2(l):
    """Return the indexes of the smalles two items in l."""
    (j1, m1) = (-1, float('inf'))
    (j2, m2) = (-1, float('inf'))
    for ix, x in enumerate(l):
        if x <= m1:
            (j2, m2) = (j1, m1)
            (j1, m1) = (ix, x)
        elif x < m2:
            (j2, m2) = (ix, x)
    return (j1, j2)

def argmin(l):
    """Return in the index of the smallest item in l."""
    (j1, _j2) = argmin2(l)
    return j1

def cumsum(xs):
    """Return list of running probability sums with overflow control."""
    s = 0
    l = []
    for x in xs:
        s += x
        l.append(min(1, s))
    return l

def bits_to_int(bits):
    sbits = ''.join(map(str, bits))
    return int(sbits, 2)

def randint(k, bitstream):
    bits = [next(bitstream) for i in range(k)]
    return bits_to_int(bits)

def frac_to_bits_rat(a, b):
    """Return bits in the binary expansion of a/b in [0,1]."""
    # http://cs.furman.edu/digitaldomain/more/ch6/dec_frac_to_bin.htm
    assert 0 <= a <= b
    x = a
    xs = []
    cache = {}
    i = 0
    while True:
        x = 2*x
        if x in cache:
            l = cache[x]
            break
        d = int(b <= x)
        xs.append(d)
        cache[x] = i
        i += 1
        if x == b:
            l = i
            break
        if x > b:
            x = x - b
    prefix = tuple(xs[:l])
    suffix = tuple(xs[l:])
    return (prefix, suffix)

def binary_search_interval(arr, x):
    """Return index j such that arr[j] <= x < arr[j+1] or None."""
    l = 0
    r = len(arr) - 1
    while l <= r:
        mid = l + (r - l) // 2
        if (arr[mid-1] <= x) and (x < arr[mid]):
            return mid - 1
        elif arr[mid] <= x:
            l = mid + 1
        else:
            r = mid - 1

def binary_search_interval_nested(arr, arr_denominator, a, b, denominator):
    l = 0
    r = len(arr) - 1
    common_a = a * arr_denominator
    common_b = b * arr_denominator
    while l <= r:
        mid = l + (r - l) // 2
        if (arr[mid-1] * denominator <= common_a) and \
                (common_b <= arr[mid] * denominator):
            return mid - 1
        elif arr[mid] * denominator <= common_a:
            l = mid + 1
        else:
            r = mid - 1
    return None

def orderm2(M):
    """Return the multiplicative of 2 modulo odd integer M."""
    output = subprocess.check_output([ORDERM2, '%d' % (M,)])
    result = output.split(b'\n')[-2]
    return int(result)

def binexp(a, b):
    """Return the preperiod and period digits of a/b."""
    r = subprocess.check_output([BINEXP, '%d' % (a,), '%d' % (b,)])
    parts = r.split(b'\n')
    bits = lambda s: tuple(map(int, s.split(b':')[1].strip().split(b',')[:-1]))
    prefix = () if len(parts) == 3 else bits(parts[0])
    suffix = bits(parts[0] if len(parts)==3 else parts[1])
    return (prefix, suffix)

def get_binary_expansion_length(M):
    """Return the length of prefix and suffix of binary expansion of 1/M."""
    if M % 2 == 1:
        k = orderm2(M)
        return (k, 0)
    Mp = M >> 1
    w = 1
    while (Mp % 2) == 0:
        w += 1
        Mp = Mp >> 1
    if Mp == 1:
        k = w
        l = k
    else:
        kp = orderm2(Mp)
        k = kp + w
        l = w
    return (k, l)

def encode_binary(x, width):
    """Convert integer x to binary with at least width digits."""
    assert isinstance(x, int)
    xb = bin(x)[2:]
    if width == 0:
        assert x == 0
        return ''
    else:
        assert len(xb) <= width
        pad = width  - len(xb)
        return '0' * pad + xb

def frac_to_bits(M, k, l):
    # Returns binary expansion of M / Zkl
    assert 0 <= M < get_Zkl(k, l) or (k == 1 and l == 0)
    if l == k:
        x = M
        y = 0
    elif l == 0:
        x = 0
        y = M
    else:
        Zb = pow(2, k-l) - 1
        x = M//Zb
        y = M - Zb * x
    a = encode_binary(x, l)
    s = encode_binary(y, k-l)
    b = a + s
    return [int(i) for i in b]

def frac_to_bits_dyadic(M, k):
    # Return binary expansion of M / 2**k
    bits = [0]*k
    for j in range(k):
        mask = 1 << ((k-1) - j)
        bits[j] = int((M & mask) > 0)
    return bits

def reduce_fractions(Ms, k, l):
    """Simplify (M/Zkl | M in Ms) to lowest terms."""
    Zkl = get_Zkl(k, l)
    assert sum(Ms) == get_Zkl(k, l)
    if any(M==Zkl for M in Ms):
        Ms_prime = [M//Zkl for M in Ms]
        k_prime = 1
        l_prime = 0
        return (Ms_prime, k_prime, l_prime)
    if l == 0:
        return (Ms, k, l)
    if all(M%2 == 0 for M in Ms):
        Ms_prime = [M//2 for M in Ms]
        return reduce_fractions(Ms_prime, k-1, l-1)
    if all(M == Ms[0] for M in Ms):
        remainder = Zkl / Ms[0]
        base = log2(remainder)
        assert remainder == int(remainder)
        assert base == int(base)
        k_prime = int(base)
        l_prime = k_prime
        Ms_prime = [1] * len(Ms)
        return Ms_prime, k_prime, l_prime
    return Ms, k, l

def bits_to_frac(bits, k, l):
    """Returns fraction M/Zkl, given bits in the kl number system."""
    Zkl = get_Zkl(k, l)
    Zb = get_Zb(k, l)
    prefix = bits[:l]
    suffix = bits[l:]
    int_prefix = bits_to_int(prefix) if prefix else 0
    int_suffix = bits_to_int(suffix) if suffix else 0
    numerator = Zb * int_prefix + int_suffix
    denominator = Zkl
    return (numerator, denominator)

def get_binary_expansion(a, b):
    """Return binary expansion of a/b (more efficient than frac_to_bits_rat)."""
    assert 0 <= a <= b
    if a == b:
        return (), (1,)
    if a == 0:
        return (0,), ()
    f = Fraction(a, b)
    bn = f.denominator
    k, l = get_binary_expansion_length(bn)
    Zkl = get_Zkl(k, l)
    ann = get_common_numerators(Zkl, [f])[0]
    result = frac_to_bits(ann, k, l)
    prefix = tuple(result[:l])
    suffix = tuple(result[l:])
    return prefix, suffix

def get_dyadic_approximation(probabilities):
    """Returning floating-point approximation of probabilities."""
    ratios = [float(x).as_integer_ratio() for x in probabilities]
    dyadics = [Fraction(r[0], r[1]) for r in ratios]
    # Normalize the distribution.
    underflow = 1 - sum(dyadics)
    if 0 < underflow:
        dyadics[0] += underflow
    elif underflow < 0:
        overflow = -underflow
        for i, d in enumerate(dyadics):
            if d > overflow:
                dyadics[i] -= overflow
                break
        else:
            assert False, 'Failed to normalize: %s' % (probabilities,)
    assert sum(dyadics) == 1
    # Expand to binary.
    expansions = [get_binary_expansion(a.numerator, a.denominator)[0]
        for a in dyadics]
    # Pad with zeros to fixed width.
    k = max(len(e) for e in expansions)
    return [e + (0,)*(k - len(e)) for e in expansions]
