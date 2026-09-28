from graph_utils import generate_sample_graph

def bfs_traversal(graph, start_node):
    """
    Manual Breadth-First Search (BFS) implementation.
    Returns the order of traversal and the set of reachable nodes.
    """
    visited = set()
    queue = [start_node]
    visited.add(start_node)
    
    traversal_order = []
    
    while queue:
        current = queue.pop(0) # Dequeue from the front
        traversal_order.append(current)
        
        # Enqueue unvisited neighbors
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                
    return traversal_order, visited

def dfs_traversal(graph, start_node):
    """
    Manual Depth-First Search (DFS) implementation using an iterative approach.
    Returns the order of traversal and the set of reachable nodes.
    """
    visited = set()
    stack = [start_node]
    
    traversal_order = []
    
    while stack:
        current = stack.pop() # Pop from the top
        
        if current not in visited:
            visited.add(current)
            traversal_order.append(current)
            
            # Push unvisited neighbors to stack
            # Reversing ensures we visit neighbors in a consistent order similar to recursive DFS
            for neighbor in reversed(list(graph.neighbors(current))):
                if neighbor not in visited:
                    stack.append(neighbor)
                    
    return traversal_order, visited

if __name__ == "__main__":
    print("--- Testing Connectivity Module (BFS/DFS) ---")
    G = generate_sample_graph(6)
    nodes = list(G.nodes())
    
    if nodes:
        start = nodes[0]
        print(f"Starting traversals from node {start}")
        
        bfs_order, bfs_reachable = bfs_traversal(G, start)
        print(f"\nBFS Traversal Order: {bfs_order}")
        print(f"BFS Reachable Nodes: {bfs_reachable}")
        
        dfs_order, dfs_reachable = dfs_traversal(G, start)
        print(f"\nDFS Traversal Order: {dfs_order}")
        print(f"DFS Reachable Nodes: {dfs_reachable}")
