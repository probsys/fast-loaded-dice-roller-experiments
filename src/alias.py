# Released under Apache 2.0; refer to LICENSE.txt

"""Implementation of Alias Method

    An Efficient Method for Generating Discrete Random Variables with General
    Distributions. ACM Transactions on Mathematical Software (TOMS). Volume 3
    Issue 3, Sept. 1977 Pages 253-256.
    https://dl.acm.org/citation.cfm?id=355749

    Algorithm from Devroye III.4
"""

def alias_preprocess(p_target):
    K = len(p_target)
    greater = set()
    smaller = set()
    q = [0] * K
    j = [0] * K
    for l in range(K):
        q[l] = K * p_target[l]
        if q[l] < 1:
            smaller.add(l)
        else:
            greater.add(l)
    while smaller:
        k = greater.pop()
        l = smaller.pop()
        j[l] = k
        q[k] = q[k] - (1 - q[l])
        if q[k] < 1:
            smaller.add(k)
        else:
            greater.add(k)
    return (K, q, j)

def alias_sample(K, q, j):
    # Inexact version, see sample.py for exact.
    from random import random
    U = random()
    x = int(K*U)
    if random() < q[x]:
        return x
    return j[x]
