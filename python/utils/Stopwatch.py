import time


def runWithStopwatch(func):
    start_time = time.time_ns()
    func()
    end_time = time.time_ns()
    print("Elapsed time: " + str((end_time - start_time) / 1_000_000) + " ms")
