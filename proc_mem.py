import psutil
import os
import random
import string
import pandas as pd
from dask.utils import format_bytes


if __name__ == "__main__":
    # string_dtype = "string[pyarrow]"
    string_dtype = object
    num_records = 10_000_000
    num_unique = 1_000_000
    names = [
        "".join(random.choices(string.ascii_letters + string.digits + " ", k=random.randint(10, 100)))
        for _ in range(num_unique)
    ]
    process = psutil.Process(os.getpid())
    mem1 = process.memory_info().rss
    print(f"{string_dtype = }")
    print(f"before: {format_bytes(mem1)}")

    s = pd.Series([random.choice(names) for _ in range(num_records)], dtype=string_dtype)

    mem_s = s.memory_usage(deep=True)
    print(f"pandas reported: {format_bytes(mem_s)}")
    mem2 = process.memory_full_info().rss
    # print(f"after: {format_bytes(mem2)}")
    print(f"psutil reported: {format_bytes(mem2 - mem1)}")
