# File that have all the auxilary functionss
import networkx as nx
import numpy as np
"""
    vertices : int of vertices
    edges: int of edges
    maximu_degree: Maximum degree for the vertices
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

def generate_degree_sequence(vertices : int, edges: int, maximum_grade: int) -> list:
    accumulate_degree = 0
    degree_sequence = np.random.randint(1,maximum_grade, size=(vertices))
    while sum(degree_sequence) != edges*2:
        degree_sequence = np.random.randint(1,maximum_grade, size=(vertices))        
    return degree_sequence
    