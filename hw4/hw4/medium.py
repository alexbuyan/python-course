import concurrent.futures
import math
import os
import sys
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging
from multiprocessing import cpu_count
from time import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


def integrate_segment(args):
    f, (a, b), n_iter, do_logging = args
    if do_logging:
        logger.info('[PID {}] Integrating f on segment [{}; {}]'.format(os.getpid(), a, b))
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, executor, do_logging):
    if do_logging:
        executor_type = 'Thread'
        if isinstance(executor_type, ProcessPoolExecutor):
            executor_type = 'Process'
        logger.info(
            '[Executor : {} / n_jobs : {} / n_iter : {}] Integrating f on [{}; {}]'.format(executor_type, n_jobs,
                                                                                           n_iter, a, b))
    segment_step = (b - a) / n_jobs
    segment_iters = int(n_iter / n_jobs)
    args = [(f, (a + segment_step * i, a + segment_step * (i + 1)), segment_iters, do_logging) for i in range(n_jobs)]
    results = []
    with executor(max_workers=n_jobs) as pool:
        results = pool.map(integrate_segment, args)
    return sum(results)


def medium_solution():
    a = 0
    b = math.pi / 2
    f = math.cos
    n_iter = 1_000_000

    res_thread = []
    thread_res = 0
    res_process = []
    process_res = 0

    for n_jobs in range(1, 2 * cpu_count() + 1):
        start_time = time()
        thread_res = integrate(f, a, b, n_jobs=n_jobs, n_iter=n_iter, executor=ThreadPoolExecutor, do_logging=True)
        calc_time = time() - start_time
        res_thread.append((n_jobs, calc_time))

        start_time = time()
        process_res = integrate(f, a, b, n_jobs=n_jobs, n_iter=n_iter, executor=ProcessPoolExecutor, do_logging=True)
        calc_time = time() - start_time
        res_process.append((n_jobs, calc_time))

    with open('artifacts/medium.txt', 'w') as file:
        file.write('-- Threading results --\n')
        for res in res_thread:
            file.write('n_jobs={} calc_time={} \n'.format(*res))
        file.write('Integration result == {}'.format(thread_res))

        file.write('\n\n\n')

        file.write('-- Multiprocessing results --\n')
        for res in res_process:
            file.write('n_jobs={} calc_time={} \n'.format(*res))
        file.write('Integration result == {}'.format(process_res))