from typing import Union

import numpy as np

from hw_3.src.mixins_matrix import MixinsMatrix
from matrix import Matrix


def generate_operations(path_to_dir: str, cls: type):
    m1 = cls(np.random.randint(0, 10, (10, 10)))
    m2 = cls(np.random.randint(0, 10, (10, 10)))
    sum_m = m1 + m2
    mul_m = m1 * m2
    matmul_m = m1 @ m2
    sum_m.write_to_file(f"{path_to_dir}/matrix+.txt")
    mul_m.write_to_file(f"{path_to_dir}/matrix*.txt")
    matmul_m.write_to_file(f"{path_to_dir}/matrix@.txt")


def find_collision(path_to_dir: str):
    Matrix.invalidate_caches()
    shape = (2, 2)
    i = 0
    np.random.seed(239239239)
    while True:
        a = Matrix(np.random.randint(0, 5, shape))
        b = Matrix(np.random.randint(0, 5, shape))
        c = Matrix(np.random.randint(0, 5, shape))
        d = b
        ab = a @ b
        Matrix.invalidate_caches()
        cd = c @ d
        Matrix.invalidate_caches()
        if hash(a) == hash(c) and (a != c) and (ab != cd):
            print(f"Hacked on {i} iteration!")
            a.write_to_file(f"{path_to_dir}/A.txt")
            b.write_to_file(f"{path_to_dir}/B.txt")
            c.write_to_file(f"{path_to_dir}/C.txt")
            d.write_to_file(f"{path_to_dir}/D.txt")
            ab.write_to_file(f"{path_to_dir}/AB.txt")
            cd.write_to_file(f"{path_to_dir}/CD.txt")
            with open(f"{path_to_dir}/hash.txt", "w") as f:
                f.write(f"Hash AB is equal to {hash(ab)}, hash CD is equal to {hash(cd)}")
            break
        i += 1


if __name__ == "__main__":
    np.random.seed(0)
    generate_operations("../artifacts/easy", Matrix)
    np.random.seed(0)
    generate_operations("../artifacts/medium", MixinsMatrix)
    find_collision("../artifacts/hard")
