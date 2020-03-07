/*
  Name:     utils.c
  Purpose:  Utilities for searching.
  Author:   F. A. Saad and C. E. Freer
  Copyright (C) 2020 Feras A. Saad and C. E. Freer, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#include "utils.h"

int binary_search_interval(int *arr, int length, int x) {
    int l = 0;
    int r = length - 1;

    while (l <= r) {
        int mid = l + (r - l) / 2;
        if ((arr[mid-1] <= x) && (x < arr[mid])) {
            return mid - 1;
        } else if (arr[mid] <= x) {
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }
}

int binary_search_interval_nested(int *arr, int arr_denominator, int length,
        int a, int b, int denominator) {

    int l = 0;
    int r = length - 1;

    int common_a = a * arr_denominator;
    int common_b = b * arr_denominator;

    while (l <= r) {
        int mid = l + (r - l) / 2;
        if ((arr[mid-1] * denominator <= common_a)
                && (common_b <= arr[mid] * denominator)) {
            return mid - 1;
        } else if (arr[mid] * denominator <= common_a) {
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }
    return -1;
}
