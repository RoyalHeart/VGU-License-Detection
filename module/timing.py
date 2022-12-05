import time


def timing(function, *args):
    start_time = time.time()
    function(*args)
    print("Time: ", round(time.time() - start_time, 3))
