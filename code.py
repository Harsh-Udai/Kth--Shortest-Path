import networkx as nx
import pandas as pd

def k_shortest_paths(G, source, target, K=1, weight='weight', all_kshortest = False):   
      
    A = []
    total_length = []
    
    if source == target:
        return (0, [source])

    B_length, B = nx.single_source_dijkstra(G, source, target, weight=weight)
    
    if K ==1:
        return B_length, B
    A.append(B)
    total_length.append(B_length)
       
    for n in range(1, K):

        for i in range(len(A[-1]) - 1):
            spur_node = A[-1][i]
            root_path = A[-1][:i + 1]
           
            if weight:
                root_path_length = get_path_length(G, root_path, weight)
           
            edges_discarded = []
            if  weight:
            
                edge_cost_add = []
            for path in A:
                if root_path == path[:i + 1]:
                    u = path[i]
                    v = path[i + 1]
                    if (u,v) not in edges_discarded:
                        if  weight:
                        
                            edge_cost_add.append(G[u][v][weight])
                            
                        G.remove_edge(u, v)
                        edges_discarded.append((u, v))
           
            for node in root_path[:-1]:
                for u, v, attr in list(G.edges(node, data=True)):
                    if  weight:
                        edge_cost_add.append(attr[weight])
                    G.remove_edge(u,v)
                    edges_discarded.append((u,v))
           
            try:
                spur_path_length, spur_path = nx.single_source_dijkstra(G, spur_node, target, weight=weight)  
            except:
                spur_path_length = 0
                spur_path = []
               
            total_path = root_path[:-1] + spur_path
            if weight:
                total_path_length = root_path_length + spur_path_length        
            else:
                total_path_length = i + spur_path_length
            if total_path_length > total_length[-1]:
                if B:
                    if total_path_length < B_length:
                        B = total_path
                        B_length = total_path_length
                    else:
                        B = total_path
                        B_length = total_path_length
                   
            for w in range(len(edges_discarded)):
                u = edges_discarded[w][0]
                v = edges_discarded[w][1]
                G.add_edge(u,v)
                if  weight:
                    G.edges[u,v][weight]=edge_cost_add[w]
       
        if B:
            A.append(B)
            total_length.append(B_length)
        else:
            break
    if all_kshortest:
        return (total_length, A)
   
    return (total_length[-1], A[-1])

def get_path_length(G, path, weight='weight'):
    length = 0

    if len(path) > 1:
        for i in range(len(path)-1):
            u = path[i]
            v = path[i + 1]
           
            length += G.edges[u,v][weight]
   
    return length    


   
G = nx.DiGraph()

file = pd.read_csv('input_edges.csv', header = None)
file1 = file.values.tolist()

for row in file1:
    # print(row)
    G.add_edge(row[0],row[1], length = row[2])

# print(G)
# print(G.nodes)
# print(G.edges)
   

sour = input ("Enter starting point or source :")
print("The source you have entered is:",sour)
dest = input("Enter destination :")
print("The destination you have entered is:",dest)
kth = input("Enter the value of k i.e. what number of shortest path you want to find? For example: 2nd shortest path or 6th shortest path..")
print("The value of k is: ",kth)



print(k_shortest_paths(G, sour, dest, int(kth), "length", False))




