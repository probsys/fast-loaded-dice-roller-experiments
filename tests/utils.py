# Released under Apache 2.0; refer to LICENSE.txt

from collections import Counter

from scipy.stats import chisquare

def get_chisquare_pval(p_target, samples):
    N = len(samples)
    f_expected = [int(N*p) for p in p_target]
    counts = Counter(samples)
    keys = sorted(set(samples))
    f_actual = [counts[k] for k in keys]
    return chisquare(f_expected, f_actual)[1]
