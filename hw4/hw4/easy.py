from multiprocessing import Process
from threading import Thread
from time import time


def fib(n):
    fib_seq = [0, 1]
    for i in range(2, n + 1):
        fib_seq.append(fib_seq[i - 1] + fib_seq[i - 2])
    return fib_seq


def easy_solution():
    n = 150_000
    jobs = 10

    start_time = time()
    for _ in range(jobs):
        fib(n)
    sync_time = time() - start_time

    start_time = time()
    threads = [Thread(target=fib, args=(n,)) for _ in range(jobs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    threads_time = time() - start_time

    start_time = time()
    procs = [Process(target=fib, args=(n,)) for _ in range(jobs)]
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()
    procs_time = time() - start_time

    with open('artifacts/easy.txt', 'w') as file:
        file.write(f'sync_time : {sync_time}\n')
        file.write(f'threads_time : {threads_time}\n')
        file.write(f'procs_time : {procs_time}\n')
