import networkx as nx
import random
import pandas as pd
import numpy as np

def create_empty_graph():
    """Returns a new empty undirected graph."""
    return nx.Graph()

def add_node(graph, node):
    """Adds a single node to the graph."""
    graph.add_node(node)

def add_edge(graph, u, v, weight=1):
    """Adds a weighted undirected edge to the graph."""
    graph.add_edge(u, v, weight=weight)

def generate_sample_graph(n_nodes):
    """
    Generates a random connected weighted graph with n nodes.
    Uses NetworkX purely for structure, not for generation algorithms.
    """
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))
    nodes = list(G.nodes)
    
    if n_nodes <= 1:
        return G
        
    # Ensure it's connected by building a spanning tree first
    connected = [nodes[0]]
    unconnected = nodes[1:]
    
    while unconnected:
        u = random.choice(connected)
        v = random.choice(unconnected)
        weight = random.randint(1, 20)
        G.add_edge(u, v, weight=weight)
        connected.append(v)
        unconnected.remove(v)
        
    # Add some random extra edges to simulate alternative routes
    extra_edges = random.randint(0, n_nodes)
    for _ in range(extra_edges):
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u != v and not G.has_edge(u, v):
            weight = random.randint(1, 20)
            G.add_edge(u, v, weight=weight)
            
    return G

def get_adjacency_list(graph):
    """Returns the adjacency list representation of the graph."""
    adj_list = {}
    for node in graph.nodes():
        adj_list[node] = list(graph.neighbors(node))
    return adj_list

def get_adjacency_matrix(graph):
    """Returns the adjacency matrix as a pandas DataFrame."""
    nodes = list(graph.nodes())
    # Initialize with zeros
    matrix = np.zeros((len(nodes), len(nodes)))
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    for u, v, data in graph.edges(data=True):
        i, j = node_to_idx[u], node_to_idx[v]
        weight = data.get('weight', 1)
        matrix[i][j] = weight
        matrix[j][i] = weight # Undirected
        
    df = pd.DataFrame(matrix, index=nodes, columns=nodes)
    return df

if __name__ == "__main__":
    print("--- Testing Graph Utils ---")
    G = generate_sample_graph(5)
    print("Nodes:", G.nodes())
    print("Edges:", G.edges(data=True))
    
    print("\nAdjacency List:")
    print(get_adjacency_list(G))
    
    print("\nAdjacency Matrix:")
    print(get_adjacency_matrix(G))
