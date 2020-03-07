# Released under Apache 2.0; refer to LICENSE.txt

"""Algorithm for generating random bits lazily, adapted from

    Optimal Discrete Uniform Generation from Coin Flips, and Applications
    Jeremie Lumbroso, April 9, 2013
    https://arxiv.org/abs/1304.1916
"""

class BitStream(object):
    def __init__(self, k, rng):
        self.k = k
        self.word = 0
        self.pos = 0
        self.calls = 0
        self.rng = rng

    def flip(self):
        if self.pos == 0:
            self.word = self.rng.randint(pow(2, self.k))
            self.pos = self.k
        self.pos -= 1
        return (self.word & (1 << self.pos)) >> self.pos

    def __next__(self):
        self.calls += 1
        return self.flip()
