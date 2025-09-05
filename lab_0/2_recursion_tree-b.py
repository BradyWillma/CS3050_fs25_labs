"""_summary_
    How to Use:

    Run the program and select from the menu
    Try option 7 for a complete demonstration
    Use option 3 to see actual merge sort execution
    Option 5 lets students experiment with different recurrences

    Key Learning Points:
    The program clearly shows:

    How divide-and-conquer creates a tree structure
    Why work is often equal at each level (for merge sort)
    How to sum work across all levels
    The connection between tree height and logarithms
    When recursion trees are more appropriate than telescoping

    This makes the recursion tree method much more concrete and helps students understand not just the math, but the actual execution pattern of recursive algorithms!

"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from typing import List, Tuple, Dict
import time

class RecursionTreeVisualizer:
    """
    Interactive visualizer for recursion tree method
    """
    
    def __init__(self):
        self.tree_data = []
        self.execution_trace = []
        
    def clear(self):
        self.tree_data = []
        self.execution_trace = []

def print_separator(char="=", length=70, title=""):
    """Helper function to print separators with optional title"""
    if title:
        padding = (length - len(title) - 2) // 2
        print(f"{char * padding} {title} {char * padding}")
    else:
        print(char * length)

def actual_merge_sort(arr, depth=0, trace=None, side="root"):
    """
    Actual merge sort implementation with tracing
    """
    if trace is None:
        trace = []
    
    n = len(arr)
    indent = "  " * depth
    
    # Record the call
    trace.append({
        'depth': depth,
        'size': n,
        'array': arr.copy(),
        'side': side,
        'work': n,  # Work for merging
        'message': f"{indent}merge_sort({arr})"
    })
    
    if n <= 1:
        return arr, trace
    
    # Split
    mid = n // 2
    left_arr = arr[:mid]
    right_arr = arr[mid:]
    
    # Recursive calls
    left_sorted, _ = actual_merge_sort(left_arr, depth + 1, trace, "left")
    right_sorted, _ = actual_merge_sort(right_arr, depth + 1, trace, "right")
    
    # Merge
    merged = []
    i = j = 0
    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] <= right_sorted[j]:
            merged.append(left_sorted[i])
            i += 1
        else:
            merged.append(right_sorted[j])
            j += 1
    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])
    
    trace.append({
        'depth': depth,
        'size': n,
        'array': merged,
        'side': side,
        'work': n,
        'message': f"{indent}merged: {merged}"
    })
    
    return merged, trace

def visualize_tree_ascii(n, a=2, b=2, show_work=True):
    """
    Create an ASCII art visualization of the recursion tree
    """
    print_separator("=", title=f"RECURSION TREE for T(n) = {a}T(n/{b}) + n")
    
    def draw_node(size, depth, position="center", is_leaf=False):
        """Draw a single node with connections"""
        indent = "    " * depth
        
        # Node representation
        if is_leaf:
            node_str = f"[{size:.0f}]"
        else:
            node_str = f"({size:.0f})"
        
        # Add work annotation if requested
        if show_work:
            work = size
            node_str += f" w={work:.0f}"
        
        return indent + node_str
    
    def build_tree(size, depth=0, max_depth=5):
        """Recursively build the tree"""
        if depth >= max_depth or size < 1:
            return []
        
        nodes = []
        is_leaf = (size <= 1) or (depth == max_depth - 1)
        
        # Current node
        nodes.append(draw_node(size, depth, is_leaf=is_leaf))
        
        if not is_leaf:
            # Draw branches
            indent = "    " * depth
            nodes.append(indent + "  ├─┬─" + "─" * 10)
            
            # Recursive calls
            for i in range(a):
                child_size = size / b
                child_nodes = build_tree(child_size, depth + 1, max_depth)
                nodes.extend(child_nodes)
        
        return nodes
    
    print(f"\n🌳 Tree Structure (n = {n}):")
    print("=" * 60)
    
    tree_lines = build_tree(n)
    for line in tree_lines[:20]:  # Limit output
        print(line)
    
    if len(tree_lines) > 20:
        print("    ... (tree continues)")

def step_by_step_tree_construction(n, a=2, b=2):
    """
    Show step-by-step construction of recursion tree with detailed work calculation
    """
    print_separator("=", title="STEP-BY-STEP TREE CONSTRUCTION")
    
    print(f"\nBuilding tree for: T(n) = {a}T(n/{b}) + n")
    print(f"Starting with n = {n}")
    
    levels_data = []
    current_level = [(n, 1)]  # (size, count)
    level = 0
    
    print("\n📊 Level-by-Level Analysis:")
    print("-" * 70)
    
    while current_level and level < 10:  # Limit depth
        # Calculate work at this level
        level_sizes = []
        level_work_items = []
        total_nodes = 0
        
        for size, count in current_level:
            if size >= 1:
                total_nodes += count
                for _ in range(count):
                    level_sizes.append(size)
                    level_work_items.append(size)
        
        if not level_sizes:
            break
            
        level_work = sum(level_work_items)
        
        # Display level information
        print(f"\n🔹 Level {level}:")
        print(f"   Number of nodes: {total_nodes}")
        print(f"   Node sizes: {[f'{s:.1f}' for s in sorted(set(level_sizes), reverse=True)]}")
        print(f"   Work per node: {level_sizes[0] if level_sizes else 0:.1f}")
        print(f"   Total work at level: {level_work:.1f}")
        
        # Visual bar for work
        max_bar_width = 40
        if level == 0:
            max_work = level_work
        bar_width = int((level_work / max_work) * max_bar_width) if max_work > 0 else 0
        bar = "█" * bar_width + "░" * (max_bar_width - bar_width)
        print(f"   Work distribution: [{bar}] {level_work:.1f}")
        
        levels_data.append({
            'level': level,
            'nodes': total_nodes,
            'work': level_work,
            'sizes': level_sizes
        })
        
        # Prepare next level
        next_level = []
        for size, count in current_level:
            if size > 1:
                child_size = size / b
                for _ in range(count):
                    for _ in range(a):
                        next_level.append((child_size, 1))
        
        # Consolidate counts for same sizes
        size_counts = {}
        for size, count in next_level:
            if size not in size_counts:
                size_counts[size] = 0
            size_counts[size] += count
        
        current_level = list(size_counts.items())
        level += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("📈 SUMMARY:")
    total_work = sum(ld['work'] for ld in levels_data)
    print(f"   Total levels: {len(levels_data)}")
    print(f"   Total work: {total_work:.1f}")
    print(f"   Theoretical: n * log₂(n) = {n} * {math.log2(n):.1f} = {n * math.log2(n):.1f}")
    
    return levels_data

def compare_with_actual_execution(arr):
    """
    Compare theoretical tree with actual merge sort execution
    """
    print_separator("=", title="THEORETICAL VS ACTUAL EXECUTION")
    
    n = len(arr)
    print(f"\nArray to sort: {arr}")
    print(f"Size: n = {n}")
    
    # Run actual merge sort with tracing
    sorted_arr, trace = actual_merge_sort(arr)
    
    # Analyze trace by depth
    depth_analysis = {}
    for item in trace:
        depth = item['depth']
        if depth not in depth_analysis:
            depth_analysis[depth] = {
                'calls': [],
                'work': 0
            }
        depth_analysis[depth]['calls'].append(item)
        depth_analysis[depth]['work'] += item['work']
    
    print("\n🔄 Actual Execution Trace:")
    print("-" * 70)
    
    for depth in sorted(depth_analysis.keys()):
        calls = depth_analysis[depth]['calls']
        work = depth_analysis[depth]['work']
        
        print(f"\nDepth {depth}: ({len(calls)} operations)")
        for call in calls[:5]:  # Show first 5 calls at each depth
            print(f"  {call['message']}")
        if len(calls) > 5:
            print(f"  ... and {len(calls) - 5} more")
        print(f"  Total work at depth {depth}: {work}")
    
    print(f"\n✅ Sorted array: {sorted_arr}")
    
    return trace, depth_analysis

def visualize_tree_graphically(n, a=2, b=2, title="Recursion Tree"):
    """
    Create a graphical visualization of the recursion tree using matplotlib
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    
    # Left plot: Tree structure
    ax1.set_title(f"{title}\nT(n) = {a}T(n/{b}) + n", fontsize=14, fontweight='bold')
    ax1.set_xlim(-1, 10)
    ax1.set_ylim(-1, 6)
    ax1.axis('off')
    
    def draw_tree_node(ax, x, y, size, level, max_level=4):
        """Recursively draw tree nodes"""
        if level > max_level or size < 1:
            return
        
        # Node color based on level
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        color = colors[level % len(colors)]
        
        # Draw node
        circle = patches.Circle((x, y), 0.3, color=color, ec='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, f'{int(size)}', ha='center', va='center', fontweight='bold')
        
        # Draw work annotation
        ax.text(x, y - 0.5, f'w={int(size)}', ha='center', va='center', 
                fontsize=8, style='italic')
        
        # Draw children
        if level < max_level and size > 1:
            child_size = size / b
            spacing = 3 / (2 ** level)
            
            for i in range(a):
                child_x = x + (i - (a-1)/2) * spacing
                child_y = y - 1.2
                
                # Draw edge
                ax.plot([x, child_x], [y - 0.3, child_y + 0.3], 
                       'k-', linewidth=1, alpha=0.6)
                
                # Recursive call
                draw_tree_node(ax, child_x, child_y, child_size, level + 1, max_level)
    
    # Draw the tree
    draw_tree_node(ax1, 5, 5, n, 0, 4)
    
    # Add level labels
    for level in range(5):
        ax1.text(-0.5, 5 - level * 1.2, f'Level {level}', 
                fontweight='bold', va='center')
    
    # Right plot: Work distribution
    ax2.set_title('Work Distribution by Level', fontsize=14, fontweight='bold')
    
    # Calculate work per level
    levels = []
    work_per_level = []
    total_work = 0
    
    for level in range(int(math.log2(n)) + 1):
        num_nodes = a ** level
        node_size = n / (b ** level)
        level_work = num_nodes * node_size
        
        levels.append(level)
        work_per_level.append(level_work)
        total_work += level_work
    
    # Create bar chart
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    bars = ax2.bar(levels, work_per_level, color=[colors[i % len(colors)] for i in levels])
    
    # Add value labels on bars
    for bar, work in zip(bars, work_per_level):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{work:.0f}', ha='center', va='bottom')
    
    ax2.set_xlabel('Level')
    ax2.set_ylabel('Work')
    ax2.set_xticks(levels)
    ax2.grid(True, alpha=0.3)
    
    # Add total work annotation
    ax2.axhline(y=n, color='r', linestyle='--', alpha=0.5, label=f'n = {n}')
    ax2.text(len(levels) - 1, total_work * 1.1, 
            f'Total Work = {total_work:.0f}\n= n × log₂(n) = {n * math.log2(n):.0f}',
            ha='right', fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", 
                                                     facecolor="yellow", alpha=0.5))
    ax2.legend()
    
    plt.suptitle(f'Recursion Tree Analysis for n = {n}', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

def interactive_tree_explorer():
    """
    Interactive function to explore different recurrence relations
    """
    print_separator("=", title="INTERACTIVE RECURSION TREE EXPLORER")
    
    print("\n📚 Common Recurrence Relations:")
    print("1. Binary Search: T(n) = T(n/2) + 1")
    print("2. Merge Sort: T(n) = 2T(n/2) + n")
    print("3. Quick Sort (best): T(n) = 2T(n/2) + n")
    print("4. Strassen's Matrix: T(n) = 7T(n/2) + n²")
    print("5. Karatsuba: T(n) = 3T(n/2) + n")
    print("6. Custom: Enter your own")
    
    choice = input("\nSelect option (1-6): ").strip()
    
    configs = {
        '1': (1, 2, lambda x: 1, "Binary Search"),
        '2': (2, 2, lambda x: x, "Merge Sort"),
        '3': (2, 2, lambda x: x, "Quick Sort (best case)"),
        '4': (7, 2, lambda x: x**2, "Strassen's Algorithm"),
        '5': (3, 2, lambda x: x, "Karatsuba Multiplication")
    }
    
    if choice in configs:
        a, b, f, name = configs[choice]
    else:
        a = int(input("Enter a (number of subproblems): "))
        b = int(input("Enter b (size reduction factor): "))
        name = "Custom Recurrence"
        f = lambda x: x  # Default to linear
    
    n = int(input("Enter n (problem size, e.g., 16, 32, 64): "))
    
    print(f"\n🎯 Analyzing: T(n) = {a}T(n/{b}) + f(n)")
    
    # Detailed analysis
    levels_data = []
    level = 0
    max_levels = int(math.log(n) / math.log(b)) + 1
    
    print("\n" + "="*80)
    print(f"{'Level':<8} {'Nodes':<10} {'Size/Node':<12} {'Work/Node':<12} {'Total Work':<12} {'Visualization'}")
    print("="*80)
    
    total_work = 0
    max_work_level = 0
    
    for level in range(max_levels):
        num_nodes = a ** level
        size_per_node = n / (b ** level)
        work_per_node = f(size_per_node)
        level_work = num_nodes * work_per_node
        total_work += level_work
        
        if level_work > max_work_level:
            max_work_level = level_work
        
        # Create visualization bar
        bar_width = int(30 * (level_work / max_work_level)) if max_work_level > 0 else 0
        bar = "█" * bar_width + "░" * (30 - bar_width)
        
        print(f"{level:<8} {num_nodes:<10} {size_per_node:<12.2f} {work_per_node:<12.2f} {level_work:<12.2f} {bar}")
        
        levels_data.append({
            'level': level,
            'nodes': num_nodes,
            'size': size_per_node,
            'work': level_work
        })
    
    print("="*80)
    print(f"{'TOTAL':<8} {'':<10} {'':<12} {'':<12} {total_work:<12.2f}")
    print("="*80)
    
    # Complexity analysis
    log_b_a = math.log(a) / math.log(b)
    print(f"\n📊 Complexity Analysis:")
    print(f"   log_b(a) = log_{b}({a}) = {log_b_a:.3f}")
    print(f"   Total work: {total_work:.2f}")
    
    # Determine Master Theorem case
    if abs(log_b_a - 1) < 0.01:  # Case 2
        print(f"   Complexity: O(n log n)")
    elif log_b_a > 1:  # Case 1
        print(f"   Complexity: O(n^{log_b_a:.2f})")
    else:  # Case 3
        print(f"   Complexity: O(n)")
    
    return levels_data

def contrast_with_telescoping():
    """
    Show the key differences between recursion tree and telescoping methods
    """
    print_separator("=", title="RECURSION TREE vs TELESCOPING METHOD")
    
    print("\n📊 KEY DIFFERENCES:\n")
    
    print("1️⃣ PROBLEM TYPES:")
    print("   Telescoping: Best for T(n) = T(n-1) + f(n) [Linear recursion]")
    print("   Tree Method: Best for T(n) = aT(n/b) + f(n) [Divide & conquer]")
    
    print("\n2️⃣ VISUALIZATION:")
    print("   Telescoping: Linear expansion → 1D sequence")
    print("   Tree Method: Tree structure → 2D hierarchy")
    
    print("\n3️⃣ EXAMPLE COMPARISON:")
    
    # Telescoping example
    print("\n   📝 Telescoping (T(n) = T(n-1) + n):")
    print("      T(5) = T(4) + 5")
    print("           = T(3) + 4 + 5")
    print("           = T(2) + 3 + 4 + 5")
    print("           = T(1) + 2 + 3 + 4 + 5")
    print("           = 1 + 2 + 3 + 4 + 5 = 15")
    
    # Tree method example
    print("\n   🌳 Tree Method (T(n) = 2T(n/2) + n):")
    print("                    8           → Work: 8")
    print("                  /   \\")
    print("                4       4       → Work: 4 + 4 = 8")
    print("              /   \\   /   \\")
    print("            2     2 2     2     → Work: 2×4 = 8")
    print("           / \\   / \\ / \\   / \\")
    print("          1  1  1  1 1  1  1  1  → Work: 1×8 = 8")
    print("                                   Total: 32 = 8 × log₂(8)")
    
    print("\n4️⃣ WHEN TO USE EACH:")
    print("   ✅ Use Telescoping when:")
    print("      • Recurrence decreases by constant (n-1, n-2)")
    print("      • Simple linear structure")
    print("      • Looking for exact closed form")
    
    print("\n   ✅ Use Tree Method when:")
    print("      • Recurrence divides problem (n/2, n/3)")
    print("      • Multiple recursive calls")
    print("      • Analyzing divide-and-conquer algorithms")

def main():
    """
    Main demonstration program
    """
    print("\n" + "="*80)
    print(" RECURSION TREE METHOD: COMPREHENSIVE VISUALIZATION ".center(80))
    print("="*80)
    
    while True:
        print("\n🎯 MENU:")
        print("1. Step-by-step tree construction")
        print("2. ASCII tree visualization")
        print("3. Actual merge sort execution trace")
        print("4. Graphical tree visualization")
        print("5. Interactive tree explorer")
        print("6. Compare with telescoping method")
        print("7. Run complete demonstration")
        print("0. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            n = int(input("Enter n (e.g., 16, 32): "))
            step_by_step_tree_construction(n)
            
        elif choice == '2':
            n = int(input("Enter n: "))
            visualize_tree_ascii(n)
            
        elif choice == '3':
            size = int(input("Enter array size (e.g., 8): "))
            arr = list(range(size, 0, -1))  # Reverse sorted for demo
            compare_with_actual_execution(arr)
            
        elif choice == '4':
            n = int(input("Enter n: "))
            visualize_tree_graphically(n)
            
        elif choice == '5':
            interactive_tree_explorer()
            
        elif choice == '6':
            contrast_with_telescoping()
            
        elif choice == '7':
            # Run complete demonstration
            print("\n🚀 Running complete demonstration...")
            
            # 1. Basic tree construction
            step_by_step_tree_construction(16)
            input("\n[Press Enter to continue...]")
            
            # 2. ASCII visualization
            visualize_tree_ascii(16)
            input("\n[Press Enter to continue...]")
            
            # 3. Actual execution
            arr = [8, 3, 5, 4, 7, 6, 1, 2]
            compare_with_actual_execution(arr)
            input("\n[Press Enter to continue...]")
            
            # 4. Graphical visualization
            visualize_tree_graphically(16)
            
            # 5. Comparison
            contrast_with_telescoping()
            
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
