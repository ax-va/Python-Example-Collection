import functools
from time import sleep, time


def timeit(func):
    """ Timing decorator """
    @functools.wraps(func)
    def wrapper(delay):
        print("Starting timing...")
        start_time = time()
        result = func(delay)
        stop_time = time()
        print(f"Task elapsed time: {stop_time - start_time}")
        return result
    return wrapper


def complex_task1(delay):
    sleep(delay)
    return "Task done"


new_complex_task = timeit(complex_task1)
print(new_complex_task(1.5))
# Starting timing...
# Task elapsed time: 1.5000855922698975
# Task done


@timeit
def complex_task2(delay):
    sleep(delay)
    return "task done"


print(complex_task2(1.5))
# Starting timing...
# Task elapsed time: 1.5001194477081299
# task done
