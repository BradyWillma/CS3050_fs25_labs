import math

def master_method_analyzer(a, b, f_n, n, f_description="f(n)"):
    """
    Analyzes recurrence using Master Method
    T(n) = a*T(n/b) + f(n)
    """
    print(f"\n{'='*60}")
    print(f"Master Method Analysis")
    print(f"Recurrence: T(n) = {a}*T(n/{b}) + {f_description}")
    print(f"{'='*60}")
    
    # Calculate log_b(a)
    log_b_a = math.log(a) / math.log(b)
    
    print(f"\nKey values:")
    print(f"a = {a} (number of subproblems)")
    print(f"b = {b} (size reduction factor)")
    print(f"log_b(a) = log_{b}({a}) = {log_b_a:.3f}")
    print(f"n^(log_b(a)) = n^{log_b_a:.3f}")
    
    # Determine which case applies
    # For demonstration, we'll check at a specific n value
    n_test = 1000
    f_n_value = f_n(n_test)
    n_log_b_a = n_test ** log_b_a
    
    ratio = f_n_value / n_log_b_a
    
    print(f"\nAt n = {n_test}:")
    print(f"f(n) = {f_n_value:.2f}")
    print(f"n^(log_b(a)) = {n_log_b_a:.2f}")
    print(f"Ratio f(n)/n^(log_b(a)) = {ratio:.6f}")
    
    # Determine case
    if ratio < 0.5:  # Simplified check for demonstration
        print("\n**CASE 1: Subproblems dominate**")
        print("f(n) is polynomially smaller than n^(log_b(a))")
        print("The work is concentrated in the leaves of recursion tree")
        print(f"Solution: T(n) = Θ(n^{log_b_a:.3f})")
        return 1, log_b_a
    elif 0.5 <= ratio <= 2:  # Simplified check
        print("\n**CASE 2: Balanced (tie)**")
        print("f(n) and n^(log_b(a)) are the same order")
        print("Work is evenly distributed across all levels")
        print(f"Solution: T(n) = Θ(n^{log_b_a:.3f} * log n)")
        return 2, log_b_a
    else:
        print("\n**CASE 3: Outside work dominates**")
        print("f(n) is polynomially larger than n^(log_b(a))")
        print("The work at the root dominates")
        print(f"Solution: T(n) = Θ({f_description})")
        return 3, None

# Demonstrate all three cases
print("\n" + "="*70)
print("MASTER METHOD: THREE CASES DEMONSTRATION")
print("="*70)

# CASE 1: Subproblems dominate
print("\n--- Example 1: Binary Search Tree Operations ---")
master_method_analyzer(2, 2, lambda x: 1, 1000, "1")
print("\nInterpretation: Most work happens in recursive calls (searching subtrees)")

# CASE 2: Tie
print("\n--- Example 2: Merge Sort ---")
master_method_analyzer(2, 2, lambda x: x, 1000, "n")
print("\nInterpretation: Work at each level (merging) equals recursive work")

# CASE 3: Outside work dominates
print("\n--- Example 3: Sloppy Recursive Algorithm ---")
master_method_analyzer(2, 2, lambda x: x**2, 1000, "n²")
print("\nInterpretation: The n² work at each call dominates the recursion")


def master_method_demo():
    """
    Interactive demonstration showing why each case occurs
    """
    print("\n" + "="*70)
    print("MASTER METHOD: INTUITIVE UNDERSTANDING")
    print("="*70)
    
    def show_work_distribution(a, b, f_func, f_name, n=32):
        """Show how work is distributed across recursion levels"""
        levels = int(math.log(n) / math.log(b)) + 1
        log_b_a = math.log(a) / math.log(b)
        
        print(f"\nT(n) = {a}T(n/{b}) + {f_name}")
        print(f"For n = {n}:")
        print("\nLevel | Size | # Nodes | f(size) | Level Work")
        print("-" * 55)
        
        total_work = 0
        level_works = []
        
        for level in range(levels):
            size = n / (b ** level)
            num_nodes = a ** level
            f_value = f_func(size) if size >= 1 else 0
            level_work = num_nodes * f_value
            level_works.append(level_work)
            total_work += level_work
            
            bar = "█" * int(20 * level_work / max(level_works + [1]))
            print(f"{level:5} | {size:4.0f} | {num_nodes:7} | {f_value:7.1f} | {level_work:10.1f} {bar}")
        
        print("-" * 55)
        print(f"Total: {total_work:.1f}")
        
        # Determine dominant portion
        leaf_work = level_works[-1] if level_works else 0
        root_work = level_works[0] if level_works else 0
        
        if leaf_work > 0.5 * total_work:
            print("➜ CASE 1: Leaves dominate (bottom-heavy)")
        elif root_work > 0.5 * total_work:
            print("➜ CASE 3: Root dominates (top-heavy)")
        else:
            print("➜ CASE 2: Balanced across levels")
    
    print("\n1️⃣ CASE 1: Subproblems Dominate (Bottom-Heavy Tree)")
    show_work_distribution(4, 2, lambda x: x, "n", 32)
    
    print("\n2️⃣ CASE 2: Balanced Work (Equal at All Levels)")
    show_work_distribution(2, 2, lambda x: x, "n", 32)
    
    print("\n3️⃣ CASE 3: Outside Work Dominates (Top-Heavy Tree)")
    show_work_distribution(2, 2, lambda x: x**2, "n²", 32)

master_method_demo()