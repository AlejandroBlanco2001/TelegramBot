import networkx as nx
import numpy as np
import sympy as sp
import random

# Sympy parser use for reading all the natural expresion
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))

"""
Function that return a simple graph

vertices : Number of vertices
edges: Number of edges
maximum_degree: Maximum degree number for the vertices
"""
def generate_graph(vertices : int, edges: int, maximum_grade: int) -> nx.Graph:
    if edges > maximum_grade*vertices/2:
        return None
    elif edges > vertices*(vertices-1)/2: # Test more edges than a complete graph
        return None
    elif edges == vertices*(vertices-1)/2: # Complete graph
        return nx.complete_graph(vertices)
    else:
        while True:
            sequence = generate_degree_sequence(vertices,edges,maximum_grade)
            try:
                G = nx.random_degree_sequence_graph(sequence)
                return G
            except Exception:
                pass

"""
Function that generates a random list with the degrees of a simple graph
taking the limit of the maximum vertice degree.

This use the Handshaking Lemma to ensure the existence of the simple graph

Handshaking Lemma: The sum of all the vertices degree must be equal to 
two times the number of edges, for a simple graph

vertices : Number of vertices
edges: Number of edges
maximum_degree: Maximum degree number for the vertices
"""
def generate_degree_sequence(vertices : int, edges: int, maximum_grade: int) -> list:
    accumulate_degree = 0
    degree_sequence = [0] * vertices
    for i in range(vertices): 
        if accumulate_degree == 2 * edges: # Handshaking lemma
            continue
        degree_sequence[i] = random.randint(0,min(vertices-1,maximum_grade,edges,2*edges-accumulate_degree))
        accumulate_degree += degree_sequence[i]  
    return degree_sequence

"""
Function that generates the solution of recurrency relation
given his characteristical polynomial in terms of constants

equation : String that represents the characteristical polynomial
"""
def resolve_characteristical_polynomial(equation : str) -> sp.Function : 
    x = sp.symbols('x')
    f = parse_expr(equation, transformations=transformations) 
    roots = sp.solve(f,x)
    mults = {root:roots.count(root) for root in roots}
    function_ans = list()
    term = 0
    for root in mults:
        part_per_coef = list()
        multiplicty = mults.get(root)
        for i in range(multiplicty):
            part_per_coef.append("c_" + str(term) + "*" + "n^" + str(i)) 
            term = term + 1
        function_ans.append("("+"+".join(part_per_coef) + ")" + "(" + str(root) + ")" + "^n")
    ans = "+".join(function_ans)
    y = parse_expr(ans,transformations=transformations)
    return y    

"""
Function that generates the solution of recurrency relation
given his characteristical polynomial

equation : String that represents the characteristical polynomial
initial_values: base cases of the recurrence relation
"""
def resolve_characteristical_polynomial_initial_value(equation : str, initial_values: int) -> sp.Function :
    n = sp.symbols('n')
    initial_values = [int(item) for item in initial_values.split(",")]
    print(initial_values)
    function_with_constants = resolve_characteristical_polynomial(equation)
    equations = []
    term = 0
    for value in initial_values:
        equations.append(sp.Eq(function_with_constants.subs(n,term),value))    
        term = term + 1
    value_constants = sp.solve(equations)
    for constant in value_constants:
        function_with_constants = function_with_constants.subs(constant,value_constants[constant])
    return function_with_constants
"""
Function that given a sequence of numbers in ascending order
finds one subsequence that follows the Fibonacci sequence principle

Fibonacci sequence principle: The next number of the sequence
is the sum of the two preview number. F_n = F_n-1 - F_n-2 

sequence: List that contains the sequence
"""
def sub_fibonacci_sequence(sequence: list) -> list:
    ans = list()
    full_list = list()
    for i in range(len(sequence)-1):
        for j in range(i+1,len(sequence)-1):
            if len(ans) == 0:
                ans = [sequence[i],sequence[j]]
            curr = ans[-1] + ans[-2]
            while curr in sequence:
                ans.append(curr)
                curr = ans[-1] + ans[-2]
            if len(ans) > 2:
                full_list.append(ans)
            ans = list()
    if len(full_list) == 1:
        return full_list[0]
    else:
        return full_list[np.random.randint(0,len(full_list))]

"""
Logic function that checks if the a sequence of number is in
ascending order

sequence: List containing the sequence of numbers
"""
def checkOrder(sequence: list) -> bool:
    for i in range(len(sequence)-1):
        if sequence[i] > sequence[i+1] :
            return False
    return True