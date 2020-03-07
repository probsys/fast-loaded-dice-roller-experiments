/*
  Name:     sample.h
  Purpose:  Exact samplers for discrete probability distributions.
  Author:   F. A. Saad
  Copyright (C) 2020 Feras A. Saad, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#ifndef SAMPLE_H
#define SAMPLE_H

#include "sstructs.h"

int sample_ky_encoding(struct sample_ky_encoding_s *x);
int sample_ky_matrix(struct sample_ky_matrix_s *x);
int sample_ky_matrix_cached(struct sample_ky_matrix_cached_s *x);

int sample_fdr(struct sample_fdr_s *x);
int sample_inversion_bernoulli(struct sample_inversion_bernoulli_s *x);

int sample_rejection_uniform(struct sample_rejection_uniform_s *x);
int sample_rejection_hash_table(struct sample_rejection_hash_table_s *x);
int sample_rejection_binary_search(struct sample_rejection_binary_search_s *x);

int sample_rejection_encoding(struct sample_ky_encoding_s *x);
int sample_rejection_matrix(struct sample_ky_matrix_s *x);
int sample_rejection_matrix_cached(struct sample_ky_matrix_cached_s *x);

int sample_interval(struct sample_interval_s *x);
int sample_alias_gsl(struct sample_alias_gsl_s *x);
int sample_alias_exact(struct sample_alias_exact_s *x);
#endif
