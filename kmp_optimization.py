import random
import string
import time
import multiprocessing

def compute_lps_array(pattern):
    """
    Compute the Longest Prefix Suffix (LPS) array for the given pattern.
    """
    m = len(pattern)
    lps = [0] * m
    j = 0  # Length of the previous longest prefix suffix

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]

        if pattern[i] == pattern[j]:
            j += 1
        lps[i] = j

    return lps

def kmp_search(text, pattern, lps):
    """
    Perform Knuth-Morris-Pratt (KMP) pattern matching algorithm.
    """
    n = len(text)
    m = len(pattern)

    matches = []

    i = 0  # Index for text[]
    j = 0  # Index for pattern[]

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches

def generate_random_text(length):
    """
    Generate random text of given length.
    """
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_random_pattern(length):
    """
    Generate a random pattern of given length.
    """
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_test_cases(num_cases, max_text_length, max_pattern_length):
    """
    Generate test cases with random text and patterns.
    """
    test_cases = []
    for _ in range(num_cases):
        text_length = random.randint(1, max_text_length)
        pattern_length = random.randint(1, max_pattern_length)
        text = generate_random_text(text_length)
        pattern = generate_random_pattern(pattern_length)
        test_cases.append((text, pattern))
    return test_cases

def measure_execution_time(test_case):
    """
    Measure execution time of KMP algorithm for a single test case.
    """
    text, pattern = test_case
    start_time = time.time()  # Record start time
    lps = compute_lps_array(pattern)  # Precompute LPS array
    matches = kmp_search(text, pattern, lps)  # Execute KMP algorithm
    end_time = time.time()  # Record end time
    execution_time = end_time - start_time  # Calculate execution time
    return len(text), len(pattern), execution_time

if __name__ == "__main__":
    # Generate test cases
    num_cases = 5
    max_text_length = 5000
    max_pattern_length = 100
    test_cases = generate_test_cases(num_cases, max_text_length, max_pattern_length)

    # Gather empirical data using multiprocessing
    with multiprocessing.Pool() as pool:
        empirical_data = pool.map(measure_execution_time, test_cases)

    # Print empirical data
    print("Empirical Data:")
    for i, (text_length, pattern_length, execution_time) in enumerate(empirical_data):
        print(f"Test Case {i+1}:")
        print("Text Length:", text_length)
        print("Pattern Length:", pattern_length)
        print("Execution Time:", execution_time)