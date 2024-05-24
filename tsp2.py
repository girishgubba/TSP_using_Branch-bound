import tkinter as tk
from tkinter import simpledialog
import matplotlib.pyplot as plt
import networkx as nx


def calculate_tour():
    n = int(entry_nodes.get())

    # Initialize distance matrix
    dist = [[0] * (n + 1) for _ in range(n + 1)]

    # Input distance values
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if (i, j) not in distances:
                distances[(i, j)] = 0
            dist[i][j] = distances[(i, j)]

    ans = float('inf')  # Initialize answer

    # Try to go from node 1 visiting all nodes in between to i
    # Then return from i taking the shortest route to 1
    for i in range(1, n + 1):
        ans = min(ans, fun(i, (1 << (n + 1)) - 1, dist, memo) + dist[i][1])

    label_result.config(text=f"The cost of the most efficient tour = {ans}")

    # Get the path
    path_edges = get_path(ans, n, dist, memo)
    path_str = " -> ".join([f"({e[0]}, {e[1]})" for e in path_edges])
    label_path.config(text=f"Path: {path_str}")

    # Display the graph
    G = nx.DiGraph()
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i != j:
                G.add_edge(i, j, weight=dist[i][j])
    pos = nx.spring_layout(G)

    # Highlight the path of the most efficient tour
    path_nodes = [edge[0] for edge in path_edges]
    path_edges = [(path_nodes[i], path_nodes[i + 1]) for i in range(len(path_nodes) - 1)]

    # Add edges representing the path traveled to the graph
    for edge in path_edges:
        G.add_edge(edge[0], edge[1], color='blue', width=2)

    plt.figure(figsize=(8, 6))
    edges = G.edges()
    colors = [G[u][v]['color'] if 'color' in G[u][v] else 'gray' for u, v in edges]
    widths = [G[u][v]['width'] if 'width' in G[u][v] else 1.0 for u, v in edges]
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color="skyblue", font_size=12, font_weight="bold",
            arrowsize=20, width=widths, edge_color=colors)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Graph of the Efficient Tour")
    plt.show()


def get_path(ans, n, dist, memo):
    for i in range(1, n + 1):
        if ans == fun(i, (1 << (n + 1)) - 1, dist, memo) + dist[i][1]:
            mask = (1 << (n + 1)) - 1
            path = [i]
            cur = i
            while cur != 1:
                for j in range(1, n + 1):
                    if (mask & (1 << j)) != 0 and j != cur and j != 1 and ans == fun(cur, mask & (~(1 << i)), dist,
                                                                                     memo) + dist[j][cur]:
                        path.append(j)
                        mask = mask & (~(1 << cur))
                        cur = j
                        break
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            return path_edges


def fun(i, mask, dist, memo):
    if mask == ((1 << i) | 1):  # Base case: visiting all nodes except 1 and ending at node i
        return dist[1][i]

    if memo[i][mask] != -1:  # Memoization
        return memo[i][mask]

    res = float('inf')  # Initialize result for this sub-problem

    # Recursively calculate the cost of visiting all nodes in the mask (except i)
    # and then return from node j to node i, taking the shortest path
    for j in range(1, n + 1):
        if (mask & (1 << j)) != 0 and j != i and j != 1:
            res = min(res, fun(j, mask & (~(1 << i)), dist, memo) + dist[j][i])
    memo[i][mask] = res  # Store the minimum value
    return res


def create_distance_entry(i, j):
    distance = simpledialog.askinteger("Input", f"Enter distance from node {i} to node {j}")
    distances[(i, j)] = distance
    if j < n:
        create_distance_entry(i, j + 1)
    elif i < n:
        create_distance_entry(i + 1, 1)


def create_distance_entries():
    global n
    n = int(entry_nodes.get())
    create_distance_entry(1, 1)


app = tk.Tk()
app.title("Efficient Tour Calculator")
app.geometry("800x600")  # Adjust the size of the applet window

frame_nodes = tk.Frame(app)
frame_nodes.pack(pady=20)

label_nodes = tk.Label(frame_nodes, text="Enter the number of nodes:")
label_nodes.grid(row=0, column=0, padx=5)

entry_nodes = tk.Entry(frame_nodes, width=5)
entry_nodes.grid(row=0, column=1, padx=5)

button_create = tk.Button(frame_nodes, text="Create Distance Entries", command=create_distance_entries)
button_create.grid(row=0, column=2, padx=5)

frame_distances = tk.Frame(app)
frame_distances.pack(pady=20)

label_result = tk.Label(app, text="")
label_result.pack()

label_path = tk.Label(app, text="")
label_path.pack()

button_calculate = tk.Button(app, text="Calculate Tour Cost", command=calculate_tour)
button_calculate.pack(pady=10)

# Initialize memoization table
memo = [[-1] * (1 << 11) for _ in range(11)]

distances = {}
n = 0

app.mainloop()
