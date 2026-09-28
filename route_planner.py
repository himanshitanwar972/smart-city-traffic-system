from graph_utils import generate_sample_graph

def dijkstra(graph, src, dst):
    """
    Manual implementation of Dijkstra's algorithm.
    Finds the shortest path and cost from src to dst.
    Returns path, cost, and a step-by-step log.
    """
    nodes = list(graph.nodes())
    if src not in nodes or dst not in nodes:
        return None, float('inf'), ["Source or destination not in graph."]
        
    # Initialization
    distances = {node: float('inf') for node in nodes}
    distances[src] = 0
    previous = {node: None for node in nodes}
    unvisited = set(nodes)
    log = []
    
    log.append(f"Initialization: distance to src '{src}' set to 0, all others to infinity.")
    
    while unvisited:
        # Find unvisited node with minimum distance
        current_node = min(unvisited, key=lambda node: distances[node])
        
        # If the smallest distance is infinity, the remaining nodes are unreachable
        if distances[current_node] == float('inf'):
            log.append("Remaining unvisited nodes are unreachable from source.")
            break 
            
        if current_node == dst:
            log.append(f"Destination '{dst}' reached. Stopping search.")
            break 
            
        unvisited.remove(current_node)
        
        # Check neighbors
        for neighbor in graph.neighbors(current_node):
            if neighbor in unvisited:
                weight = graph[current_node][neighbor].get('weight', 1)
                new_distance = distances[current_node] + weight
                
                if new_distance < distances[neighbor]:
                    log.append(f"Update: dist[{neighbor}] changed from {distances[neighbor]} to {new_distance} via {current_node}")
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_node
                    
    # Reconstruct the shortest path
    path = []
    current = dst
    if previous[current] is not None or current == src:
        while current is not None:
            path.insert(0, current)
            current = previous[current]
            
    if not path or path[0] != src:
        return [], float('inf'), log # No path found
        
    return path, distances[dst], log

if __name__ == "__main__":
    print("--- Testing Route Planner (Dijkstra) ---")
    G = generate_sample_graph(6)
    nodes = list(G.nodes())
    
    if len(nodes) >= 2:
        src, dst = nodes[0], nodes[-1]
        print(f"Finding path from {src} to {dst}")
        
        path, cost, log = dijkstra(G, src, dst)
        
        print(f"Path: {path}")
        print(f"Cost: {cost}")
        print("Log of updates:")
        for entry in log:
            print(f"  - {entry}")
