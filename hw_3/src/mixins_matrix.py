import numbers

import numpy as np


class ConsoleRepresentationMixin:

    def __str__(self) -> str:
        return "[" + "\n".join(
            map(
                str,
                map(
                    list,
                    self._matrix
                )
            )
        ) + "]"


class WritingToFileMixin:

    def write_to_file(self, path: str):
        with open(path, 'w') as f:
            f.write(str(self))


class FieldPropertiesMixin:

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = np.asarray(matrix)


class MixinsMatrix(
    np.lib.mixins.NDArrayOperatorsMixin,
    ConsoleRepresentationMixin,
    WritingToFileMixin,
    FieldPropertiesMixin
):

    def __init__(self, matrix):
        self._matrix = np.asarray(matrix)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (MixinsMatrix,)):
                return NotImplemented

        inputs = tuple(x._matrix if isinstance(x, MixinsMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x._matrix if isinstance(x, MixinsMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)
