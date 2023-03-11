def fib(n: int) -> list[int]:
    fib_seq = [0, 1]
    for _ in range(n - 2):
        fib_seq.append(fib_seq[-1] + fib_seq[-2])
    return fib_seq
