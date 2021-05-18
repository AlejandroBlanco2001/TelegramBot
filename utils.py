import networkx as nx
import numpy as np
import sympy as sp

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
        sequence = generate_degree_sequence(vertices,edges,maximum_grade)
        try:
            G = nx.random_degree_sequence_graph(sequence)
        except Exception:
            return None
    return G

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
    degree_sequence = np.random.randint(maximum_grade+1, size=(vertices)) 
    while sum(degree_sequence) != edges*2: # Handshake lemma
        degree_sequence = np.random.randint(maximum_grade+1, size=(vertices))        
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
# Terminar mañana
def resolve_characteristical_polynomial_initial_value(equation : str, initial_values: int) -> sp.Function :
    n = sp.symbols('n')
    function_with_constants = resolve_characteristical_polynomial(equation)
    for value in initial_values:
        print(function_with_constants.subs(n,value))
        
"""

"""
def sub_fibonacci_sequence(sequence: list) -> list:
    ans = list()
    inc = 1
    full_list = list()
    for i in range(len(sequence)-1):
        ans.extend([sequence[i],sequence[i+inc]])
        next_number = ans[-1] + ans[-2]
        while next_number in sequence:
            ans.append(next_number)
        if ans > 2:
            full_list.append(ans)
        ans.clear()
    return full_list

"""
Comentar mañana / más tarde
"""
def checkOrder(sequence: list) -> bool:
    for i in range(len(sequence)-1):
        if sequence[i] > sequence[i+1] :
            return False
    return True