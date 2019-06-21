#include <time.h>
#include <math.h>
#include <sys/time.h>
#include <unistd.h>
#include <signal.h>
#include <stdio.h>


#define NS_TO_S(ns) ((ns) / 1000000000.0)


double gettimeNanoTest(int c, struct timespec ts) {
    struct timespec start, stop;
    clock_gettime(c, &start);
    nanosleep(&ts, NULL);
    clock_gettime(c, &stop);

    long sdiff = (long)(stop.tv_sec - start.tv_sec);
    double nsdiff = NS_TO_S((double)(stop.tv_nsec - start.tv_nsec));
    double diff = sdiff + nsdiff;
    return diff;
}

double calcMean(double a[], int n) {
    if (n == 0)
        return 0.0;
    int i;
    double sum = 0;
    for (i = 0; i < n; i+=1) {
        sum += a[i];
    }
    double mean = sum / n;
    return mean;
}

double calcStdDev(double a[], double mean, int n) {
    if (n == 0)
        return 0.0;

    int i;
    double sq_diff_sum = 0;
    double diff;

    for (i = 0; i < n; i+=1) {
        diff = a[i] - mean;
        sq_diff_sum += diff * diff;
    }

    double variance = sq_diff_sum / n;
    return sqrt(variance);
}

void clockTest(double stdev[4], double means[4], struct timespec ts) {
    int testRuns = 1000;
    double results[4][testRuns];
    int clocks[] = {
        CLOCK_REALTIME,
        CLOCK_MONOTONIC,
        CLOCK_PROCESS_CPUTIME_ID,
        CLOCK_THREAD_CPUTIME_ID
    };
    //results suggest that CLOCK_PROCESS_CPUTIME_ID or CLOCK_THREAD_CPUTIME_ID
    // are the most consistent,
    //but CLOCK_MONOTONIC is the closest to the target value
    // (though CLOCK_REALTIME gets pretty close too)

    size_t i, j;
    for (i = 0; i < 4; i+=1) {
        int c = clocks[i];

        for (j = 0; j < testRuns; j+=1) {
            results[i][j] = gettimeNanoTest(c, ts);
        }
    }

    for (i = 0; i < 4; i+=1) {
        means[i] = calcMean(results[i], testRuns);
        stdev[i] = calcStdDev(results[i], means[i], testRuns);
    }

    return;
}

void printResults(char* clockNames[], double means[4], double stdev[4], double target) {
    int i;
    int minStdevIdx, minMeanIdx, closeIdx;
    double minStdev = 1, minMean = 1, close = 1;
    double dist;

    for (i = 0; i < 4; i+=1) {
        printf("mean  %s: %.10g\n", clockNames[i], means[i]);
        printf("stdev %s: %.10g\n", clockNames[i], stdev[i]);
        if (means[i] < minMean) {
            minMean = means[i];
            minMeanIdx = i;
        }
        if (stdev[i] < minStdev) {
            minStdev = stdev[i];
            minStdevIdx = i;
        }
        dist = fabs(means[i] - target);
        if (dist < close) {
            close = dist;
            closeIdx = i;
        }
    }

    puts("");
    printf("Min mean  = %.10g (%s)\n", minMean, clockNames[minMeanIdx]);
    printf("Min stdev = %.10g (%s)\n", minStdev, clockNames[minStdevIdx]);
    printf("Closest to target: %s (off by %.10g)\n", clockNames[closeIdx], close);
}

int main() {
    // sleep for 1,000,000 nanoseconds, which is 1 millisecond
    struct timespec ts0 = {0, 1000000L};
    // 10 microseconds
    struct timespec ts1 = {0, 10000L};
    // 1 microsecond
    struct timespec ts2 = {0, 1000L};
    // clock names
    char* clockNames[] = {
        "CLOCK_REALTIME",
        "CLOCK_MONOTONIC",
        "CLOCK_PROCESS_CPUTIME_ID",
        "CLOCK_THREAD_CPUTIME_ID"
    };

    double stdev[4];
    double means[4];

    double target = NS_TO_S(ts0.tv_nsec);
    printf("\nTarget time: %ld ns (%.10g seconds)\n", ts0.tv_nsec, target);
    clockTest(stdev, means, ts0);
    printResults(clockNames, means, stdev, target);

    target = NS_TO_S(ts1.tv_nsec);
    printf("\nTarget time: %ld ns (%.10g seconds)\n", ts1.tv_nsec, target);
    clockTest(stdev, means, ts1);
    printResults(clockNames, means, stdev, target);

    target = NS_TO_S(ts2.tv_nsec);
    printf("\nTarget time: %ld ns (%.10g seconds)\n", ts2.tv_nsec, target);
    clockTest(stdev, means, ts2);
    printResults(clockNames, means, stdev, target);

    // ualarm(1000, 0);
}
