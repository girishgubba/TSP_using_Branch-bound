import numpy as np
import matplotlib.pyplot as plt


def euclidean_distance(city1, city2):
    return np.linalg.norm(np.array(city1) - np.array(city2))


def nearest_neighbor(graph, start):
    unvisited = set(range(len(graph)))
    path = [start]
    unvisited.remove(start)
    current = start
    while unvisited:
        nearest_city = min(unvisited, key=lambda city: graph[current][city])
        path.append(nearest_city)
        unvisited.remove(nearest_city)
        current = nearest_city
    return path


def total_cost(graph, path):
    cost = 0
    for i in range(len(path)):
        cost += graph[path[i - 1]][path[i]]
    return cost


def plot_graph(graph, path, cost):
    x = [city[0] for city in graph]
    y = [city[1] for city in graph]
    plt.plot(x, y, 'bo')
    for i in range(len(graph)):
        plt.text(x[i], y[i], str(i), fontsize=12)
    for i in range(len(path) - 1):
        plt.plot([graph[path[i]][0], graph[path[i + 1]][0]],
                 [graph[path[i]][1], graph[path[i + 1]][1]], 'r-')
        distance = euclidean_distance(graph[path[i]], graph[path[i + 1]])
        plt.text((graph[path[i]][0] + graph[path[i + 1]][0]) / 2,
                 (graph[path[i]][1] + graph[path[i + 1]][1]) / 2,
                 f"{round(distance, 2)}", fontsize=10, horizontalalignment='center')
    plt.plot([graph[path[-1]][0], graph[path[0]][0]],
             [graph[path[-1]][1], graph[path[0]][1]], 'r-')
    distance = euclidean_distance(graph[path[-1]], graph[path[0]])
    plt.text((graph[path[-1]][0] + graph[path[0]][0]) / 2,
             (graph[path[-1]][1] + graph[path[0]][1]) / 2,
             f"{round(distance, 2)}", fontsize=10, horizontalalignment='center')

    plt.text(min(x) + 0.1, min(y) + 0.1, f"Mininimum Cost: {round(cost, 2)}", fontsize=12)

    plt.title('TSP Path with Distances and Total Cost')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()


# Example usage
# Define cities as (x, y) coordinates
cities = [(1, 0), (3, 2), (3, 4), (6, 2), (7, 0)]

# Calculate distance matrix
num_cities = len(cities)
distance_matrix = np.zeros((num_cities, num_cities))
for i in range(num_cities):
    for j in range(num_cities):
        distance_matrix[i][j] = euclidean_distance(cities[i], cities[j])

# Run nearest neighbor algorithm
start_city = 0
path = nearest_neighbor(distance_matrix, start_city)

# Calculate total path cost
cost = total_cost(distance_matrix, path)

# Plot the graph with the path, distances, and total cost
plot_graph(cities, path, cost)

print("Path:", path)
print("MINIMUM COST:",cost)