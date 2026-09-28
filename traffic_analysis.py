from graph_utils import generate_sample_graph

def bellman_ford(graph, src, dst):
    """
    Manual implementation of the Bellman-Ford algorithm.
    Returns path, cost, and a step-by-step log of distance updates.
    """
    nodes = list(graph.nodes())
    edges = list(graph.edges(data=True))
    
    if src not in nodes or dst not in nodes:
        return [], float('inf'), ["Source or destination not in graph."]
    
    # Since Bellman-Ford operates on directed edges, we duplicate undirected edges
    directed_edges = []
    for u, v, data in edges:
        weight = data.get('weight', 1)
        directed_edges.append((u, v, weight))
        directed_edges.append((v, u, weight))
        
    distances = {node: float('inf') for node in nodes}
    distances[src] = 0
    previous = {node: None for node in nodes}
    log = []
    
    log.append(f"Initialization: distance to src '{src}' is 0, others infinity.")
    
    # Relax edges (V-1) times
    for i in range(len(nodes) - 1):
        updated = False
        for u, v, weight in directed_edges:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                log.append(f"Step {i+1}: Update dist[{v}] from {distances[v]} to {distances[u] + weight} via {u}")
                distances[v] = distances[u] + weight
                previous[v] = u
                updated = True
        
        if not updated:
            log.append(f"Early termination at step {i+1}: no updates made.")
            break
            
    # Check for negative weight cycles (Vth relaxation)
    for u, v, weight in directed_edges:
        if distances[u] != float('inf') and distances[u] + weight < distances[v]:
            log.append("Warning: Graph contains a negative weight cycle.")
            return [], float('-inf'), log
            
    # Reconstruct path
    path = []
    current = dst
    if previous[current] is not None or current == src:
        while current is not None:
            path.insert(0, current)
            current = previous[current]
            
    if not path or path[0] != src:
        return [], float('inf'), log # No path found
        
    return path, distances[dst], log


def simulate_congestion(graph, edge_list, increase_factor=2.0):
    """
    Raises the weights of the given edges to simulate traffic congestion.
    Returns a new graph with updated weights.
    """
    new_graph = graph.copy()
    for u, v in edge_list:
        if new_graph.has_edge(u, v):
            current_weight = new_graph[u][v].get('weight', 1)
            new_graph[u][v]['weight'] = current_weight * increase_factor
    return new_graph


def compare_routes_under_congestion(graph, src, dst, congested_edges):
    """
    Compares original route/cost vs new route/cost after applying congestion.
    """
    print("--- Original Routing (No Congestion) ---")
    orig_path, orig_cost, orig_log = bellman_ford(graph, src, dst)
    print(f"Original Route: {orig_path}")
    print(f"Original Cost: {orig_cost}")
    
    # Apply severe congestion
    congested_graph = simulate_congestion(graph, congested_edges, increase_factor=5.0)
    
    print("\n--- Routing with Congestion ---")
    new_path, new_cost, new_log = bellman_ford(congested_graph, src, dst)
    print(f"New Route: {new_path}")
    print(f"New Cost: {new_cost}")
    
    print("\n--- Impact Analysis ---")
    print(f"Cost Difference: +{new_cost - orig_cost}")
    if orig_path != new_path:
        print("Alert: Traffic congestion forced a route change!")
    else:
        print("Info: Route remained the same despite congestion (no better alternatives).")


if __name__ == "__main__":
    print("--- Testing Traffic Analysis (Bellman-Ford) ---")
    G = generate_sample_graph(6)
    nodes = list(G.nodes())
    
    if len(nodes) >= 2:
        src, dst = nodes[0], nodes[-1]
        
        # First, find a path to pick an edge to congest
        path, _, _ = bellman_ford(G, src, dst)
        
        if len(path) > 1:
            # Pick the first edge in the original path to simulate congestion
            edges_to_congest = [(path[0], path[1])]
            print(f"Applying heavy congestion to edge: {edges_to_congest}\n")
            
            compare_routes_under_congestion(G, src, dst, edges_to_congest)
        else:
            print("Source and destination are the same, or unreachable.")
