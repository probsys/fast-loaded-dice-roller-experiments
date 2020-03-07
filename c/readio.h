/*
  Name:     readio.h
  Purpose:  Loading sampling data structures from disk..
  Author:   F. A. Saad
  Copyright (C) 2020 Feras A. Saad, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#ifndef READIO_H
#define READIO_H

#include <stdio.h>
#include "sstructs.h"

struct matrix_s load_matrix(FILE *fp);
struct array_s load_array(FILE *fp);
struct sample_ky_encoding_s read_sample_ky_encoding(char *fname);
struct sample_ky_matrix_s read_sample_ky_matrix(char *fname);
struct sample_ky_matrix_cached_s read_sample_ky_matrix_cached(char *fname);
struct sample_fdr_s read_sample_fdr(char *fname);
struct sample_inversion_bernoulli_s read_sample_inversion_bernoulli(char *fname);
struct sample_rejection_uniform_s read_sample_rejection_uniform(char *fname);
struct sample_rejection_hash_table_s read_sample_rejection_hash_table(char *fname);
struct sample_rejection_binary_search_s read_sample_rejection_binary_search(char *fname);
struct sample_interval_s read_sample_interval(char *fname);
struct sample_alias_gsl_s read_sample_alias_gsl(char *fname);
struct sample_alias_exact_s read_sample_alias_exact(char *fname);

void free_matrix_s(struct matrix_s x);
void free_array_s(struct array_s x);
void free_sample_ky_encoding_s(struct sample_ky_encoding_s x);
void free_sample_ky_matrix_s(struct sample_ky_matrix_s x);
void free_sample_ky_matrix_cached_s(struct sample_ky_matrix_cached_s x);
void free_sample_fdr_s(struct sample_fdr_s x);
void free_sample_inversion_bernoulli_s(struct sample_inversion_bernoulli_s x);
void free_sample_rejection_uniform_s(struct sample_rejection_uniform_s x);
void free_sample_rejection_hash_table_s(struct sample_rejection_hash_table_s x);
void free_sample_rejection_binary_search_s(struct sample_rejection_binary_search_s x);
void free_sample_interval_s(struct sample_interval_s x);
void free_sample_alias_gsl_s(struct sample_alias_gsl_s x);
void free_sample_alias_exact_s(struct sample_alias_exact_s x);

#endif
