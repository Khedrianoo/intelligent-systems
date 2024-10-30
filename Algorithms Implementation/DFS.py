graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A'],
    'C': ['A', 'D'],
    'D': ['A', 'C', 'E'],
    'E': ['D'],
}

def DFS(start):

    stack = [start]               
    visited = []                  
    vertex = []          
    
    while stack:
        node = stack.pop()
        
        if node not in visited:
            visited.append(node)            
            vertex.append(node)     
            
            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

    print(vertex)
    
DFS('D')
