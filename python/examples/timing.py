import time
import statistics

# test the resolution of the Python time module


def timeTest(t):
    t0 = time.perf_counter()
    time.sleep(t)
    t1 = time.perf_counter()
    return t1 - t0


def runTest(times, runs):
    means = []
    stdevs = []
    results = []

    for t in times:
        sublist = []
        for i in range(runs):
            sublist.append(timeTest(t))
        results.append(sublist)

    for i in range(len(times)):
        means.append(statistics.mean(results[i]))
        stdevs.append(statistics.stdev(results[i], times[i]))
        print("Sleep time: {:6}  Actual Mean: {:.10f}".format(times[i], means[i]), end='')
        print("  Stdev from expected: {:.10f}".format(stdevs[i]))


def main():
    bigTimes = [
        0.5, 0.25, 0.1
    ]
    smallTimes = [
        0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001, 0.00005, 0.00001
    ]
    bigRuns = 5
    smallRuns = 20

    runTest(bigTimes, bigRuns)
    runTest(smallTimes, smallRuns)


if __name__ == '__main__':
    main()
