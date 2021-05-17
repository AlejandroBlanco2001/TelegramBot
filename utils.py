import networkx as nx
import numpy as np
import sympy as sp

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
    elif edges > vertices*(vertices-1)/2:
        return None
    elif edges == vertices*(vertices-1)/2:
        return nx.complete_graph(vertices)
    else:
        sequence = generate_degree_sequence(vertices,edges,maximum_grade)
        try:
            G = nx.random_degree_sequence_graph(sequence)
        except Exception:
            pass
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
    degree_sequence = np.random.randint(1,maximum_grade, size=(vertices))
    while sum(degree_sequence) != edges*2: # Handshake lema
        degree_sequence = np.random.randint(1,maximum_grade, size=(vertices))        
    return degree_sequence

"""
Function that generates the solution of recurrency relation
given his characteristical polynomial

equation : String that represents the characteristical polynomial
"""
def resolve_characteristical_polynomial(equation : str) -> list : 
    x = sp.symbols('x')
    f = parse_expr(equation, transformations=transformations)
    roots = sp.solve(f,x)
    mult = {root:roots.count(root) for root in roots}
    print(mult)