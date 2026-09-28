import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from graph_utils import create_empty_graph, add_node, add_edge, generate_sample_graph, get_adjacency_list, get_adjacency_matrix
from route_planner import dijkstra
from traffic_analysis import bellman_ford, simulate_congestion
from connectivity_module import bfs_traversal, dfs_traversal
from mst_planner import prim_mst, kruskal_mst

def plot_graph(graph, highlight_nodes=None, highlight_edges=None):
    fig, ax = plt.subplots(figsize=(6, 4))
    if len(graph.nodes()) == 0:
        ax.text(0.5, 0.5, "Empty Graph", ha="center", va="center")
        ax.axis('off')
        return fig
    
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, ax=ax, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_weight='bold')
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
    
    if highlight_nodes:
        nx.draw_networkx_nodes(graph, pos, nodelist=highlight_nodes, node_color='lightgreen', ax=ax, node_size=500)
    if highlight_edges:
        edges_to_draw = []
        for edge in highlight_edges:
            u, v = edge[0], edge[1]
            if graph.has_edge(u, v):
                edges_to_draw.append((u, v))
            elif graph.has_edge(v, u):
                edges_to_draw.append((v, u))
        nx.draw_networkx_edges(graph, pos, edgelist=edges_to_draw, edge_color='red', width=2.5, ax=ax)
        
    return fig

def path_to_edges(path):
    return [(path[i], path[i+1]) for i in range(len(path)-1)]

def init_state():
    if 'graph' not in st.session_state:
        st.session_state.graph = generate_sample_graph(5)

def page_network_modeling():
    st.header("Network Modeling")
    g = st.session_state.graph
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Add Node")
        new_node = st.text_input("Node Name (e.g., A, B, 1, 2)")
        if st.button("Add Node"):
            if new_node:
                try:
                    new_node = int(new_node)
                except ValueError:
                    pass
                add_node(g, new_node)
                st.success(f"Added node: {new_node}")
                st.rerun()
                
        st.subheader("Add Edge")
        nodes = list(g.nodes())
        if len(nodes) >= 2:
            u = st.selectbox("Source", nodes, key="edge_u")
            v = st.selectbox("Destination", nodes, key="edge_v")
            w = st.number_input("Weight", min_value=1, value=10)
            if st.button("Add Edge"):
                if u != v:
                    add_edge(g, u, v, w)
                    st.success(f"Added edge {u}-{v} with weight {w}")
                    st.rerun()
                else:
                    st.error("Source and destination must be different.")
                    
        st.subheader("Load Sample Graph")
        size = st.number_input("Number of Nodes", min_value=2, max_value=20, value=5)
        if st.button("Generate"):
            st.session_state.graph = generate_sample_graph(size)
            st.rerun()
            
    with col2:
        st.pyplot(plot_graph(g))
        
    st.subheader("Graph Representations")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Adjacency List**")
        st.json(get_adjacency_list(g))
    with c2:
        st.write("**Adjacency Matrix**")
        if len(nodes) > 0:
            st.dataframe(get_adjacency_matrix(g))

def page_route_planning():
    st.header("Route Planning (Dijkstra)")
    g = st.session_state.graph
    nodes = list(g.nodes())
    
    if len(nodes) < 2:
        st.warning("Need at least 2 nodes in the graph.")
        return
        
    c1, c2 = st.columns(2)
    with c1:
        src = st.selectbox("Source", nodes, key="rp_src")
    with c2:
        dst = st.selectbox("Destination", nodes, key="rp_dst")
        
    if st.button("Find Shortest Path"):
        path, cost, log = dijkstra(g, src, dst)
        
        if not path:
            st.error("No path found!")
        else:
            st.success(f"Path: {' -> '.join(map(str, path))} | Total Cost: {cost}")
            st.pyplot(plot_graph(g, highlight_nodes=path, highlight_edges=path_to_edges(path)))
            
            st.subheader("Distance Updates Log")
            st.table(pd.DataFrame({"Log": log}))

def page_traffic_analysis():
    st.header("Traffic Analysis (Bellman-Ford)")
    g = st.session_state.graph
    nodes = list(g.nodes())
    edges = list(g.edges())
    
    if len(nodes) < 2 or len(edges) == 0:
        st.warning("Graph must have nodes and edges.")
        return
        
    c1, c2, c3 = st.columns(3)
    with c1:
        src = st.selectbox("Source", nodes, key="ta_src")
    with c2:
        dst = st.selectbox("Destination", nodes, key="ta_dst")
    with c3:
        edge_to_congest = st.selectbox("Road to Congest", edges, format_func=lambda e: f"{e[0]} - {e[1]}")
        factor = st.slider("Congestion Factor", min_value=2.0, max_value=10.0, value=3.0)
        
    if st.button("Analyze Impact"):
        orig_path, orig_cost, _ = bellman_ford(g, src, dst)
        
        congested_graph = simulate_congestion(g, [edge_to_congest], increase_factor=factor)
        new_path, new_cost, _ = bellman_ford(congested_graph, src, dst)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Before Congestion")
            if orig_path:
                st.write(f"**Path**: {' -> '.join(map(str, orig_path))}")
                st.write(f"**Cost**: {orig_cost}")
                st.pyplot(plot_graph(g, highlight_edges=path_to_edges(orig_path)))
            else:
                st.write("No path found.")
                
        with col2:
            st.subheader("After Congestion")
            if new_path:
                st.write(f"**Path**: {' -> '.join(map(str, new_path))}")
                st.write(f"**Cost**: {new_cost}")
                fig = plot_graph(congested_graph, highlight_edges=path_to_edges(new_path))
                st.pyplot(fig)
            else:
                st.write("No path found.")
                
        st.subheader("Comparison")
        df = pd.DataFrame({
            "Metric": ["Path", "Cost"],
            "Original": [str(orig_path), orig_cost],
            "Congested": [str(new_path), new_cost]
        })
        st.table(df)

def page_connectivity():
    st.header("Connectivity Analysis")
    g = st.session_state.graph
    nodes = list(g.nodes())
    
    if not nodes:
        st.warning("Empty graph.")
        return
        
    start = st.selectbox("Start Node", nodes)
    
    if st.button("Analyze Connectivity"):
        bfs_order, bfs_reachable = bfs_traversal(g, start)
        dfs_order, dfs_reachable = dfs_traversal(g, start)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("BFS Traversal")
            st.write(f"**Order**: {bfs_order}")
            st.write(f"**Reachable Nodes**: {bfs_reachable}")
            st.pyplot(plot_graph(g, highlight_nodes=list(bfs_reachable)))
            
        with c2:
            st.subheader("DFS Traversal")
            st.write(f"**Order**: {dfs_order}")
            st.write(f"**Reachable Nodes**: {dfs_reachable}")
            st.pyplot(plot_graph(g, highlight_nodes=list(dfs_reachable)))

def page_infrastructure():
    st.header("Infrastructure Planning (MST)")
    g = st.session_state.graph
    
    if len(g.nodes()) == 0:
        st.warning("Empty graph.")
        return
        
    if st.button("Compute Minimum Spanning Trees"):
        p_edges, p_cost = prim_mst(g)
        k_edges, k_cost = kruskal_mst(g)
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Prim's Algorithm")
            st.write(f"**Total Cost**: {p_cost}")
            st.write(f"**Edges**: {p_edges}")
            st.pyplot(plot_graph(g, highlight_edges=p_edges))
            
        with c2:
            st.subheader("Kruskal's Algorithm")
            st.write(f"**Total Cost**: {k_cost}")
            st.write(f"**Edges**: {k_edges}")
            st.pyplot(plot_graph(g, highlight_edges=k_edges))

def main():
    st.set_page_config(page_title="Smart City Traffic System", layout="wide")
    init_state()
    
    st.sidebar.title("Navigation")
    pages = {
        "Network Modeling": page_network_modeling,
        "Route Planning": page_route_planning,
        "Traffic Analysis": page_traffic_analysis,
        "Connectivity Analysis": page_connectivity,
        "Infrastructure Planning": page_infrastructure
    }
    
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    pages[selection]()

if __name__ == "__main__":
    main()
