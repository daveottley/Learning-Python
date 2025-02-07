class Queue():
    def __init__(self, data=None, head=0):
        if data is None:
            self.data = []
        else:
            self.data = data
        self.head = head

    def enqueue(self, element):
        self.data.append(element) # O(1) time

    def dequeue(self): # O(1) amortized
        popped = self.data[self.head]
        self.head += 1
        return popped

    def is_empty(self):
        return self.head == len(self.data)

def topo_sort_kahn(graph, orphan_nodes=None):
    if orphan_nodes is None:
        orphan_nodes = []
    
    nodes = set(graph.keys())
    for lst in graph.values():
        nodes.update(lst)
    nodes.update(orphan_nodes)
    
    in_degree = {u: 0 for u in nodes}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    
    Q = Queue([u for u in nodes if in_degree[u] == 0])
    ordering = []
    while not Q.is_empty():
        u = Q.dequeue()
        ordering.append(u)
        for v in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                Q.enqueue(v)

    if len(ordering) != len(in_degree):
        raise ValueError("Cycle detected")
    return ordering

graph = {
    0: [1, 2, 5],
    1: [3],
    2: [3],
    3: [],
    4: []
}

# Example usage
print("Build order (Kahn):", topo_sort_kahn(graph))
