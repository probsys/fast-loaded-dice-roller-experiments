# Released under Apache 2.0; refer to LICENSE.txt

"""Implementation of limited precision algorithm, adapted from Algorithm 1 of:

    Uyematsu, Tomohiko, and Yuan Li. "Two algorithms for random number
    generation implemented by using arithmetic of limited precision." IEICE
    TRANSACTIONS on Fundamentals of Electronics, Communications and Computer
    Sciences 86.10 (2003): 2542-2551.
    http://www.it.ce.titech.ac.jp/uyematsu/papers/ul03.pdf

    The implementation only produces a single sample as opposed to a stream of
    samples, as given by the implementation in Algorithm 1 of Uyematsu and Li
    (the latter is slightly faster due by constant factors, but the entropy
    consumption in either case is the same).
"""

from discrete_sampling.utils import cumsum

def preprocess_interval(p_target, k):
    """Compute intervals of the target distribution for interval sampling."""
    N = len(p_target)
    u = 2**(k-1)
    Q = cumsum(p_target)
    F = [0] + [int(.5 + u*Q[i]) for i in range(N)]
    J = [(int(.5 + F[i]), int(.5 + F[i+1])) for i in range(N)]
    return J

def sample_interval_no_preprocess(p_target, k, J, bitstream):
    # Implementation assumes cached J, for benchmarking.
    u = 2**(k-1)
    R = 2**(k-1)
    N = len(p_target)
    s = ()
    alpha = {s: 0}
    beta = {s: u}
    I = {s: (alpha[s], beta[s])}
    nflips = 0
    while True:
        nflips += 1
        a = 1 + next(bitstream)
        sa = s + (a,)
        alpha[sa] = alpha[s] + (a-1)*R/2
        beta[sa] = alpha[s] + a*R/2
        I[sa] = (alpha[sa], beta[sa])
        R = R/2
        # TODO: Use binary search.
        for b in range(N):
            if J[b][0] <= alpha[sa] <= beta[sa] <= J[b][1]:
                return b
        s = sa
        if nflips == k-1:
            assert False, 'Fatal error: too many bits consumed.'

def sample_interval(p_target, k, bitstream):
    """Return sample from p_target using k-bit precision interval sampling."""
    J = preprocess_interval(p_target, k)
    return sample_interval_no_preprocess(p_target, k, J, bitstream)
