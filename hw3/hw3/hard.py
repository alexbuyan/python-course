import os

import numpy as np


class MatrixOperationException(Exception):
    def __init__(self, n1, m1, n2, m2):
        self.message = 'Operation aborted: Incorrect matrix sizes with {}x{} and {}x{}'.format(n1, m1, n2, m2)

    def __str__(self):
        return self.message


class MatrixException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class HashMixin:
    '''
    u, v - random numbers
    hash(a[i][j]) = a[i][j] * u^i * v^j
    hash(matrix) = sum(hash(a[i][j])
    '''

    def __init__(self):
        self.u = 1
        self.v = 2

    def matrix_hash(self):
        return sum(sum(elem * (self.u ** i) * (self.v ** j) for j, elem in enumerate(row)) for i, row in
                   enumerate(self.values))


class Matrix(HashMixin):
    known_hashes = {}

    def __init__(self, values):
        super().__init__()
        self.values = values
        self.n = len(self.values)
        if self.n == 0:
            raise MatrixException('Zero matrix')
        self.m = len(self.values[0])
        for row in self.values:
            if self.m != len(row):
                raise MatrixException('Invalid matrix! All rows must have the same length!')

    def __matmul__(self, other):
        if self.n != other.m:
            raise MatrixOperationException(self.n, self.m, other.n, other.m)
        res_hash = sum([hash(self), hash(other)])
        if res_hash in self.known_hashes:
            return Matrix(self.known_hashes[res_hash])
        result_matrix = [[0 for _ in range(self.n)] for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                for k in range(self.n):
                    result_matrix[i][j] = self.values[i][k] + other.values[k][j]
        self.known_hashes[res_hash] = result_matrix
        return Matrix(self.known_hashes[res_hash])

    def __str__(self):
        repr = 'Matrix([\n'
        for i in range(self.n):
            repr += str(self.values[i])
            if i != self.n - 1:
                repr += ',\n'
        repr += '\n])'
        return repr

    def __hash__(self):
        return self.matrix_hash()

    def write_to_file(self, filepath):
        with open(filepath, 'w') as file:
            file.write(str(self))


def hard_solution():
    a = Matrix([[1, 2], [3, 4]])  # hash 16
    b = Matrix([[1, 1], [1, 1]])
    c = Matrix([[4, 3], [2, 2]])  # hash 16
    d = Matrix([[1, 1], [1, 1]])

    artifacts_path = 'artifacts/hard'
    if not os.path.exists(artifacts_path):
        os.makedirs(artifacts_path)

    a.write_to_file(f"{artifacts_path}/A.txt")
    b.write_to_file(f"{artifacts_path}/B.txt")
    c.write_to_file(f"{artifacts_path}/C.txt")
    d.write_to_file(f"{artifacts_path}/D.txt")

    ab = a @ b

    # res_hash = hash(c) + hash(d) = hash(a) + hash(b), so we need to clear cache to compute correctly
    c.known_hashes = {}
    cd = c @ d

    ab.write_to_file(f"{artifacts_path}/AB.txt")
    cd.write_to_file(f"{artifacts_path}/CD.txt")

    with open(f"{artifacts_path}/hash.txt", 'w') as file:
        file.write(f'AB hash: {hash(ab)} \n')
        file.write(f'CD hash: {hash(cd)} \n')
