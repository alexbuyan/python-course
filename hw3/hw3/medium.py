import os

import numpy as np


class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(matrix)
        self.m = len(matrix[0])


class FileMixin:
    def write_to_file(self, filepath):
        with open(filepath, 'w') as file:
            file.write(str(self))


class StrReprMixin:
    def __str__(self):
        repr = 'Matrix([\n'
        for i in range(self.n):
            repr += str(self.matrix[i])
            if i != self.n - 1:
                repr += ',\n'
        repr += '\n])'
        return repr


class GetSetMixin:
    def set_matrix(self, matrix):
        self.matrix = matrix
        self.n = len(matrix)
        self.m = len(matrix[0])

    def get_matrix(self):
        return self.matrix

    def get_n(self):
        return self.n

    def get_m(self):
        return self.m


class MatrixNp(Matrix, np.lib.mixins.NDArrayOperatorsMixin, FileMixin, StrReprMixin, GetSetMixin):
    _HANDLED_TYPES = (Matrix,)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        inputs = tuple(x.matrix if isinstance(x, Matrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.matrix if isinstance(x, Matrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


def medium_solution():
    np.random.seed(0)
    a = MatrixNp(np.random.randint(0, 10, (10, 10)))
    b = MatrixNp(np.random.randint(0, 10, (10, 10)))

    artifacts_path = 'artifacts/medium'
    if not os.path.exists(artifacts_path):
        os.makedirs(artifacts_path)

    (a + b).write_to_file(f"{artifacts_path}/matrix+.txt")
    (a * b).write_to_file(f"{artifacts_path}/matrix_mul.txt")
    (a @ b).write_to_file(f"{artifacts_path}/matrix@.txt")




