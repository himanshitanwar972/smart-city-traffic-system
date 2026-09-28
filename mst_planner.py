from graph_utils import generate_sample_graph

def prim_mst(graph):
    """
    Manual implementation of Prim's Algorithm for Minimum Spanning Tree.
    Returns the selected edges and the total cost of the MST.
    """
    nodes = list(graph.nodes())
    if not nodes:
        return [], 0
        
    start_node = nodes[0]
    visited = set([start_node])
    mst_edges = []
    total_cost = 0
    
    # Loop until all nodes are visited (assuming graph is connected)
    while len(visited) < len(nodes):
        min_edge = None
        min_weight = float('inf')
        
        # Find the minimum weight edge connecting the visited set to an unvisited node
        for u in visited:
            for v in graph.neighbors(u):
                if v not in visited:
                    weight = graph[u][v].get('weight', 1)
                    if weight < min_weight:
                        min_weight = weight
                        min_edge = (u, v, weight)
                        
        if min_edge is None:
            # Graph is disconnected, cannot form a full MST
            break
            
        u, v, weight = min_edge
        visited.add(v)
        mst_edges.append((u, v, weight))
        total_cost += weight
        
    return mst_edges, total_cost


def kruskal_mst(graph):
    """
    Manual implementation of Kruskal's Algorithm for Minimum Spanning Tree.
    Uses a Disjoint Set (Union-Find) to detect cycles.
    Returns the selected edges and the total cost of the MST.
    """
    nodes = list(graph.nodes())
    edges_with_weights = []
    
    # Extract unique edges and weights
    added_edges = set()
    for u, v, data in graph.edges(data=True):
        # Sort node tuple to handle undirected nature
        edge_id = tuple(sorted((u, v))) 
        if edge_id not in added_edges:
            edges_with_weights.append((u, v, data.get('weight', 1)))
            added_edges.add(edge_id)
            
    # Sort edges by weight in ascending order
    edges_with_weights.sort(key=lambda x: x[2])
    
    # --- Disjoint Set (Union-Find) Data Structure ---
    parent = {node: node for node in nodes}
    
    def find(i):
        if parent[i] == i:
            return i
        parent[i] = find(parent[i]) # Path compression
        return parent[i]
        
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False
    # ------------------------------------------------
        
    mst_edges = []
    total_cost = 0
    
    # Process edges in increasing order of weight
    for u, v, weight in edges_with_weights:
        # If including this edge doesn't cause a cycle
        if union(u, v):
            mst_edges.append((u, v, weight))
            total_cost += weight
            
            # Stop early if we have included V-1 edges
            if len(mst_edges) == len(nodes) - 1:
                break
                
    return mst_edges, total_cost


if __name__ == "__main__":
    print("--- Testing MST Planners ---")
    G = generate_sample_graph(6)
    
    print("\n--- Prim's Algorithm ---")
    prim_edges, prim_cost = prim_mst(G)
    print(f"Selected Edges: {prim_edges}")
    print(f"Total MST Cost: {prim_cost}")
    
    print("\n--- Kruskal's Algorithm ---")
    kruskal_edges, kruskal_cost = kruskal_mst(G)
    print(f"Selected Edges: {kruskal_edges}")
    print(f"Total MST Cost: {kruskal_cost}")
