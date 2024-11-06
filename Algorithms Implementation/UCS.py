import heapq

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 5)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('B', 5), ('C', 1)]
}

def ucs(graph, start, goal):

    queue = [(0, start)]
    visited = {start: 0}

    while queue:
        current_cost, current_node = heapq.heappop(queue)

        if current_node == goal:
            return current_cost

        for neighbor, cost in graph[current_node]:
            new_cost = current_cost + cost

            if neighbor not in visited or new_cost < visited[neighbor]:
                visited[neighbor] = new_cost
                heapq.heappush(queue, (new_cost, neighbor))

    return float("inf")

start = 'A'
goal = 'D'

result = ucs(graph, start, goal)

print(f"from {start} to {goal} is: {result}")
