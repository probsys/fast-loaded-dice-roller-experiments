# Released under Apache 2.0; refer to LICENSE.txt

def sample_ky_encoding(enc, bitstream):
    if len(enc) == 1:
        assert enc[0] == -1
        return 1

    c = 0
    while True:
        b = next(bitstream)
        c = enc[c + b]
        if enc[c] < 0:
            return -enc[c]

def sample_ky_matrix(P, k, l, bitstream):
    if len(P) == 1:
        assert P[0][0] == 1
        return 1

    N = len(P)
    assert len(P[0]) == k
    assert 0 <= l <= k
    d = 0
    c = 0
    while True:
        b = next(bitstream)
        d = 2*d + (1 - b)
        for r in range(N):
            d = d - P[r][c]
            if d == - 1:
                return r + 1
        if c == k - 1:
            assert l < k-1
            c = l
        else:
            c = c + 1

def sample_ky_matrix_cached(k, l, h, T, bitstream):
    if len(T) == 1:
        return 1
    assert len(T[0]) == k
    assert 0 <= l <= k
    d = 0
    c = 0
    while True:
        b = next(bitstream)
        d = 2*d + (1 - b)
        if d < h[c]:
            return T[d][c] + 1
        d = d - h[c]
        if c == k - 1:
            assert l < k-1
            c = l
        else:
            c = c + 1

def sample_fdr(n, bitstream):
    # https://arxiv.org/pdf/1304.1916.pdf
    v = 1
    c = 0
    while True:
        b = next(bitstream)
        v = v << 1
        c = (c << 1) + b
        if n <= v:
            if c < n:
                return c + 1
            else:
                v = v - n
                c = c - n

def sample_inversion_bernoulli(a, M, bitstream):
    v = a
    while True:
        v = 2*v
        if M <= v:
            v = v - M
            x = 1
        else:
            x = 0
        b = next(bitstream)
        if b:
            return x

def sample_rejection_uniform(Ms, M, n, bitstream):
    while True:
        j = sample_fdr(n, bitstream)
        idx = j - 1
        b = sample_inversion_bernoulli(Ms[idx], M, bitstream)
        if b == 1:
            return j

def sample_rejection_hash_table(T, Z, k, bitstream):
    from .utils import randint
    while True:
        W = randint(k, bitstream)
        if W < Z:
            return T[W]

def sample_rejection_binary_search(cdf, Z, k, bitstream):
    from .utils import randint
    from .utils import binary_search_interval
    while True:
        W = randint(k, bitstream)
        if W < Z:
            j = binary_search_interval(cdf, W)
            return j + 1

def sample_rejection_encoding(enc, n, bitstream):
    while True:
        s = sample_ky_encoding(enc, bitstream)
        if s < n:
            return s

def sample_rejection_matrix(P, k, l, bitstream):
    n = len(P)
    while True:
        s = sample_ky_matrix(P, k, l, bitstream)
        if s < n:
            return s

def sample_rejection_matrix_cached(k, l, h, T, bitstream):
    n = len(T)
    while True:
        s = sample_ky_matrix_cached(k, l, h, T, bitstream)
        if s < n:
            return s

def sample_interval(cdf, Z, bitstream):
    from .utils import binary_search_interval_nested
    alpha = 0
    beta = 1
    denominator = 1
    location = None

    while location is None:
        b = next(bitstream)
        alpha_prev = alpha
        alpha = 2 * alpha + (beta - alpha) * b
        beta = 2 * alpha_prev + (beta - alpha_prev) * (b+1)

        if (alpha % 2 == 0) and (beta % 2 == 0):
            alpha //= 2
            beta //= 2
        else:
            denominator *= 2

        location = binary_search_interval_nested(
            cdf, Z, alpha, beta, denominator)

    return location

def sample_alias(n, qs, Ms, j, bitstream):
    n = sample_fdr(n, bitstream)
    x = sample_inversion_bernoulli(qs[n-1], Ms[n-1], bitstream)
    if x == 1:
        return n
    return j[n-1] + 1
