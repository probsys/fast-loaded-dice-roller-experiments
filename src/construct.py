# Released under Apache 2.0; refer to LICENSE.txt

from math import ceil
from math import log2

from discrete_sampling.matrix import make_ddg_matrix
from discrete_sampling.matrix import make_hamming_matrix
from discrete_sampling.matrix import make_hamming_vector

from discrete_sampling.rejection import get_rejection_Ms_k
from discrete_sampling.rejection import get_rejection_cdf
from discrete_sampling.rejection import get_rejection_precision
from discrete_sampling.rejection import get_rejection_table

from discrete_sampling.alias import alias_preprocess

from discrete_sampling.utils import get_Zkl
from discrete_sampling.utils import get_binary_expansion_length
from discrete_sampling.utils import get_common_denominator
from discrete_sampling.utils import get_common_numerators
from discrete_sampling.utils import get_dyadic_approximation

from discrete_sampling.packing import pack_tree
from discrete_sampling.tree import make_ddg_tree

def construct_sample_ky_encoding(p_target):
    P, k, l = construct_sample_ky_matrix(p_target)
    root = make_ddg_tree(P, k, l)
    enc = {}
    pack_tree(enc, root, 0)
    n = len(P)
    return [enc[i] for i in range(len(enc))], n, k

def construct_sample_ky_matrix(p_target):
    Z = get_common_denominator(p_target)
    k, l = get_binary_expansion_length(Z)
    Zkl = get_Zkl(k, l)
    Ms = get_common_numerators(Zkl, p_target)
    P, kp, lp = make_ddg_matrix(Ms, k, l)
    return P, kp, lp

def construct_sample_ky_matrix_cached(p_target):
    P, k, l = construct_sample_ky_matrix(p_target)
    h = make_hamming_vector(P)
    T = make_hamming_matrix(P)
    return k, l, h, T

def construct_sample_ky_approx_encoding(p_target):
    P, k, l = construct_sample_ky_approx_matrix(p_target)
    root = make_ddg_tree(P, k, l)
    enc = {}
    pack_tree(enc, root, 0)
    n = len(P)
    return [enc[i] for i in range(len(enc))], n, k

def construct_sample_ky_approx_matrix(p_target):
    P = get_dyadic_approximation(p_target)
    kp = len(P[0])
    lp = len(P[0])
    return (P, kp, lp)

def construct_sample_ky_approx_matrix_cached(p_target):
    P, k, l = construct_sample_ky_approx_matrix(p_target)
    h = make_hamming_vector(P)
    T = make_hamming_matrix(P)
    return k, l, h, T

def construct_sample_fdr(n):
    return n

def construct_sample_bernoulli(a, n):
    return a, n

def construct_sample_rejection_uniform(p_target):
    Z = get_common_denominator(p_target)
    Ms = get_common_numerators(Z, p_target)
    M = max(Ms)
    n = len(p_target)
    return Ms, M, n

def construct_sample_rejection_hash_table(p_target):
    Z = get_common_denominator(p_target)
    k = get_rejection_precision(p_target)
    T = get_rejection_table(p_target)
    return T, Z, k

def construct_sample_rejection_binary_search(p_target):
    cdf = get_rejection_cdf(p_target)
    Z = get_common_denominator(p_target)
    k = get_rejection_precision(p_target)
    return cdf, Z, k

def construct_sample_rejection_encoding(p_target):
    P, k, l = construct_sample_rejection_matrix(p_target)
    root = make_ddg_tree(P, k, l)
    enc = {}
    pack_tree(enc, root, 0)
    encoding = [enc[i] for i in range(len(enc))]
    n = len(P)
    return encoding, n, k

def construct_sample_rejection_matrix(p_target):
    Ms, k = get_rejection_Ms_k(p_target)
    P, kp, lp = make_ddg_matrix(Ms, k, k)
    return P, kp, lp

def construct_sample_rejection_matrix_cached(p_target):
    P, k, l = construct_sample_rejection_matrix(p_target)
    h = make_hamming_vector(P)
    T = make_hamming_matrix(P)
    return k, l, h, T

def construct_sample_interval(p_target):
    n = len(p_target)
    cdf = get_rejection_cdf(p_target)
    Z = get_common_denominator(p_target)
    k = ceil(log2(n))
    return cdf, Z, k

def construct_sample_alias(p_target):
    (n, q, j) = alias_preprocess(p_target)
    qs = [x.numerator for x in q]
    Ms = [x.denominator for x in q]
    return n, qs, Ms, j
