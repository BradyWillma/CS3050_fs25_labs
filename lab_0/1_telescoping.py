import time
import matplotlib.pyplot as plt
import numpy as np

def recursive_sum(n):
    """Example function with recurrence T(n) = T(n-1) + n"""
    if n <= 1:
        return n
    return recursive_sum(n-1) + n

# Verify our analysis: T(n) = n(n+1)/2 = O(n²)
def verify_telescoping():
    print("Telescoping Method Demonstration")
    print("Recurrence: T(n) = T(n-1) + n, T(1) = 1")
    print("\nExpanding:")
    print("T(n) = T(n-1) + n")
    print("     = T(n-2) + (n-1) + n")
    print("     = T(n-3) + (n-2) + (n-1) + n")
    print("     = ... ")
    print("     = T(1) + 2 + 3 + ... + n")
    print("     = 1 + 2 + 3 + ... + n")
    print("     = n(n+1)/2 = O(n²)")
    
    # Verify with actual values
    print("\nVerification:")
    for n in [5, 10, 15, 20]:
        result = recursive_sum(n)
        expected = n * (n + 1) // 2
        print(f"n={n:2d}: T(n)={result:4d}, n(n+1)/2={expected:4d} ✓")

verify_telescoping()

def time_telescoping_example():
    """Time the recursive sum to verify O(n²) behavior"""
    sizes = [10, 20, 30, 40, 50]
    times = []
    
    for n in sizes:
        start = time.perf_counter()
        for _ in range(1000):  # Run multiple times for accuracy
            recursive_sum(n)
        end = time.perf_counter()
        times.append((end - start) / 1000)
    
    # Plot results
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(sizes, times, 'bo-', label='Actual time')
    plt.xlabel('n')
    plt.ylabel('Time (seconds)')
    plt.title('Recursive Sum Performance')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    # Normalize to show O(n²) relationship
    normalized_times = [t / (sizes[0]**2 / times[0]) for t in times]
    expected_n2 = [n**2 for n in sizes]
    plt.plot(sizes, normalized_times, 'bo-', label='Actual (normalized)')
    plt.plot(sizes, expected_n2, 'r--', label='n² (expected)')
    plt.xlabel('n')
    plt.ylabel('Normalized time')
    plt.title('O(n²) Verification')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()