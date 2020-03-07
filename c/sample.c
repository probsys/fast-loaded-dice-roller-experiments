/*
  Name:     sample.c
  Purpose:  Exact samplers for discrete probability distributions.
  Author:   F. A. Saad and C. E. Freer
  Copyright (C) 2020 Feras A. Saad and C. E. Freer, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#include <stdbool.h>
#include <stdlib.h>

#include "flip.h"
#include "sample.h"
#include "sstructs.h"
#include "utils.h"

int sample_ky_encoding(struct sample_ky_encoding_s *x) {

    if (x->encoding.length == 1) {
        return 1;
    }

    int *enc = x->encoding.a;
    int c = 0;
    while (true) {
        int b = flip();
        c = enc[c+b];
        if (enc[c] < 0) {
            return -enc[c];
        }
    }
}

int sample_ky_matrix(struct sample_ky_matrix_s *x) {
    if (x->P.nrows == 1) {
        return 1;
    }

    int **P = x->P.P;
    int c = 0;
    int d = 0;

    while (true) {
        int b = flip();
        d = 2 * d + (1-b);
        for (int r = 0; r < x->P.nrows; r++) {
            d = d - P[r][c];
            if (d == - 1) {
                return r + 1;
            }
        }
        if (c == x->k - 1) {
            c = x->l;
        } else {
            c = c + 1;
        }
    }
}

int sample_ky_matrix_cached(struct sample_ky_matrix_cached_s *x) {
    if (x->T.nrows == 1) {
        return 1;
    }

    int **T = x->T.P;
    int *h = x->h.a;

    int c = 0;
    int d = 0;

    while (true) {
        int b = flip();
        d = 2 * d + (1-b);
        if (d < h[c]) {
            return T[d][c] + 1;
        }
        d = d - h[c];
        if (c == x->k - 1) {
            c = x->l;
        } else {
            c = c + 1;
        }
    }
}

int sample_fdr(struct sample_fdr_s *x) {
    int v = 1;
    int c = 0;

    while (true) {
        int b = flip();
        v = v << 1;
        c = (c << 1) + b;
        if (x->n <= v) {
            if (c < x->n) {
                return c + 1;
            } else {
                v = v - x->n;
                c = c - x->n;
            }
        }
    }
}

int sample_inversion_bernoulli(struct sample_inversion_bernoulli_s *x) {
    int v = x->a;
    int M = x->M;
    int y;

    while (true) {
        v = 2*v;
        if (M <= v) {
            v = v - M;
            y = 1;
        } else {
            y = 0;
        }
        int b = flip();
        if (b == 1) {
            return y;
        }
    }
}

int sample_rejection_uniform(struct sample_rejection_uniform_s *x) {
    struct sample_fdr_s n = {.n = x->n};
    while (true) {
        int j = sample_fdr(&n);
        int b = sample_inversion_bernoulli(&(x->ratios[j-1]));
        if (b == 1) {
            return j;
        }
    }
}

int sample_rejection_hash_table(struct sample_rejection_hash_table_s *x) {
    int *T = x->T.a;
    while (true) {
        int W = randint(x->k);
        if (W < x->Z) {
            return T[W];
        }
    }
}

int sample_rejection_binary_search(struct sample_rejection_binary_search_s *x) {
    while (true) {
        int W = randint(x->k);
        if (W < x->Z) {
            int j = binary_search_interval(x->cdf.a, x->cdf.length, W);
            return j + 1;
        }
    }

}

int sample_rejection_encoding(struct sample_ky_encoding_s *x) {
    int *enc = x->encoding.a;
    int n = x->n;
    int c = 0; int s;
    while (true) {
        int b = flip();
        c = enc[c+b];
        s = -enc[c];
        if (s > 0) {
            if ( s < n ) {
                return s;
            } else {
                c = 0;
            }
        }
    }
}

int sample_rejection_matrix(struct sample_ky_matrix_s *x) {
    int n = x->P.nrows;
    while (true) {
        int s = sample_ky_matrix(x);
        if (s < n) {
            return s;
        }
    }
}

int sample_rejection_matrix_cached(struct sample_ky_matrix_cached_s *x) {

    int **T = x->T.P;
    int *h = x->h.a;

    int n = x->T.nrows;
    int c = 0;
    int d = 0;

    while (true) {
        int b = flip();
        d = 2 * d + (1-b);
        if (d < h[c]) {
            int s = T[d][c];
            if (s < n-1) {
                return s + 1;
            } else {
                d = 0;
                c = 0;
            }
        } else {
            d = d - h[c];
            c = c + 1;
        }
    }
}

int sample_interval(struct sample_interval_s *x) {
    int alpha = 0;
    int beta = 1;
    int alpha_prev = 0;
    int denominator = 1;
    int location = -1;
    int b = 0;

    while (location == -1) {
        b = flip();

        alpha_prev = alpha;
        alpha = 2 * alpha + (beta - alpha) * b;
        beta = 2 * alpha_prev + (beta - alpha_prev) * (b+1);

        if ((alpha % 2 == 0) && (beta % 2 == 0)) {
            alpha /= 2;
            beta /= 2;
        } else {
            denominator *= 2;
        }

        location = binary_search_interval_nested(
            x->cdf.a, x->Z, x->cdf.length, alpha, beta, denominator);
    }

    return location;
}

int sample_alias_gsl(struct sample_alias_gsl_s *x) {
    int draw = gsl_ran_discrete(x->prng, x->distribution);
    return draw;
}

int sample_alias_exact(struct sample_alias_exact_s *x) {
    struct sample_fdr_s xn = {.n = x->n};
    int n = sample_fdr(&xn);
    int b = sample_inversion_bernoulli(&(x->ratios[n-1]));
    if (b == 1) {
        return n;
    } else {
        return x->j.a[n-1] + 1;
    }
}
