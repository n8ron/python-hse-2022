import operator
from typing import Callable

from hw_3.src.mixins_matrix import WritingToFileMixin, ConsoleRepresentationMixin


class HashableMatrixMixin:

    def __hash__(self) -> int:
        """
        Calculate sum elements of matrix by module of prime number 10^9+7
        """
        sum_elem = 0
        for row in self._matrix:
            sum_elem += sum(row)
        return int(sum_elem) % (10 ** 9 + 7)


class Matrix(
    HashableMatrixMixin,
    WritingToFileMixin,
    ConsoleRepresentationMixin
):
    _matmul_cashed = {}

    # https://docs.python.org/3/reference/datamodel.html#object.__hash__ said that
    # "If a class does not define an __eq__() method it should not define a __hash__() operation either"
    # So I defined __eq__() method and this require this line because
    # "If a class that overrides __eq__() needs to retain the implementation of __hash__()
    # from a parent class, the interpreter must be told this explicitly by setting
    # __hash__ = <ParentClass>.__hash__."
    __hash__ = HashableMatrixMixin.__hash__

    def __init__(self, matrix):
        if len(matrix) == 0:
            raise ValueError("Input matrix should be 2 dimensional")
        self._shape = len(matrix), len(matrix[0])
        self._matrix = []

        for row in matrix:
            if len(row) != len(matrix[0]):
                raise ValueError("All rows in matrix should have equal sizes")
            self._matrix.append(list(row))

    @classmethod
    def invalidate_caches(cls):
        cls._matmul_cashed = {}

    def __add__(self, other: 'Matrix') -> 'Matrix':
        return self.__element_by_element_operator(other, operator.add)

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        return self.__element_by_element_operator(other, operator.mul)

    def __eq__(self, other):
        m_bool = self.__element_by_element_operator(other, operator.eq)
        for row in m_bool._matrix:
            for elem in row:
                if not elem:
                    return False
        return True

    def __element_by_element_operator(self, other: 'Matrix', element_operator: Callable) -> 'Matrix':
        if self._shape != other._shape:
            raise ValueError(f"shapes of matrix should be equal, but actual is {self._shape} and {other._shape}")
        return Matrix(
            [
                [
                    element_operator(
                        self._matrix[i][j], other._matrix[i][j]
                    )
                    for j in range(self._shape[1])
                ]
                for i in range(self._shape[0])
            ]
        )

    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        if self._shape != other._shape[::-1]:
            raise ValueError(f"operands could not be broadcast together with shapes {self._shape} and {other._shape}")
        key = hash(self), hash(other)
        if key not in self._matmul_cashed:
            self._matmul_cashed[key] = Matrix(
                [
                    [
                        sum(a * b for a, b in zip(self_row, other_col))
                        for other_col in zip(*other._matrix)
                    ]
                    for self_row in self._matrix
                ]
            )
        return self._matmul_cashed[key]

