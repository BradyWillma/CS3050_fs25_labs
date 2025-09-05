"""_summary_
Key Features:
Real Algorithm Implementations for Each Case:
CASE 1 (Subproblems Dominate):

Binary Tree Sum: Just adds a constant at each node
Tournament Maximum: Simple comparisons only
These do minimal work (O(1)) at each node

CASE 2 (Balanced Work):

Merge Sort: Linear merging at each level
Partition Statistics: Scans all elements at each level
These do O(n) work at each node

CASE 3 (Outside Work Dominates):

Matrix Multiplication: O(n³) work at each node
Exhaustive Search: O(n²) pair checking at each node
These do polynomial work that overshadows recursion

Visual Analysis Shows:

Work Distribution Bars: Shows exactly how much work happens at each level
Cumulative Work Plots: Reveals whether work is bottom-heavy, balanced, or top-heavy
Side-by-side Comparison: All three cases visualized together

Key Educational Points:
The program emphasizes that it's NOT about the data - the same array can be processed by all three algorithm types. What matters is:

Case 1: Algorithm just splits/combines with minimal operations
Case 2: Algorithm processes all n elements at each level
Case 3: Algorithm does expensive operations (nested loops) at each node

Interactive Features:

Students can run each algorithm on different data sizes
See actual work counts at each recursion level
Visual bars show work distribution patterns
Compare theoretical predictions with actual execution
"""
import math
import numpy as np
import matplotlib.pyplot as plt
import time
from typing import List, Tuple, Callable
import random

def print_separator(char="=", length=70, title=""):
    """Helper function to print separators with optional title"""
    if title:
        padding = (length - len(title) - 2) // 2
        print(f"{char * padding} {title} {char * padding}")
    else:
        print(char * length)

# ============================================================================
# CASE 1 ALGORITHMS: Subproblems Dominate (Bottom-Heavy)
# ============================================================================

def binary_tree_sum(arr, start=0, end=None, depth=0, trace=None):
    """
    Case 1 Example: Sum all elements in array using binary tree recursion
    T(n) = 2T(n/2) + O(1)
    Just splits and combines - minimal work at each node
    """
    if trace is None:
        trace = []
    if end is None:
        end = len(arr)
    
    size = end - start
    
    if size <= 1:
        result = arr[start] if size == 1 else 0
        trace.append({'depth': depth, 'size': size, 'work': 1, 'result': result})
        return result, trace
    
    mid = (start + end) // 2
    
    # Record the split (constant work)
    trace.append({'depth': depth, 'size': size, 'work': 1, 'operation': 'split'})
    
    # Recursive calls
    left_sum, _ = binary_tree_sum(arr, start, mid, depth + 1, trace)
    right_sum, _ = binary_tree_sum(arr, mid, end, depth + 1, trace)
    
    # Combine (constant work)
    result = left_sum + right_sum
    trace.append({'depth': depth, 'size': size, 'work': 1, 'result': result})
    
    return result, trace

def tournament_max(arr, start=0, end=None, depth=0, trace=None):
    """
    Case 1 Example: Find maximum using tournament style
    T(n) = 2T(n/2) + O(1)
    """
    if trace is None:
        trace = []
    if end is None:
        end = len(arr)
    
    size = end - start
    
    if size <= 1:
        result = arr[start] if size == 1 else float('-inf')
        trace.append({'depth': depth, 'size': size, 'work': 1, 'result': result})
        return result, trace
    
    mid = (start + end) // 2
    
    trace.append({'depth': depth, 'size': size, 'work': 1, 'operation': 'compare'})
    
    left_max, _ = tournament_max(arr, start, mid, depth + 1, trace)
    right_max, _ = tournament_max(arr, mid, end, depth + 1, trace)
    
    result = max(left_max, right_max)
    trace.append({'depth': depth, 'size': size, 'work': 1, 'result': result})
    
    return result, trace

# ============================================================================
# CASE 2 ALGORITHMS: Balanced Work (Equal at All Levels)
# ============================================================================

def merge_sort_real(arr, depth=0, trace=None):
    """
    Case 2 Example: Classic Merge Sort
    T(n) = 2T(n/2) + O(n)
    Linear work at each level for merging
    """
    if trace is None:
        trace = []
    
    n = len(arr)
    
    if n <= 1:
        trace.append({'depth': depth, 'size': n, 'work': n, 'operation': 'base'})
        return arr, trace
    
    mid = n // 2
    left = arr[:mid]
    right = arr[mid:]
    
    # Record split
    trace.append({'depth': depth, 'size': n, 'work': n, 'operation': 'split'})
    
    # Recursive calls
    left_sorted, _ = merge_sort_real(left, depth + 1, trace)
    right_sorted, _ = merge_sort_real(right, depth + 1, trace)
    
    # Merge (linear work)
    merged = []
    i = j = 0
    work_done = 0
    
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] <= right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        else:
            merged.append(right_sorted[j])
            j += 1
        work_done += 1
    
    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])
    work_done += len(left_sorted[i:]) + len(right_sorted[j:])
    
    trace.append({'depth': depth, 'size': n, 'work': work_done, 'operation': 'merge'})
    
    return merged, trace

def partition_statistics(arr, depth=0, trace=None):
    """
    Case 2 Example: Computing order statistics with linear partitioning
    T(n) = 2T(n/2) + O(n)
    """
    if trace is None:
        trace = []
    
    n = len(arr)
    
    if n <= 1:
        trace.append({'depth': depth, 'size': n, 'work': 1, 'operation': 'base'})
        return arr, trace
    
    # Linear scan to compute statistics
    median = np.median(arr)
    mean = np.mean(arr)
    work = n  # Linear scan
    
    trace.append({'depth': depth, 'size': n, 'work': work, 
                 'operation': f'stats: median={median:.1f}, mean={mean:.1f}'})
    
    # Partition around median
    left = [x for x in arr if x < median]
    right = [x for x in arr if x >= median]
    
    # Process both halves if they exist
    if len(left) > 0:
        partition_statistics(left, depth + 1, trace)
    if len(right) > 1:  # Skip if only median remains
        partition_statistics(right, depth + 1, trace)
    
    return arr, trace

# ============================================================================
# CASE 3 ALGORITHMS: Outside Work Dominates (Top-Heavy)
# ============================================================================

def matrix_recursive_multiply(n, depth=0, trace=None):
    """
    Case 3 Example: Naive recursive matrix multiplication
    T(n) = 2T(n/2) + O(n³) 
    Combining submatrices requires n³ work
    """
    if trace is None:
        trace = []
    
    if n <= 1:
        trace.append({'depth': depth, 'size': n, 'work': 1, 'operation': 'base'})
        return 1, trace
    
    # Simulate n³ work for matrix operations at this level
    work = n ** 3
    trace.append({'depth': depth, 'size': n, 'work': work, 
                 'operation': f'matrix ops: {n}×{n}×{n}'})
    
    # Two recursive calls on n/2 sized problems
    matrix_recursive_multiply(n // 2, depth + 1, trace)
    matrix_recursive_multiply(n // 2, depth + 1, trace)
    
    return work, trace

def exhaustive_search_with_pruning(arr, target, depth=0, trace=None):
    """
    Case 3 Example: Exhaustive search with expensive local computation
    T(n) = 2T(n/2) + O(n²)
    Quadratic work at each node for checking combinations
    """
    if trace is None:
        trace = []
    
    n = len(arr)
    
    if n <= 1:
        trace.append({'depth': depth, 'size': n, 'work': 1, 'operation': 'base'})
        return arr[0] == target if n == 1 else False, trace
    
    # Check all pairs at this level (quadratic work)
    work = 0
    for i in range(n):
        for j in range(i + 1, n):
            work += 1
            if arr[i] + arr[j] == target:
                trace.append({'depth': depth, 'size': n, 'work': work, 
                            'operation': f'found pair: {arr[i]}+{arr[j]}={target}'})
                return True, trace
    
    trace.append({'depth': depth, 'size': n, 'work': work, 
                 'operation': f'checked {work} pairs'})
    
    # Recursively check halves
    mid = n // 2
    left_found, _ = exhaustive_search_with_pruning(arr[:mid], target, depth + 1, trace)
    if left_found:
        return True, trace
    
    right_found, _ = exhaustive_search_with_pruning(arr[mid:], target, depth + 1, trace)
    return right_found, trace

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def analyze_algorithm_characteristics(name, algorithm, data, *args):
    """
    Analyze and visualize the characteristics of an algorithm
    """
    print_separator("=", title=f"{name}")
    
    # Run algorithm and collect trace
    if args:
        result, trace = algorithm(data, *args)
    else:
        result, trace = algorithm(data)
    
    # Analyze work distribution by depth
    depth_work = {}
    for item in trace:
        if 'depth' in item:
            depth = item['depth']
            if depth not in depth_work:
                depth_work[depth] = {'count': 0, 'total_work': 0, 'operations': []}
            depth_work[depth]['count'] += 1
            depth_work[depth]['total_work'] += item.get('work', 0)
            if 'operation' in item:
                depth_work[depth]['operations'].append(item['operation'])
    
    # --- FIXED: handle ints vs sequences here ---
    if isinstance(data, int):
        data_preview = f"n={data}"
        n = data
    elif isinstance(data, (list, tuple, np.ndarray, str)):
        seq = list(data)
        data_preview = f"{seq[:10]}{'...' if len(seq) > 10 else ''}"
        n = len(seq)
    else:
        try:
            n = len(data)
        except TypeError:
            n = "?"
        data_preview = repr(data)

    print(f"\nData: {data_preview}")
    print(f"Size: n = {n}")
    # -------------------------------------------

    print("\n📊 Work Distribution by Level:")
    print("-" * 60)
    print("Level | Nodes | Total Work | Work/Node | Visualization")
    print("-" * 60)
    
    max_work = max(d['total_work'] for d in depth_work.values()) if depth_work else 1
    total_work = 0
    
    for depth in sorted(depth_work.keys()):
        info = depth_work[depth]
        work_per_node = info['total_work'] / info['count'] if info['count'] > 0 else 0
        total_work += info['total_work']
        
        bar_width = int(30 * (info['total_work'] / max_work)) if max_work > 0 else 0
        bar = "█" * bar_width + "░" * (30 - bar_width)
        
        print(f"{depth:5} | {info['count']:5} | {info['total_work']:10.0f} | {work_per_node:9.1f} | {bar}")
    
    print("-" * 60)
    print(f"Total work: {total_work:.0f}")
    
    return depth_work, total_work

def visualize_master_cases(data_size=32):
    """
    Create comprehensive visualization comparing all three cases
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Generate test data
    data = list(range(data_size, 0, -1))  # Reverse sorted
    random.shuffle(data)
    
    algorithms = [
        ("CASE 1: Binary Tree Sum\nT(n) = 2T(n/2) + O(1)", binary_tree_sum),
        ("CASE 2: Merge Sort\nT(n) = 2T(n/2) + O(n)", merge_sort_real),
        ("CASE 3: Matrix Operations\nT(n) = 2T(n/2) + O(n³)", matrix_recursive_multiply)
    ]
    
    # For each case, create visualizations
    for col, (title, algorithm) in enumerate(algorithms):
        # Run algorithm
        if algorithm == matrix_recursive_multiply:
            result, trace = algorithm(data_size)
        else:
            result, trace = algorithm(data[:data_size])
        
        # Analyze work by depth
        depth_work = {}
        for item in trace:
            if 'depth' in item:
                depth = item['depth']
                if depth not in depth_work:
                    depth_work[depth] = 0
                depth_work[depth] += item.get('work', 0)
        
        depths = sorted(depth_work.keys())
        work_values = [depth_work[d] for d in depths]
        
        # Top plot: Work distribution
        ax1 = axes[0, col]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        bars = ax1.bar(depths, work_values, color=[colors[i % len(colors)] for i in depths])
        
        # Add value labels on bars
        for bar, work in zip(bars, work_values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{work:.0f}', ha='center', va='bottom', fontsize=9)
        
        ax1.set_xlabel('Depth/Level')
        ax1.set_ylabel('Work Done')
        ax1.set_title(title, fontweight='bold', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Bottom plot: Cumulative work
        ax2 = axes[1, col]
        cumulative_work = np.cumsum(work_values)
        ax2.plot(depths, cumulative_work, 'o-', linewidth=2, markersize=8)
        ax2.fill_between(depths, 0, cumulative_work, alpha=0.3)
        
        # Add annotations for case characteristics
        total_work = cumulative_work[-1]
        
        if col == 0:  # Case 1
            ax2.text(0.5, 0.9, 'Bottom-Heavy\n(Leaves Dominate)', 
                    transform=ax2.transAxes, ha='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
        elif col == 1:  # Case 2
            ax2.text(0.5, 0.9, 'Balanced\n(Equal Work)', 
                    transform=ax2.transAxes, ha='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.5))
        else:  # Case 3
            ax2.text(0.5, 0.9, 'Top-Heavy\n(Root Dominates)', 
                    transform=ax2.transAxes, ha='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.5))
        
        ax2.set_xlabel('Depth/Level')
        ax2.set_ylabel('Cumulative Work')
        ax2.set_title(f'Total: {total_work:.0f}', fontsize=10)
        ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Master Method: Three Cases Visualization', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def demonstrate_case_characteristics():
    """
    Demonstrate the key characteristics that determine each case
    """
    print_separator("=", title="MASTER METHOD: DATA & ALGORITHM CHARACTERISTICS")
    
    print("\n" + "="*70)
    print(" UNDERSTANDING WHICH ALGORITHMS FALL INTO EACH CASE ".center(70))
    print("="*70)
    
    print("\n📚 KEY INSIGHT: It's not about the data, it's about the WORK PATTERN!\n")
    
    # Case 1 Characteristics
    print("\n" + "-"*70)
    print("🔵 CASE 1: Subproblems Dominate (Bottom-Heavy)")
    print("-"*70)
    print("\n📌 CHARACTERISTICS:")
    print("• Minimal work at each node (O(1) or O(log n))")
    print("• Just splitting/combining with simple operations")
    print("• Most computation happens at the leaves")
    print("• Tree has many leaves compared to internal work")
    
    print("\n📊 TYPICAL ALGORITHMS:")
    print("• Binary search tree operations")
    print("• Tournament-style algorithms")
    print("• Simple recursive counting")
    print("• Power calculation (x^n)")
    
    print("\n🎯 RECOGNITION PATTERN:")
    print("  If you're just splitting and doing a simple comparison/addition")
    print("  → Probably Case 1!")
    
    # Case 2 Characteristics
    print("\n" + "-"*70)
    print("🟢 CASE 2: Balanced Work (Equal at All Levels)")
    print("-"*70)
    print("\n📌 CHARACTERISTICS:")
    print("• Linear work at each node O(n)")
    print("• Processing all elements once per level")
    print("• Work decreases proportionally with problem size")
    print("• Perfect balance between splitting and combining")
    
    print("\n📊 TYPICAL ALGORITHMS:")
    print("• Merge Sort (merging takes O(n))")
    print("• Quick Sort best case (partitioning takes O(n))")
    print("• Finding median of medians")
    print("• Karatsuba multiplication (with linear combination)")
    
    print("\n🎯 RECOGNITION PATTERN:")
    print("  If you're scanning/processing all n elements at each level")
    print("  → Probably Case 2!")
    
    # Case 3 Characteristics
    print("\n" + "-"*70)
    print("🔴 CASE 3: Outside Work Dominates (Top-Heavy)")
    print("-"*70)
    print("\n📌 CHARACTERISTICS:")
    print("• Heavy work at each node (O(n²), O(n³), etc.)")
    print("• Expensive operations beyond just splitting/merging")
    print("• Work at root level dominates everything else")
    print("• Recursion doesn't help much due to expensive local work")
    
    print("\n📊 TYPICAL ALGORITHMS:")
    print("• Naive recursive matrix multiplication")
    print("• Exhaustive search algorithms")
    print("• Recursive algorithms with nested loops")
    print("• Poorly designed divide-and-conquer")
    
    print("\n🎯 RECOGNITION PATTERN:")
    print("  If you have nested loops or expensive operations at each node")
    print("  → Probably Case 3!")

def interactive_case_explorer():
    """
    Interactive exploration of different cases with various data sets
    """
    print_separator("=", title="INTERACTIVE CASE EXPLORER")
    
    while True:
        print("\n📋 Select Algorithm to Analyze:")
        print("\nCASE 1 Algorithms (Subproblems Dominate):")
        print("  1. Binary Tree Sum")
        print("  2. Tournament Maximum")
        
        print("\nCASE 2 Algorithms (Balanced):")
        print("  3. Merge Sort")
        print("  4. Partition Statistics")
        
        print("\nCASE 3 Algorithms (Outside Work Dominates):")
        print("  5. Matrix Recursive Multiply")
        print("  6. Exhaustive Search")
        
        print("\n  7. Compare All Cases Visually")
        print("  0. Exit")
        
        choice = input("\nSelect option (0-7): ").strip()
        
        if choice == '0':
            break
            
        # Get data size
        if choice in ['1', '2', '3', '4', '6']:
            size = int(input("Enter data size (e.g., 16, 32, 64): "))
            data = list(range(size, 0, -1))
            random.shuffle(data)
        
        if choice == '1':
            analyze_algorithm_characteristics("Binary Tree Sum", binary_tree_sum, data)
            print("\n💡 Notice: Work is constant at each node, total work dominated by leaves")
            
        elif choice == '2':
            analyze_algorithm_characteristics("Tournament Maximum", tournament_max, data)
            print("\n💡 Notice: Simple comparisons only, tree structure does most work")
            
        elif choice == '3':
            sorted_data = merge_sort_real(data.copy())[0]
            analyze_algorithm_characteristics("Merge Sort", merge_sort_real, data)
            print("\n💡 Notice: Work is proportional to n at each level, perfectly balanced")
            print(f"✅ Sorted result: {sorted_data[:10]}{'...' if len(sorted_data) > 10 else ''}")
            
        elif choice == '4':
            analyze_algorithm_characteristics("Partition Statistics", partition_statistics, data)
            print("\n💡 Notice: Linear scanning at each level creates balanced work")
            
        elif choice == '5':
            size = int(input("Enter matrix size (power of 2, e.g., 8, 16, 32): "))
            analyze_algorithm_characteristics("Matrix Operations", matrix_recursive_multiply, size)
            print("\n💡 Notice: Cubic work at each node completely dominates recursion")
            
        elif choice == '6':
            target = int(input(f"Enter target sum (between {min(data)*2} and {max(data)*2}): "))
            analyze_algorithm_characteristics("Exhaustive Search", exhaustive_search_with_pruning, data, target)
            print("\n💡 Notice: Quadratic checking at each node overshadows recursive work")
            
        elif choice == '7':
            size = int(input("Enter data size for comparison (e.g., 32): "))
            visualize_master_cases(size)
            
        input("\n[Press Enter to continue...]")

def main():
    """
    Main demonstration program
    """
    print("\n" + "="*80)
    print(" MASTER METHOD: DATA CHARACTERISTICS & VISUAL ANALYSIS ".center(80))
    print("="*80)
    
    # 1. Show characteristics
    demonstrate_case_characteristics()
    input("\n[Press Enter to continue to examples...]")
    
    # 2. Run examples for each case
    print_separator("=", title="CASE 1 EXAMPLE: BINARY TREE SUM")
    data = list(range(16, 0, -1))
    analyze_algorithm_characteristics("Binary Tree Sum (Case 1)", binary_tree_sum, data)
    input("\n[Press Enter to continue...]")
    
    print_separator("=", title="CASE 2 EXAMPLE: MERGE SORT")
    analyze_algorithm_characteristics("Merge Sort (Case 2)", merge_sort_real, data)
    input("\n[Press Enter to continue...]")
    
    print_separator("=", title="CASE 3 EXAMPLE: MATRIX OPERATIONS")
    analyze_algorithm_characteristics("Matrix Multiply (Case 3)", matrix_recursive_multiply, 16)
    input("\n[Press Enter to see visual comparison...]")
    
    # 3. Visual comparison
    visualize_master_cases(32)
    
    # 4. Interactive exploration
    print("\n" + "="*70)
    print("Would you like to explore more algorithms interactively? (y/n)")
    if input().lower() == 'y':
        interactive_case_explorer()
    
    print("\n" + "="*70)
    print(" DEMONSTRATION COMPLETE ".center(70))
    print("="*70)
    print("\n📚 KEY TAKEAWAYS:")
    print("1. Case 1: Minimal work per node → leaves dominate")
    print("2. Case 2: Linear work per node → balanced across levels")
    print("3. Case 3: Heavy work per node → root dominates")
    print("4. The data doesn't determine the case - the algorithm's work pattern does!")

if __name__ == "__main__":
    main()