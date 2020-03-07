# Released under Apache 2.0; refer to LICENSE.txt

def write_array(array, f):
    n = len(array)
    f.write('%d ' % (n,))
    f.write(' '.join(map(str, array)))
    f.write('\n')

def write_matrix(matrix, f):
    nrow = len(matrix)
    ncol = len(matrix[0])
    f.write('%d %d\n' % (nrow, ncol))
    for row in matrix:
        f.write(' '.join(map(str, row)))
        f.write('\n')

def write_sample_ky_encoding(enc, n, k, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (n, k))
        write_array(enc, f)

def write_sample_ky_matrix(P, k, l, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (k, l))
        write_matrix(P, f)

def write_sample_ky_matrix_cached(k, l, h, T, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (k, l))
        write_array(h, f)
        write_matrix(T, f)

def write_sample_fdr(n, fname):
    with open(fname, 'w') as f:
        f.write('%d\n' % (n,))

def write_sample_inversion_bernoulli(a, M, fname):
    with open(fname, 'w') as f:
        f.write("%d %d\n" % (a, M))

def write_sample_rejection_uniform(Ms, M, n, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (n, M,))
        write_array(Ms, f)

def write_sample_rejection_hash_table(T, Z, k, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (k, Z))
        write_array(T, f)

def write_sample_rejection_binary_search(cdf, Z, k, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (k, Z))
        write_array(cdf, f)

def write_sample_interval(cdf, Z, k, fname):
    with open(fname, 'w') as f:
        f.write('%d %d\n' % (k, Z))
        write_array(cdf, f)

def write_sample_alias(n, qs, Ms, j, fname):
    with open(fname, 'w') as f:
        f.write('%d\n' % (n,))
        write_array(qs, f)
        write_array(Ms, f)
        write_array(j, f)
