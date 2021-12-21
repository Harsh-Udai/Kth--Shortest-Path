# -*- coding: utf-8 -*-

__author__ = 'Gunjan Rakesh Mishra'

__all__ = ['kth_shortest_path']


import networkx as nx
import pandas as pd
import csv

# file_nodes = csv.reader(open(r"C:\Users\SUNYloaner\Desktop\pythonyen\input_nodes.csv" ,'r'))
# file_edges = csv.reader(open(r"C:\Users\SUNYloaner\Desktop\pythonyen\input_edges.csv" ,'r'))


file_nodes = pd.read_csv("input_nodes.csv")
file_edges = pd.read_csv("input_edges.csv")

G=nx.Graph()
tmp=0
for row in file_nodes:
    if (tmp>0):
        G.add_node(row[0])
    tmp=+1


tmp=0
for row in file_edges:
    print(row)
    if (tmp>0): # Ignores the first line in the file
        G.add_edge(row[0],row[1])
        G[row[0]][row[1]]['weight']=float(row[2])
    tmp+=1

print(G)
print(G.nodes)
print(G.edges)

def k_shortest_paths(G, source, target, K, weight='weight', all_kshortest = False):
   
    if source == target:
        return (0, [source]) 
    
    A = []
    all_length = []
    
    B_length, B = nx.single_source_dijkstra(G, source, target, weight=weight)
    
    if K ==1:
        return B_length, B
    A.append(B)
    all_length.append(B_length)
    
    if target not in A[0]:
        raise nx.NetworkXNoPath("node %s not reachable from %s" % (source, target))
        
    for k in range(1, K):

        for i in range(len(A[-1]) - 1):
            spur_node = A[-1][i]
            root_path = A[-1][:i + 1]
            
            if weight:
                root_path_length = get_path_length(G, root_path, weight)
            
            edges_removed = []
            if  weight:
                edge_attr = []
            for path in A:
                if root_path == path[:i + 1]:
                    u = path[i]
                    v = path[i + 1]
                    if (u,v) not in edges_removed:
                        if  weight:
                            edge_attr.append(G[u][v][weight])
                        G.remove_edge(u, v)
                        edges_removed.append((u, v))
            
            for node in root_path[:-1]:
                for u, v, attr in list(G.edges(node, data=True)):
                    if  weight:
                        edge_attr.append(attr[weight])
                    G.remove_edge(u,v)
                    edges_removed.append((u,v))
            
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
            if total_path_length > all_length[-1]:
                if B:
                    if total_path_length < B_length:
                        B = total_path
                        B_length = total_path_length
                    else:
                        B = total_path
                        B_length = total_path_length
                    
            for w in range(len(edges_removed)):
                u = edges_removed[w][0]
                v = edges_removed[w][1]
                G.add_edge(u,v)
                if  weight:
                    G.edges[u,v][weight]=edge_attr[w]
        
        if B:
            A.append(B)
            all_length.append(B_length)
        else:
            break
    if all_kshortest:
        return (all_length, A)
    
    return (all_length[-1], A[-1])

def get_path_length(G, path, weight='weight'):
    cost = 0

    if len(path) > 1:
        for i in range(len(path)-1):
            u = path[i]
            v = path[i + 1]
            
            cost += G.edges[u,v][weight]
    
    return cost    
    
'''G = nx.DiGraph()
G.add_edge('C', 'D',co = 3)
G.add_edge('C', 'E',length = 2)
G.add_edge('D', 'F',length = 4)
G.add_edge('E', 'D',length = 1)
G.add_edge('E', 'F',length = 2)
G.add_edge('E', 'G',length = 3)
G.add_edge('F', 'G',length = 2)
G.add_edge('F', 'H',length = 1)
G.add_edge('G', 'H',length = 2)

file_nodes = csv.reader(open('input_nodes.txt' ,'r'))
file_edges = csv.reader(open('input_edges.txt' ,'r'))
'''

sour = input ("Enter starting point or source :")
print("The source you have entered is:",sour)
dest = input("Enter destination :")
print("The destination you have entered is:",dest)
kth = input("Enter the value of k i.e. what number of shortest path you want to find? For example: 2nd shortest path or 6th shortest path..")
print("The value of k is: ",kth)



print(k_shortest_paths(G, sour, dest, kth, "cost", False)) 