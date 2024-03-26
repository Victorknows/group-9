import random
import time
import statistics
import matplotlib.pyplot as plt
from scipy import stats

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    left_index, right_index = 0, 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result

def generate_random_array(size):
    return [random.randint(0, 1000) for _ in range(size)]

def measure_time(algorithm, arr):
    start_time = time.time()
    algorithm(arr)
    end_time = time.time()
    return end_time - start_time

def run_experiment(algorithm, sizes, trials):
    runtimes = []
    for size in sizes:
        times = []
        for _ in range(trials):
            arr = generate_random_array(size)
            time_taken = measure_time(algorithm, arr)
            times.append(time_taken)
        runtimes.append(times)
    return runtimes

def analyze_statistics(runtimes):
    means = [statistics.mean(times) for times in runtimes]
    medians = [statistics.median(times) for times in runtimes]
    stddevs = [statistics.stdev(times) for times in runtimes]
    return means, medians, stddevs

def compare_algorithms(runtimes):
    t_statistic, p_value = stats.ttest_ind(runtimes[0], runtimes[1])
    return t_statistic, p_value

def plot_results(sizes, means, medians, stddevs):
    plt.errorbar(sizes, means, yerr=stddevs, fmt='o', label='Mean ± Std Dev')
    plt.plot(sizes, medians, marker='o', label='Median')
    plt.xlabel('Array Size')
    plt.ylabel('Time (seconds)')
    plt.title('Algorithm Performance Analysis')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    sizes = [100, 500, 1000, 2000, 5000]
    trials = 10

    quicksort_runtimes = run_experiment(quicksort, sizes, trials)
    mergesort_runtimes = run_experiment(mergesort, sizes, trials)

    quicksort_statistics = analyze_statistics(quicksort_runtimes)
    mergesort_statistics = analyze_statistics(mergesort_runtimes)

    quicksort_means, quicksort_medians, quicksort_stddevs = quicksort_statistics
    mergesort_means, mergesort_medians, mergesort_stddevs = mergesort_statistics

    plot_results(sizes, quicksort_means, quicksort_medians, quicksort_stddevs)
    plot_results(sizes, mergesort_means, mergesort_medians, mergesort_stddevs)

    t_statistic, p_value = compare_algorithms([quicksort_runtimes[0], mergesort_runtimes[0]])
    print("T-Statistic:", t_statistic)
    print("P-Value:", p_value)
