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


class Matrix:
    def __init__(self, values):
        self.values = values
        self.n = len(self.values)
        if self.n == 0:
            raise MatrixException('Zero matrix')
        self.m = len(self.values[0])
        for row in self.values:
            if self.m != len(row):
                raise MatrixException('Invalid matrix! All rows must have the same length!')

    def __add__(self, other):
        if self.n != other.n and self.m != other.m:
            raise MatrixOperationException(self.n, self.m, other.n, other.m)
        result_matrix = [[0 for _ in range(self.m)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                result_matrix[i][j] = self.values[i][j] + other.values[i][j]
        return Matrix(result_matrix)

    def __mul__(self, other):
        if self.n != other.n and self.m != other.m:
            raise MatrixOperationException(self.n, self.m, other.n, other.m)
        result_matrix = [[0 for _ in range(self.m)] for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                result_matrix[i][j] = self.values[i][j] * other.values[i][j]
        return Matrix(result_matrix)

    def __matmul__(self, other):
        if self.n != other.m:
            raise MatrixOperationException(self.n, self.m, other.n, other.m)
        result_matrix = [[0 for _ in range(self.n)] for _ in range(self.m)]
        for i in range(self.n):
            for j in range(self.m):
                for k in range(self.n):
                    result_matrix[i][j] = self.values[i][k] + other.values[k][j]
        return Matrix(result_matrix)

    def __str__(self):
        repr = 'Matrix([\n'
        for i in range(self.n):
            repr += str(self.values[i])
            if i != self.n - 1:
                repr += ',\n'
        repr += '\n])'
        return repr

def easy_solution():
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))

    artifacts_path = 'artifacts/easy'
    if not os.path.exists(artifacts_path):
        os.makedirs(artifacts_path)

    with open(f"{artifacts_path}/matrix+.txt", 'w') as f:
        f.write(str(a + b))

    with open(f"{artifacts_path}/matrix_mul.txt", 'w') as f:
        f.write(str(a * b))

    with open(f"{artifacts_path}/matrix@.txt", 'w') as f:
        f.write(str(a @ b))

