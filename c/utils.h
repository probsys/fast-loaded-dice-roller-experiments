/*
  Name:     utils.h
  Purpose:  Utilities for searching.
  Author:   F. A. Saad and C. E. Freer
  Copyright (C) 2020 Feras A. Saad and C. E. Freer, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#ifndef UTILS_H
#define UTILS_H

int binary_search_interval(int *arr, int length, int x);
int binary_search_interval_nested(int *arr, int arr_denominator,
    int length, int a, int b, int denominator);

#endif
