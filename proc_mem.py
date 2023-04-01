# proc_mem.py
import psutil
import os
import random
import string
import pandas as pd
import gc
import sys


def format_mb(n):
    return f"{n / 1024 ** 2:,.2f} MiB"


def random_string():
    """Generate a random string with letters and numbers, between 10 and 100 characters"""
    return "".join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(10, 100)))


def random_strings(n, n_unique=None):
    """Returns a generator of n random strings, choosing from n_unique unique strings."""
    if n_unique is None:
        n_unique = n
    if n == n_unique:
        return (random_string() for _ in range(n_unique))
    choices = [random_string() for _ in range(n_unique)]
    return (random.choice(choices) for _ in range(n))


if __name__ == "__main__":
    if len(sys.argv) == 4:
        string_dtype = sys.argv[1]
        N = int(sys.argv[2])
        N_UNIQUE = int(sys.argv[3])
    else:
        print(f"Usage: {sys.argv[0]} [STRING_DTYPE] [N] [N_UNIQUE]")
        exit(1)

    process = psutil.Process(os.getpid())
    mem1 = process.memory_info().rss
    print(f"{string_dtype = }, {N = :,}, {N_UNIQUE = :,}")
    print(f"before: {format_mb(mem1)}")
    s = pd.Series(random_strings(N, N_UNIQUE), dtype=string_dtype, copy=True)
    mem_s = s.memory_usage(deep=True)
    print(f"pandas reported: {format_mb(mem_s)}")
    mem2 = process.memory_info().rss
    print(f"psutil reported: {format_mb(mem2 - mem1)}")
    del s
    gc.collect()
    mem3 = process.memory_info().rss
    print(f"released: {format_mb(mem2 - mem3)}")
