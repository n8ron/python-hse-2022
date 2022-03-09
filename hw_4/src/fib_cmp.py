import time

from multiprocessing import Process
from threading import Thread


def fib(n):
    fst, snd = 1, 0
    n_fibs = [fst]
    for _ in range(n - 1):
        fst, snd = fst + snd, fst
        n_fibs.append(fst)
    return n_fibs


if __name__ == "__main__":
    N = 100000

    start_time = time.time()
    for _ in range(10):
        fib(N)
    sync_time = time.time() - start_time

    threads = [Thread(target=fib, args=(N, )) for _ in range(10)]
    start_time = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    threads_time = time.time() - start_time

    processes = [Process(target=fib, args=(N, )) for _ in range(10)]
    start_time = time.time()
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    processes_time = time.time() - start_time

    with open("../artifacts/easy_logs.txt", "w") as f:
        f.write(f"Test getting first {N} fibonacci numbers\n")
        f.write(f"Synchronous time: {sync_time} sec\n")
        f.write(f"Threads time: {threads_time} sec\n")
        f.write(f"Processes time: {processes_time} sec\n")

