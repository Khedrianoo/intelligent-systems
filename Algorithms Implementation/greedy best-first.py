import heapq

graph = {
    'A': [('B', 1), ('C', 2)],
    'B': [('D', 3), ('E', 1)],
    'C': [('F', 4)],
    'D': [],
    'E': [('G', 2)],
    'F': [('G', 1)],
    'G': []
}

heuristics = {
    'A': 5,
    'B': 4,
    'C': 2,
    'D': 6,
    'E': 3,
    'F': 1,
    'G': 0  
}

def greedy_best_first_search(graph, start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristics[start], start))
    
    visited = set()
    
    path = []
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path.append(current)
            print("Goal found! Path:", path)
            return path
        
        path.append(current)
        visited.add(current)
        
        for neighbor, _ in graph[current]:
            if neighbor not in visited:
                heapq.heappush(open_list, (heuristics[neighbor], neighbor))
    
    print("Goal not found.")
    return None

start_node = 'A'
goal_node = 'G'
greedy_best_first_search(graph, start_node, goal_node)