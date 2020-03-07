/*
  Name:     flip.h
  Purpose:  Generating a sequence of pseudo-random bits.
  Author:   F. A. Saad
  Copyright (C) 2020 Feras A. Saad, All Rights Reserved.

  Released under Apache 2.0; refer to LICENSE.txt
*/

#ifndef FLIP_H
#define FLIP_H

extern unsigned long NUM_RNG_CALLS;

int flip(void);
int randint(int k);

#endif
