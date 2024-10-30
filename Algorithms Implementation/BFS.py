graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A'],
    'C': ['A', 'D'],
    'D': ['A', 'C', 'E'],
    'E': ['D'],
}

def BFS(node):

    queue = []                  
    visited = []                
    order = []        

    visited.append(node)        
    queue.append(node)          

    while queue:
        vertex = queue.pop(0)   
        order.append(vertex)   

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

    print(order)

BFS('D')