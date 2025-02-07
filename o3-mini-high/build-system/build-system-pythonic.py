from collections import deque

graph = {
    0: [1, 2, 5],
    1: [3],
    2: [3],
    3: [],
    4: []
}

def topo_sort_kahn(graph):
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1
    
    Q = deque([u for u in graph if in_degree[u] == 0])
    ordering = []
    while Q:
        u = Q.popleft()
        ordering.append(u)
        for v in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                Q.append(v)

    if len(ordering) != len(in_degree):
        raise ValueError("Cycle detected")
    return ordering

# Example usage
print("Build order (Kahn):", topo_sort_kahn(graph))
