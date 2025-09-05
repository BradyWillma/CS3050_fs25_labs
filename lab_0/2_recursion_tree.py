import math 
import numpy as np 

def merge_sort_work_calculator(n, depth=0):
    """Calculate work done by merge sort at each level"""
    if n <= 1:
        return [(depth, 1)]
    
    work = [(depth, n)]  # Current level work
    # Add work from left and right subtrees
    work.extend(merge_sort_work_calculator(n//2, depth+1))
    work.extend(merge_sort_work_calculator(n - n//2, depth+1))
    
    return work

def visualize_recursion_tree():
    """Visualize the recursion tree for merge sort"""
    print("\nRecursion Tree Method Demonstration")
    print("Recurrence: T(n) = 2T(n/2) + n (Merge Sort)")
    print("\nRecursion Tree Structure:")
    
    n = 16
    work = merge_sort_work_calculator(n)
    
    # Group work by depth
    depth_work = {}
    for d, w in work:
        if d not in depth_work:
            depth_work[d] = []
        depth_work[d].append(w)
    
    print(f"\nFor n = {n}:")
    print("-" * 50)
    total_work = 0
    
    for depth in sorted(depth_work.keys()):
        level_work = sum(depth_work[depth])
        num_nodes = len(depth_work[depth])
        total_work += level_work
        
        # Visual representation
        indent = "  " * depth
        nodes = f"[{','.join(map(str, depth_work[depth]))}]"
        
        print(f"Level {depth}: {indent}{nodes}")
        print(f"         Work at level: {level_work} (from {num_nodes} nodes)")
    
    print("-" * 50)
    print(f"Total work: {total_work}")
    print(f"Number of levels: {len(depth_work)} = log₂(n) + 1")
    print(f"Work per level: n")
    print(f"Total: n * log(n) = {n} * {np.log2(n):.0f} = {n * np.log2(n):.0f}")

visualize_recursion_tree()

def analyze_recurrence_tree(a, b, f_n, n):
    """
    Generic recursion tree analyzer
    For recurrence: T(n) = a*T(n/b) + f(n)
    """
    print(f"\nAnalyzing: T(n) = {a}*T(n/{b}) + f(n)")
    
    levels = int(np.log(n) / np.log(b)) + 1
    
    print("\nLevel | # Nodes | Work per Node | Total Work")
    print("-" * 50)
    
    total_work = 0
    for level in range(levels):
        num_nodes = a ** level
        size_at_level = n / (b ** level)
        work_per_node = f_n(size_at_level)
        level_work = num_nodes * work_per_node
        total_work += level_work
        
        print(f"{level:5} | {num_nodes:7} | {work_per_node:13.2f} | {level_work:10.2f}")
    
    print("-" * 50)
    print(f"Total work: {total_work:.2f}")
    
    # Determine complexity
    leaf_work = a ** (levels - 1)
    root_work = f_n(n)
    
    print(f"\nLeaf nodes: {leaf_work}")
    print(f"Root work: {root_work}")
    
    return total_work

# Example analyses
print("\n" + "="*60)
print("RECURSION TREE EXAMPLES")
print("="*60)

# Binary search: T(n) = T(n/2) + 1
analyze_recurrence_tree(1, 2, lambda x: 1, 64)

# Merge sort: T(n) = 2T(n/2) + n
analyze_recurrence_tree(2, 2, lambda x: x, 64)

# Strassen's algorithm: T(n) = 7T(n/2) + n²
analyze_recurrence_tree(7, 2, lambda x: x**2, 64)