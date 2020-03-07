#!/usr/bin/env python
#
# Copyright 2019 MIT Probabilistic Computing Project.
# Released under Apache 2.0; refer to LICENSE.txt

import os
import shutil
import subprocess

from fractions import Fraction

import matplotlib;
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from discrete_sampling.construct import construct_sample_alias
from discrete_sampling.construct import construct_sample_interval
from discrete_sampling.construct import construct_sample_ky_approx_encoding
from discrete_sampling.construct import construct_sample_ky_approx_matrix
from discrete_sampling.construct import construct_sample_ky_approx_matrix_cached
from discrete_sampling.construct import construct_sample_ky_encoding
from discrete_sampling.construct import construct_sample_ky_matrix
from discrete_sampling.construct import construct_sample_ky_matrix_cached
from discrete_sampling.construct import construct_sample_rejection_binary_search
from discrete_sampling.construct import construct_sample_rejection_encoding
from discrete_sampling.construct import construct_sample_rejection_hash_table
from discrete_sampling.construct import construct_sample_rejection_matrix
from discrete_sampling.construct import construct_sample_rejection_matrix_cached
from discrete_sampling.construct import construct_sample_rejection_uniform

from discrete_sampling.writeio import write_sample_alias
from discrete_sampling.writeio import write_sample_interval
from discrete_sampling.writeio import write_sample_ky_encoding
from discrete_sampling.writeio import write_sample_ky_matrix
from discrete_sampling.writeio import write_sample_ky_matrix_cached
from discrete_sampling.writeio import write_sample_rejection_binary_search
from discrete_sampling.writeio import write_sample_rejection_hash_table
from discrete_sampling.writeio import write_sample_rejection_uniform

from discrete_sampling.entropy import compute_entropy
from discrete_sampling.entropy import get_alpha_entropies
from discrete_sampling.utils import get_common_denominator
from discrete_sampling.utils import get_common_numerators
from discrete_sampling.utils import sample_dirichlet_multinomial_positive

from parallel_map import parallel_map
from parsable import parsable

def get_distribution_least_entropy(n, Z):
    assert n <= Z
    S = Z - n
    numerators = [1] * n
    numerators[0] += S
    assert sum(numerators) == Z
    return [Fraction(a, Z) for a in numerators]

def get_distribution_most_entropy(n, Z):
    assert n <= Z
    numerators = np.ones(n, dtype=int)
    S = Z - n
    numerators += S // n
    numerators[:(S%n)] += 1
    assert sum(numerators) == Z
    return [Fraction(int(a), Z) for a in numerators]

def get_distribution_entropy_bounds(n, Z):
    l = get_distribution_least_entropy(n, Z)
    h = get_distribution_most_entropy(n, Z)
    el = compute_entropy(l)
    eh = compute_entropy(h)
    assert el <= eh
    return (el, eh)

def write_samplers(args):
    (samplers, dirname, idx, p_target, entropy) = args
    structures = [
        ('ky.enc',
            construct_sample_ky_encoding,
            write_sample_ky_encoding),
        ('ky.mat',
            construct_sample_ky_matrix,
            write_sample_ky_matrix),
        ('ky.matc',
            construct_sample_ky_matrix_cached,
            write_sample_ky_matrix_cached),

        ('ky.approx.enc',
            construct_sample_ky_approx_encoding,
            write_sample_ky_encoding),
        ('ky.approx.mat',
            construct_sample_ky_approx_matrix,
            write_sample_ky_matrix),
        ('ky.approx.matc',
            construct_sample_ky_approx_matrix_cached,
            write_sample_ky_matrix_cached),

        ('rej.uniform',
            construct_sample_rejection_uniform,
            write_sample_rejection_uniform),
        ('rej.table',
            construct_sample_rejection_hash_table,
            write_sample_rejection_hash_table),
        ('rej.binary',
            construct_sample_rejection_binary_search,
            write_sample_rejection_binary_search),

        ('rej.enc',
            construct_sample_rejection_encoding,
            write_sample_ky_encoding),
        ('rej.mat',
            construct_sample_rejection_matrix,
            write_sample_ky_matrix),
        ('rej.matc',
            construct_sample_rejection_matrix_cached,
            write_sample_ky_matrix_cached),

        ('interval',
            construct_sample_interval,
            write_sample_interval),
        ('alias.exact',
            construct_sample_alias,
            write_sample_alias),
    ]

    for suffix, f_construct, f_write in structures:
        if samplers and suffix not in samplers:
            continue
        fpath = os.path.join(dirname, 'd.%05d.%s' % (idx, suffix))
        struc = f_construct(p_target)
        f_write(*struc, fpath)
        print(fpath)

    fname_dist = 'd.%05d.dist' % (idx,)
    fpath_dist = os.path.join(dirname, fname_dist)
    with open(fpath_dist, 'w') as f:
        n = len(p_target)
        Z = get_common_denominator(p_target)
        Ms = get_common_numerators(Z, p_target)
        f.write('%d\n' % (Z,))
        f.write('%d %s\n' % (n, ' '.join(map(str, Ms))))
        f.write('%1.5f\n' % (entropy,))
        print(fpath_dist)

    # Make soft links to dist file for non ANCI C baselines.
    for suffix in ['alias.boost', 'inversion.std', 'alias.gsl']:
        if samplers and suffix not in samplers:
            continue
        fname_suffix = fname_dist.replace('.dist', '.%s' % (suffix,))
        fpath = os.path.join(dirname, fname_suffix)
        subprocess.check_output(['ln', fpath_dist, fpath])
        print(fpath)

@parsable
def generate_distributions(N=10, Z=-1, seed=1, samplers='', thin=1,
        force=None, offset=0):
    """Generate distributions and save to disk."""
    Z =  2*N**2 + 1 if Z == - 1 else int(Z)
    dirname = 'dists.%d.%d.%d' % (N, Z, seed,)
    samplers = samplers.replace('\'', '').split(' ') if samplers != '' else []
    if force and os.path.exists(dirname):
        shutil.rmtree(dirname)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    # XXX
    import sys; sys.setrecursionlimit(100000)

    rng = np.random.RandomState(seed)
    alphas = get_alpha_entropies(N, maxalpha=5, numalpha=1000, parallel=True)
    distributions = [
        sample_dirichlet_multinomial_positive(a, N, Z, rng)
        # for a in alphas
        for a in alphas[offset::thin]
    ]

    low, high = get_distribution_entropy_bounds(N, Z)
    entropies = parallel_map(compute_entropy, distributions)
    idxs = np.argsort(entropies)
    args = [
        (samplers, dirname, i, distributions[idx], entropies[idx])
        for i, idx in enumerate(idxs)
    ]
    parallel_map(write_samplers, args)
    # list(map(write_samplers, args))

if __name__ == '__main__':
    parsable()
