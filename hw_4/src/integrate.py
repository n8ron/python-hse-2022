import math
import time
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime


def _integrate(f, left, right, step):
    acc = 0
    cur = left
    start_time = datetime.now()
    while cur < right:
        acc += f(cur) * min(right - cur, step)
        cur += step
    end_time = datetime.now()
    return acc, start_time, end_time, left, right


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, is_multiprocess=False, logging=False):
    logs = []
    executor_cls = ProcessPoolExecutor if is_multiprocess else ThreadPoolExecutor
    res = []
    int_step = (b - a) / n_iter
    range_step = (b - a) / n_jobs
    cur_pos = a
    with executor_cls(max_workers=n_jobs) as executor:
        integrate_res = 0
        for i in range(n_jobs):
            next_pos = cur_pos + range_step
            res.append(executor.submit(_integrate, f, cur_pos, min(next_pos, b), int_step))
            cur_pos = next_pos
        for t in res:
            acc, start_time, end_time, left, right = t.result()
            integrate_res += acc
            logs.append((start_time, end_time, left, right))
    if logging:
        with open("../artifacts/processes_log_integrate.txt", "w") as f:
            for log in logs:
                f.write("Integrate from {} to {} part from {} to {}\n".format(*log))
    return integrate_res


if __name__ == "__main__":
    print(integrate(math.cos, 0, math.pi / 2, n_iter=1000000, n_jobs=10, logging=True))

    cpu_num = multiprocessing.cpu_count()
    with open('../artifacts/compare.txt', 'w') as fp:
        for n_jobs_ in range(1, 2 * cpu_num + 1):
            fp.write(f'{n_jobs_} threads:\n')
            start_time_threads = time.time()
            result = integrate(math.cos, 0, math.pi / 2, n_iter=1000000, n_jobs=n_jobs_)
            fp.write(
                f'\tTime: {time.time() - start_time_threads} seconds\n'
                f'\tResult: {result}\n'
            )

            fp.write(f'{n_jobs_} processes:\n')
            start_time_processes = time.time()
            result = integrate(math.cos, 0, math.pi / 2, n_iter=1000000, n_jobs=n_jobs_, is_multiprocess=True)
            fp.write(
                f'\tTime: {time.time() - start_time_processes} seconds\n'
                f'\tResult: {result}\n'
            )
