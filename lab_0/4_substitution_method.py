import math 

def substitution_method_demo():
    """
    Demonstrate the substitution method with step-by-step verification
    """
    print("\n" + "="*70)
    print("SUBSTITUTION METHOD DEMONSTRATION")
    print("="*70)
    
    print("\nExample: T(n) = 2T(n/2) + n")
    print("Step 1: Guess that T(n) = O(n log n)")
    print("        So we guess T(n) ≤ cn log n for some constant c > 0")
    
    print("\nStep 2: Verify by substitution")
    print("Assume T(k) ≤ ck log k for all k < n")
    print("\nSubstitute into recurrence:")
    print("T(n) = 2T(n/2) + n")
    print("     ≤ 2(c(n/2)log(n/2)) + n")
    print("     = cn(log n - log 2) + n")
    print("     = cn log n - cn + n")
    print("     = cn log n - (c-1)n")
    
    print("\nFor T(n) ≤ cn log n to hold, we need:")
    print("cn log n - (c-1)n ≤ cn log n")
    print("-(c-1)n ≤ 0")
    print("(c-1)n ≥ 0")
    print("c ≥ 1")
    
    print("\nStep 3: Verify with actual values")
    
    def verify_substitution(n_values):
        """Verify our guess T(n) ≤ cn log n with c = 2"""
        c = 2
        print(f"\nUsing c = {c}:")
        print("n    | T(n) actual | cn log n | Valid?")
        print("-" * 45)
        
        def T(n):
            if n <= 1:
                return 1
            return 2 * T(n // 2) + n
        
        for n in n_values:
            actual = T(n)
            bound = c * n * math.log2(n) if n > 1 else c
            valid = "✓" if actual <= bound else "✗"
            print(f"{n:4} | {actual:11.1f} | {bound:8.1f} | {valid}")
    
    verify_substitution([2, 4, 8, 16, 32, 64])
    
    print("\n✓ Substitution method confirms: T(n) = O(n log n)")

substitution_method_demo()

def substitution_method_detailed():
    """
    More detailed substitution method with different complexities
    """
    print("\n" + "="*70)
    print("SUBSTITUTION METHOD: MULTIPLE EXAMPLES")
    print("="*70)
    
    # Example 1: Linear recurrence
    print("\n📝 Example 1: T(n) = T(n-1) + 1")
    print("Guess: T(n) = O(n)")
    print("Assume: T(k) ≤ ck for k < n")
    print("\nSubstitution:")
    print("T(n) = T(n-1) + 1")
    print("     ≤ c(n-1) + 1")
    print("     = cn - c + 1")
    print("     ≤ cn  (when c ≥ 1)")
    print("✓ Verified: T(n) = O(n)")
    
    # Example 2: Quadratic recurrence
    print("\n📝 Example 2: T(n) = T(n/2) + n²")
    print("Guess: T(n) = O(n²)")
    print("Assume: T(k) ≤ ck² for k < n")
    print("\nSubstitution:")
    print("T(n) = T(n/2) + n²")
    print("     ≤ c(n/2)² + n²")
    print("     = cn²/4 + n²")
    print("     = n²(c/4 + 1)")
    print("     ≤ cn²  (when c ≥ 4/3)")
    print("✓ Verified: T(n) = O(n²)")
    
    # Example 3: Failed guess
    print("\n📝 Example 3: T(n) = 2T(n/2) + n log n")
    print("First guess: T(n) = O(n log n) -- Let's see if this works")
    print("Assume: T(k) ≤ ck log k for k < n")
    print("\nSubstitution:")
    print("T(n) = 2T(n/2) + n log n")
    print("     ≤ 2c(n/2)log(n/2) + n log n")
    print("     = cn(log n - 1) + n log n")
    print("     = cn log n - cn + n log n")
    print("     = (c+1)n log n - cn")
    print("✗ This is NOT ≤ cn log n")
    print("\nRevised guess: T(n) = O(n log² n)")
    print("✓ This would work (left as exercise)")

substitution_method_detailed()