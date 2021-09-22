import contextlib
import time


@contextlib.contextmanager
def timer(name: str):
    start = time.time()
    yield
    duration = (time.time() - start) * 1000
    print(f"{name}: {duration} ms")
