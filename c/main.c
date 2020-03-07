/*
  Name:     main.c
  Purpose:  Command line interface for sampling algorithms.
  Author:   F. A. Saad and C. E. Freer
  Copyright (C) 2020 Feras A. Saad and C. E. Freer, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "flip.h"
#include "readio.h"
#include "sample.h"
#include "sstructs.h"

#include "macros.c"

int main(int argc, char **argv) {
    // Read command line arguments.
    if (argc != 5) {
        printf("usage: %s seed steps sampler path\n", argv[0]);
        exit(0);
    }
    int seed = atoi(argv[1]);
    int steps = atoi(argv[2]);
    char *sampler = argv[3];
    char *path = argv[4];

    printf("%d %d %s %s\n", seed, steps, sampler, path);
    srand(seed);

    int x = 0;
    clock_t t;
    READ_SAMPLE_TIME("ky.enc",
        sampler,
        sample_ky_encoding_s,
        read_sample_ky_encoding,
        sample_ky_encoding,
        free_sample_ky_encoding_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("ky.mat",
        sampler,
        sample_ky_matrix_s,
        read_sample_ky_matrix,
        sample_ky_matrix,
        free_sample_ky_matrix_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("ky.matc",
        sampler,
        sample_ky_matrix_cached_s,
        read_sample_ky_matrix_cached,
        sample_ky_matrix_cached,
        free_sample_ky_matrix_cached_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("ky.approx.enc",
        sampler,
        sample_ky_encoding_s,
        read_sample_ky_encoding,
        sample_ky_encoding,
        free_sample_ky_encoding_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("ky.approx.mat",
        sampler,
        sample_ky_matrix_s,
        read_sample_ky_matrix,
        sample_ky_matrix,
        free_sample_ky_matrix_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("ky.approx.matc",
        sampler,
        sample_ky_matrix_cached_s,
        read_sample_ky_matrix_cached,
        sample_ky_matrix_cached,
        free_sample_ky_matrix_cached_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("fdr",
        sampler,
        sample_fdr_s,
        read_sample_fdr,
        sample_fdr,
        free_sample_fdr_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("inv.bern",
        sampler,
        sample_inversion_bernoulli_s,
        read_sample_inversion_bernoulli,
        sample_inversion_bernoulli,
        free_sample_inversion_bernoulli_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("rej.uniform",
        sampler,
        sample_rejection_uniform_s,
        read_sample_rejection_uniform,
        sample_rejection_uniform,
        free_sample_rejection_uniform_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("rej.table",
        sampler,
        sample_rejection_hash_table_s,
        read_sample_rejection_hash_table,
        sample_rejection_hash_table,
        free_sample_rejection_hash_table_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("rej.binary",
        sampler,
        sample_rejection_binary_search_s,
        read_sample_rejection_binary_search,
        sample_rejection_binary_search,
        free_sample_rejection_binary_search_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("rej.enc",
        sampler,
        sample_ky_encoding_s,
        read_sample_ky_encoding,
        sample_rejection_encoding,
        free_sample_ky_encoding_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("rej.mat",
        sampler,
        sample_ky_matrix_s,
        read_sample_ky_matrix,
        sample_rejection_matrix,
        free_sample_ky_matrix_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("rej.matc",
        sampler,
        sample_ky_matrix_cached_s,
        read_sample_ky_matrix_cached,
        sample_rejection_matrix_cached,
        free_sample_ky_matrix_cached_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("interval",
        sampler,
        sample_interval_s,
        read_sample_interval,
        sample_interval,
        free_sample_interval_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("alias.exact",
        sampler,
        sample_alias_exact_s,
        read_sample_alias_exact,
        sample_alias_exact,
        free_sample_alias_exact_s,
        path, steps, t, x)
    else READ_SAMPLE_TIME("alias.gsl",
        sampler,
        sample_alias_gsl_s,
        read_sample_alias_gsl,
        sample_alias_gsl,
        free_sample_alias_gsl_s,
        path, steps, t, x)
    else {
        printf("Unknown sampler: %s\n", sampler);
        exit(1);
    }

    double e = ((double)t) / CLOCKS_PER_SEC;
    printf("%s %1.5f %ld\n", sampler, e, NUM_RNG_CALLS);

    return 0;
}
