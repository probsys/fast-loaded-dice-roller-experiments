/*
  Name:     preprocess.c
  Purpose:  Preprocessing algorithm for FLDR.
  Author:   F. A. Saad
  Copyright (C) 2020 Feras A. Saad, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#include <stdbool.h>
#include <stdio.h>
#include <time.h>

#include <gsl/gsl_randist.h>

#include "readio.h"
#include "sstructs.h"

int ceil_log2(unsigned long long x) {
  static const unsigned long long t[6] = {
    0xFFFFFFFF00000000ull,
    0x00000000FFFF0000ull,
    0x000000000000FF00ull,
    0x00000000000000F0ull,
    0x000000000000000Cull,
    0x0000000000000002ull
  };

  int y = (((x & (x - 1)) == 0) ? 0 : 1);
  int j = 32;
  int i;

  for (i = 0; i < 6; i++) {
    int k = (((x & t[i]) == 0) ? 0 : j);
    y += k;
    x >>= k;
    j >>= 1;
  }

  return y;
}

int preprocess_fldr(struct array_s x, int m) {
    int k = ceil_log2(m);
    int r = (1 << k) - m;
    int n = x.length + 1;

    int *h = calloc(k, sizeof(int));
    int *H = calloc(n*k, sizeof(int));

    int d;
    for(int j = 0; j < k; j++) {
        d = 0;
        for (int i = 0 ; i < x.length; i++) {
            bool w = (x.a[i] >> ((k-1) -j)) & 1;
            h[j] += w;
            if (w) {
                H[d*k + j] = i;
                d += 1;
            }
        }
        // Reject outcome.
        bool w = (w >> ((k-1) -j)) & 1;
        h[j] += w;
        if (w) {
            H[d*k + j] = n;
            d += 1;
        }
    }
    return d;
}

void preprocess_alias_gsl(struct array_s x, int m) {
    gsl_ran_discrete_preproc(x.length, (double*)x.a);
}

int main(int argc, char **argv) {
    // Read command line arguments.
    if (argc != 2) {
        printf("usage: ./mainc path\n");
        exit(0);
    }
    char *path = argv[1];

    // Load the distribution.
    FILE *fp = fopen(path, "r");
    int Z;
    fscanf(fp, "%d", &Z);
    struct array_s x = load_array(fp);
    fclose(fp);

    // Measure time of FLDR.
    clock_t t;
    t = clock();
    int d = preprocess_fldr(x, Z);
    t = clock() - t;
    double t_fldr = ((double) t) / CLOCKS_PER_SEC;

    // Measure time of Alias GSL.
    t = clock();
    preprocess_alias_gsl(x, Z);
    t = clock() - t;
    double t_alias = ((double) t) / CLOCKS_PER_SEC;

    printf("%dc %1.6f %1.6f\n", d, t_fldr, t_alias);
}
