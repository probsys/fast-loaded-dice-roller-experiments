/*
  Name:     readio.c
  Purpose:  Loading sampling data structures from disk..
  Author:   F. A. Saad
  Copyright (C) 2020 Feras A. Saad, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#include <stdlib.h>

#include "readio.h"
#include "sstructs.h"

// Load matrix from file.
struct matrix_s load_matrix(FILE *fp) {

    struct matrix_s mat;
    fscanf(fp, "%d %d", &(mat.nrows), &(mat.ncols));

    mat.P = (int **) calloc(mat.nrows, sizeof(int **));
    for(int r = 0; r < mat.nrows; ++r) {
        mat.P[r] = (int *) calloc(mat.ncols, sizeof(int));
        for (int c = 0; c < mat.ncols; ++c){
            fscanf(fp, "%d", &(mat.P[r][c]));
        }
    }

    return mat;
}

void free_matrix_s (struct matrix_s x) {
    for (int i = 0; i < x.nrows; i++) {
        free(x.P[i]);
    }
    free(x.P);
}

// Load matrix from file.
struct array_s load_array(FILE *fp) {

    struct array_s arr;
    fscanf(fp, "%d", &(arr.length));

    arr.a = (int *) calloc(arr.length, sizeof(int));
    for (int i = 0; i < arr.length; i++) {
        fscanf(fp, "%d", &arr.a[i]);
    }

    return arr;
}

void free_array_s (struct array_s x) {
    free(x.a);
}

// Load sample_ky_encoding data structure from file path.
struct sample_ky_encoding_s read_sample_ky_encoding(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_ky_encoding_s x;
    fscanf(fp, "%d %d", &(x.n), &(x.k));
    x.encoding = load_array(fp);

    fclose(fp);
    return x;
}

void free_sample_ky_encoding_s (struct sample_ky_encoding_s x) {
    free_array_s(x.encoding);
}

// Load sample_ky_matrix data structure from file path.
struct sample_ky_matrix_s read_sample_ky_matrix(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_ky_matrix_s x;
    fscanf(fp, "%d %d", &(x.k), &(x.l));
    x.P = load_matrix(fp);

    fclose(fp);
    return x;
}

void free_sample_ky_matrix_s (struct sample_ky_matrix_s x) {
    free_matrix_s(x.P);
}

// Load sample_ky_matrix_cached data structure from file path.
struct sample_ky_matrix_cached_s read_sample_ky_matrix_cached(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_ky_matrix_cached_s x;
    fscanf(fp, "%d %d", &(x.k), &(x.l));
    x.h = load_array(fp);
    x.T = load_matrix(fp);

    fclose(fp);
    return x;
}

void free_sample_ky_matrix_cached_s (struct sample_ky_matrix_cached_s x) {
    free_array_s(x.h);
    free_matrix_s(x.T);
}

// Load sample_fdr data structure from file path.
struct sample_fdr_s read_sample_fdr(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_fdr_s x;
    fscanf(fp, "%d", &(x.n));

    fclose(fp);
    return x;
}

void free_sample_fdr_s(struct sample_fdr_s x) {
}

// Load sample_bernoulli data structure from file path.
struct sample_inversion_bernoulli_s read_sample_inversion_bernoulli(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_inversion_bernoulli_s x;
    fscanf(fp, "%d %d", &(x.a), &(x.M));

    fclose(fp);
    return x;
}

void free_sample_inversion_bernoulli_s(struct sample_inversion_bernoulli_s x) {
}

// Load sample_rejection_uniform data structure from file path.
struct sample_rejection_uniform_s read_sample_rejection_uniform(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_rejection_uniform_s x;
    fscanf(fp, "%d %d", &(x.n), &(x.M));
    x.Ms = load_array(fp);

    x.ratios = (struct sample_inversion_bernoulli_s*)
        calloc(x.n, sizeof(struct sample_inversion_bernoulli_s));

    for (int i = 0; i < x.n; i++) {
        struct sample_inversion_bernoulli_s y = {.a = x.Ms.a[i], .M = x.M};
        x.ratios[i] = y;
    }

    fclose(fp);
    return x;
}

void free_sample_rejection_uniform_s (struct sample_rejection_uniform_s x) {
    free_array_s(x.Ms);
    for (int i = 0; i < x.n; i ++) {
        free_sample_inversion_bernoulli_s(x.ratios[i]);
    }
}

// Load sample_rejection_hash_table data structure from file path.
struct sample_rejection_hash_table_s read_sample_rejection_hash_table(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_rejection_hash_table_s x;
    fscanf(fp, "%d %d", &(x.k), &(x.Z));
    x.T = load_array(fp);

    fclose(fp);
    return x;
}

void free_sample_rejection_hash_table_s(
        struct sample_rejection_hash_table_s x) {
    free_array_s(x.T);
}

// Load sample_rejection_binary_search data structure from file path.
struct sample_rejection_binary_search_s read_sample_rejection_binary_search(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_rejection_binary_search_s x;
    fscanf(fp, "%d %d", &(x.k), &(x.Z));
    x.cdf = load_array(fp);

    fclose(fp);
    return x;
}

void free_sample_rejection_binary_search_s(
        struct sample_rejection_binary_search_s x) {
    free_array_s(x.cdf);
}

// Load sample_interval data structure from file path.
struct sample_interval_s read_sample_interval(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_interval_s x;
    fscanf(fp, "%d %d", &(x.k), &(x.Z));
    x.cdf = load_array(fp);

    fclose(fp);
    return x;
}

void free_sample_interval_s(struct sample_interval_s x) {
    free_array_s(x.cdf);
}


// Load sample_alias_gsl data structure from file path.
struct sample_alias_gsl_s read_sample_alias_gsl(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_alias_gsl_s x;
    int Z;
    fscanf(fp, "%d", &Z);
    struct array_s numerators = load_array(fp);
    fclose(fp);

    x.distribution = gsl_ran_discrete_preproc(
        numerators.length, (double*)numerators.a);

    const gsl_rng_type *rT = gsl_rng_default;
    x.prng = gsl_rng_alloc(rT);

    return x;
}

void free_sample_alias_gsl_s (struct sample_alias_gsl_s x) {
    gsl_ran_discrete_free(x.distribution);
    gsl_rng_free(x.prng);
}

// Load sample_alias_exact data structure from file path.
// Load sample_rejection_uniform data structure from file path.
struct sample_alias_exact_s read_sample_alias_exact(char *fname) {
    FILE *fp = fopen(fname, "r");

    struct sample_alias_exact_s x;
    fscanf(fp, "%d", &(x.n));
    struct array_s qs = load_array(fp);
    struct array_s Ms = load_array(fp);
    x.j = load_array(fp);

    x.ratios = (struct sample_inversion_bernoulli_s*)
        calloc(x.n, sizeof(struct sample_inversion_bernoulli_s));

    for (int i = 0; i < x.n; i++) {
        struct sample_inversion_bernoulli_s y = {.a = qs.a[i], .M = Ms.a[i]};
        x.ratios[i] = y;
    }

    fclose(fp);

    free_array_s(qs);
    free_array_s(Ms);

    return x;
}

void free_sample_alias_exact_s (struct sample_alias_exact_s x) {
    free_array_s(x.j);
    for (int i = 0; i < x.n; i ++) {
        free_sample_inversion_bernoulli_s(x.ratios[i]);
    }
}
