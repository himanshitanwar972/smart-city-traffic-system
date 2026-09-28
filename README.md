# Smart City Traffic System

A Python-based smart city traffic system simulation leveraging graph algorithms.

## Features
- **Network Modeling (`app.py`, `graph_utils.py`)**: Interactively generate and manage road networks as graphs.
- **Route Planning (`route_planner.py`)**: Dijkstra's algorithm for finding the shortest paths between city locations.
- **Traffic Analysis (`traffic_analysis.py`)**: Bellman-Ford algorithm to find shortest paths and analyze route changes due to traffic congestion.
- **Connectivity Analysis (`connectivity_module.py`)**: BFS and DFS to check reachable zones and traversal orders.
- **Infrastructure Planning (`mst_planner.py`)**: Prim's and Kruskal's algorithms to design minimum spanning trees for optimal infrastructure deployment.
- **Algorithm Analysis (`project_notebook.ipynb`)**: Jupyter notebook containing performance benchmarks and execution time charts.

## Project Structure
- `app.py`: The main Streamlit dashboard to visualize the algorithms.
- `graph_utils.py`, `route_planner.py`, `traffic_analysis.py`, `connectivity_module.py`, `mst_planner.py`: Core logic files implementing manual graph algorithms.
- `project_notebook.ipynb`: Data science notebook comparing algorithms.
- `Final_Report.docx`: The final analysis and experimental results report.
- `requirements.txt`: Python package dependencies.
- `/screenshots`: Visual examples of each module from the UI.

## Setup Instructions
1. Clone the repository and navigate to the project directory.
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On MacOS/Linux
   # .venv\Scripts\activate   # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
To launch the interactive dashboard, run:
```bash
streamlit run app.py
```
The app will open automatically in your browser (usually at `http://localhost:8501`).
