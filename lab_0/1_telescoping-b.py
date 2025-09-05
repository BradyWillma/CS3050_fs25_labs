"""
Key Features:

Step-by-Step Expansion: Shows exactly how T(n) = T(n-1) + n expands term by term
Telescoping Cancellation Visualization: Demonstrates how terms cancel in the telescoping process
Calculation Table: Builds a table showing cumulative sums at each step
Expansion Tree: Visualizes the recursion as a tree structure
Actual Recursion Trace: Shows the real call stack as the recursion executes
Comparison Analysis: Compares recursive calculation with the closed-form formula
Complexity Plots: Four different graphs showing the O(n²) behavior

How to Use:

Run the script and it will walk through each visualization step-by-step
Press Enter to move between sections
The script pauses at each major concept so students can understand before moving on

Example Output:
The script will show things like:
```
Step 3.1: T(8) = T(7) + 8
Step 3.2: T(8) = T(6) + 7 + 8
Step 3.3: T(8) = T(5) + 6 + 7 + 8
...
Final: T(8) = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 = 36
```
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple
import pandas as pd

class TelescopingVisualizer:
    """
    A class to visualize the telescoping method step by step
    """
    
    def __init__(self):
        self.expansion_steps = []
        self.computation_trace = []
        
    def clear(self):
        """Reset the visualizer"""
        self.expansion_steps = []
        self.computation_trace = []

def print_separator(char="=", length=70):
    """Helper function to print separators"""
    print(char * length)

def recursive_sum_traced(n, depth=0, trace_list=None):
    """
    Recursive sum with detailed tracing to show actual computation
    """
    if trace_list is None:
        trace_list = []
    
    indent = "  " * depth
    
    if n <= 1:
        trace_list.append((depth, n, f"{indent}T(1) = 1"))
        return 1, trace_list
    
    # Record the current call
    trace_list.append((depth, n, f"{indent}T({n}) = T({n-1}) + {n}"))
    
    # Recursive call
    result_recursive, _ = recursive_sum_traced(n-1, depth+1, trace_list)
    
    # Compute result
    result = result_recursive + n
    trace_list.append((depth, n, f"{indent}T({n}) = {result_recursive} + {n} = {result}"))
    
    return result, trace_list

def demonstrate_telescoping_expansion(n: int):
    """
    Show the telescoping expansion step by step
    """
    print_separator("=")
    print(f"TELESCOPING METHOD: Step-by-Step Expansion for T(n) = T(n-1) + n")
    print(f"Solving for n = {n}")
    print_separator("=")
    
    print("\n📝 Step 1: Write the original recurrence")
    print(f"   T({n}) = T({n-1}) + {n}")
    
    print("\n📝 Step 2: Expand T(n-1)")
    print(f"   T({n-1}) = T({n-2}) + {n-1}")
    print(f"   So: T({n}) = [T({n-2}) + {n-1}] + {n}")
    print(f"       T({n}) = T({n-2}) + {n-1} + {n}")
    
    print("\n📝 Step 3: Continue expanding...")
    
    # Show progressive expansion
    terms = []
    for i in range(min(4, n-1)):  # Show first 4 expansions
        remaining = n - i - 1
        current_terms = [str(n-j) for j in range(i+1)]
        terms_str = " + ".join(current_terms)
        
        if remaining > 1:
            print(f"   Step 3.{i+1}: T({n}) = T({remaining}) + {terms_str}")
        else:
            print(f"   Step 3.{i+1}: T({n}) = T(1) + {terms_str}")
    
    if n > 5:
        print(f"   ...")
    
    # Final expansion
    print(f"\n📝 Step 4: Complete expansion (base case T(1) = 1)")
    all_terms = [str(i) for i in range(1, n+1)]
    print(f"   T({n}) = {' + '.join(all_terms)}")
    
    # Calculate sum
    print(f"\n📝 Step 5: Calculate the sum")
    print(f"   T({n}) = 1 + 2 + 3 + ... + {n}")
    print(f"   T({n}) = Σ(i) from i=1 to {n}")
    print(f"   T({n}) = n(n+1)/2")
    print(f"   T({n}) = {n}×{n+1}/2")
    print(f"   T({n}) = {n*(n+1)//2}")
    
    return n * (n + 1) // 2

def visualize_telescoping_cancellation(n: int):
    """
    Visualize how terms telescope (cancel) in certain recurrences
    """
    print_separator("=")
    print(f"TELESCOPING CANCELLATION VISUALIZATION")
    print(f"Example: T(n) = T(n-1) + 1/n  (different recurrence for demonstration)")
    print_separator("=")
    
    print("\n📊 Showing how terms might cancel in telescoping:")
    print("When we have: T(n) - T(n-1) = f(n)")
    print("We can write:")
    
    equations = []
    for i in range(n, max(1, n-5), -1):
        if i > 1:
            eq = f"T({i}) - T({i-1}) = f({i})"
            equations.append(eq)
            print(f"   {eq}")
    
    if n > 6:
        print("   ...")
    print("   T(2) - T(1) = f(2)")
    
    print("\n➕ Adding all equations (left sides and right sides):")
    print("   Left side:  T(n) - T(1)  (middle terms cancel!)")
    print(f"   Right side: f(2) + f(3) + ... + f({n})")
    print(f"\n✨ Result: T(n) = T(1) + Σf(i) from i=2 to {n}")

def create_step_by_step_table(n: int):
    """
    Create a table showing the step-by-step calculation
    """
    print_separator("=")
    print(f"STEP-BY-STEP CALCULATION TABLE for n = {n}")
    print_separator("=")
    
    # Build the table data
    data = []
    cumulative_sum = 0
    
    print("\n| Step | Current Term | Cumulative Sum | Calculation |")
    print("|------|-------------|----------------|-------------|")
    
    for i in range(1, n+1):
        cumulative_sum += i
        calculation = f"{cumulative_sum-i} + {i}"
        if i == 1:
            calculation = "1"
        
        data.append({
            'Step': i,
            'Term': i,
            'Cumulative': cumulative_sum,
            'Calculation': calculation
        })
        
        print(f"| {i:4} | {i:11} | {cumulative_sum:14} | {calculation:11} |")
    
    print(f"\n✅ Final result: T({n}) = {cumulative_sum}")
    print(f"✅ Formula check: n(n+1)/2 = {n}×{n+1}/2 = {n*(n+1)//2}")
    
    return pd.DataFrame(data)

def visualize_expansion_tree(n: int):
    """
    Show the expansion as a tree structure
    """
    print_separator("=")
    print(f"EXPANSION TREE VISUALIZATION for n = {n}")
    print_separator("=")
    
    print("\n🌳 Recursion/Expansion Tree:")
    
    # Show the tree structure
    max_depth = min(n-1, 6)  # Limit depth for display
    
    for depth in range(max_depth + 1):
        indent = "  " * depth
        value = n - depth
        
        if value > 1:
            print(f"{indent}T({value})")
            print(f"{indent}├── T({value-1})")
            print(f"{indent}└── +{value}")
        else:
            print(f"{indent}T(1) = 1 [base case]")
    
    if n > 7:
        print("  " * (max_depth + 1) + "...")

def compare_recursive_vs_formula(max_n: int = 20):
    """
    Compare recursive calculation with formula
    """
    print_separator("=")
    print("COMPARING RECURSIVE CALCULATION VS FORMULA")
    print_separator("=")
    
    print("\n| n  | Recursive | Formula | Match | Time (recursive) |")
    print("|----|-----------|---------|-------|-----------------|")
    
    recursive_times = []
    formula_times = []
    
    for n in range(1, min(max_n + 1, 21)):
        # Recursive calculation with timing
        start = time.perf_counter()
        recursive_result = sum(range(1, n+1))  # Simpler for timing
        recursive_time = time.perf_counter() - start
        recursive_times.append(recursive_time * 1000000)  # Convert to microseconds
        
        # Formula calculation with timing
        start = time.perf_counter()
        formula_result = n * (n + 1) // 2
        formula_time = time.perf_counter() - start
        formula_times.append(formula_time * 1000000)
        
        match = "✓" if recursive_result == formula_result else "✗"
        
        print(f"| {n:2} | {recursive_result:9} | {formula_result:7} | {match:5} | {recursive_time*1000000:15.3f}μs |")
    
    return recursive_times, formula_times

def plot_complexity_analysis():
    """
    Create visual plots showing the O(n²) complexity
    """
    print_separator("=")
    print("COMPLEXITY ANALYSIS PLOTS")
    print_separator("=")
    
    # Generate data
    n_values = np.array([5, 10, 15, 20, 25, 30, 35, 40])
    actual_values = [n * (n + 1) // 2 for n in n_values]
    n_squared = n_values ** 2
    n_squared_half = n_squared / 2
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Actual values
    axes[0, 0].plot(n_values, actual_values, 'bo-', label='T(n) = n(n+1)/2', linewidth=2)
    axes[0, 0].set_xlabel('n')
    axes[0, 0].set_ylabel('T(n)')
    axes[0, 0].set_title('Actual Recurrence Solution')
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].legend()
    
    # Plot 2: Comparison with n² and n²/2
    axes[0, 1].plot(n_values, actual_values, 'bo-', label='T(n) = n(n+1)/2', linewidth=2)
    axes[0, 1].plot(n_values, n_squared, 'r--', label='n²', alpha=0.7)
    axes[0, 1].plot(n_values, n_squared_half, 'g--', label='n²/2', alpha=0.7)
    axes[0, 1].set_xlabel('n')
    axes[0, 1].set_ylabel('Value')
    axes[0, 1].set_title('T(n) vs n² Comparison')
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].legend()
    
    # Plot 3: Log scale to show polynomial growth
    axes[1, 0].loglog(n_values, actual_values, 'bo-', label='T(n)', linewidth=2)
    axes[1, 0].loglog(n_values, n_squared, 'r--', label='n²', alpha=0.7)
    axes[1, 0].loglog(n_values, n_values, 'g--', label='n', alpha=0.7)
    axes[1, 0].set_xlabel('n (log scale)')
    axes[1, 0].set_ylabel('T(n) (log scale)')
    axes[1, 0].set_title('Log-Log Plot (slope = 2 indicates O(n²))')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].legend()
    
    # Plot 4: Terms visualization
    n_demo = 10
    terms = list(range(1, n_demo + 1))
    positions = list(range(1, n_demo + 1))
    axes[1, 1].bar(positions, terms, color='skyblue', edgecolor='navy')
    axes[1, 1].set_xlabel('Term index')
    axes[1, 1].set_ylabel('Term value')
    axes[1, 1].set_title(f'Individual terms for n={n_demo}: sum = {sum(terms)}')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    # Add cumulative sum line
    cumsum = np.cumsum(terms)
    ax2 = axes[1, 1].twinx()
    ax2.plot(positions, cumsum, 'ro-', label='Cumulative sum')
    ax2.set_ylabel('Cumulative sum', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    plt.suptitle('Telescoping Method: T(n) = T(n-1) + n Analysis', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def trace_actual_recursion(n: int):
    """
    Trace the actual recursive calls showing the call stack
    """
    print_separator("=")
    print(f"ACTUAL RECURSION TRACE for n = {n}")
    print_separator("=")
    
    result, trace = recursive_sum_traced(n)
    
    print("\n📞 Call Stack Trace:")
    for depth, value, message in trace:
        print(message)
    
    print(f"\n✅ Final result: {result}")
    print(f"✅ Formula verification: {n}×({n}+1)/2 = {n*(n+1)//2}")

def main():
    """
    Main demonstration function
    """
    print("\n" + "="*70)
    print(" TELESCOPING METHOD: COMPREHENSIVE VISUALIZATION ".center(70))
    print("="*70)
    
    # Choose n value for demonstration
    n = 8
    
    # 1. Show step-by-step expansion
    result1 = demonstrate_telescoping_expansion(n)
    input("\n[Press Enter to continue to cancellation visualization...]")
    
    # 2. Show telescoping cancellation concept
    visualize_telescoping_cancellation(n)
    input("\n[Press Enter to continue to calculation table...]")
    
    # 3. Create calculation table
    df = create_step_by_step_table(n)
    input("\n[Press Enter to continue to expansion tree...]")
    
    # 4. Show expansion tree
    visualize_expansion_tree(n)
    input("\n[Press Enter to continue to recursion trace...]")
    
    # 5. Trace actual recursion
    trace_actual_recursion(n)
    input("\n[Press Enter to continue to comparison...]")
    
    # 6. Compare recursive vs formula
    compare_recursive_vs_formula(15)
    input("\n[Press Enter to see complexity plots...]")
    
    # 7. Plot complexity analysis
    plot_complexity_analysis()
    
    print("\n" + "="*70)
    print(" DEMONSTRATION COMPLETE ".center(70))
    print("="*70)
    
    # Summary
    print("\n📚 KEY TAKEAWAYS:")
    print("1. Telescoping expands the recurrence by substituting repeatedly")
    print("2. For T(n) = T(n-1) + n, we get the sum 1 + 2 + ... + n")
    print("3. This sum equals n(n+1)/2, which is O(n²)")
    print("4. The method reveals the exact closed-form solution")
    print("5. Visualization helps understand where the complexity comes from")

if __name__ == "__main__": 
    main()