def fib(n):
    fst, snd = 1, 0
    n_fibs = [fst]
    for _ in range(n - 1):
        fst, snd = fst + snd, fst
        n_fibs.append(fst)
    return n_fibs
