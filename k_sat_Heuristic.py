"""
This script generates a random k-SAT problem with a specified number of clauses, literals per clause, and variables.
It uses the concepts of Constraint Satisfaction Problems (CSPs) as explained in Stuart Russell's "Artificial Intelligence: A Modern Approach".

Functions:
- create_k_SAT_problem(num_clauses, literals_per_clause, num_variables): Generates a k-SAT problem with randomly selected literals.
- get_inputs(): Retrieves user inputs for the number of clauses, literals per clause, and total number of variables.
- main(): Main function to generate the k-SAT problem and display it.

Variable Naming:
- num_clauses: Number of clauses to be generated.
- literals_per_clause: Number of literals per clause.
- num_variables: Number of distinct variables.
- positive_literals: List of lowercase letters representing positive literals.
- negative_literals: List of uppercase letters representing negated literals.
- all_literals: Combined list of positive and negative literals.
"""

from string import ascii_lowercase
import random

def create_k_SAT_problem(num_clauses, literals_per_clause, num_variables):
    positive_literals = list(ascii_lowercase[:num_variables])
    negative_literals = [literal.upper() for literal in positive_literals]
    
    all_literals = positive_literals + negative_literals
    clauses = []
    
    for _ in range(num_clauses):
        clause = set()
        
        while len(clause) < literals_per_clause:
            literal = random.choice(all_literals)
            if literal.lower() in [lit.lower() for lit in clause]:
                continue
            clause.add(literal)
        
        clauses.append(list(clause))
    
    return clauses

def get_inputs():
    num_clauses = int(input("Enter the number of clauses (num_clauses): "))
    literals_per_clause = int(input("Enter the number of literals per clause (literals_per_clause): "))
    num_variables = int(input("Enter the total number of variables (num_variables): "))
    
    if literals_per_clause > num_variables:
        raise ValueError("The number of literals per clause cannot exceed the total number of variables.")
    
    return num_clauses, literals_per_clause, num_variables

def main():
    print("k-SAT Problem Generator - Based on Stuart Russell's AI Approach")
    
    num_clauses, literals_per_clause, num_variables = get_inputs()
    
    k_SAT_problem = create_k_SAT_problem(num_clauses, literals_per_clause, num_variables)
    
    print("\nGenerated k-SAT Problem:")
    for idx, clause in enumerate(k_SAT_problem):
        print(f"Clause {idx + 1}: {clause}")

if __name__ == "__main__":
    main()
