import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

########################################### create graph 
def random_adjacency_matrix(n, p):
    A = np.random.rand(n, n) < p
    A = A.astype(int)
    A = np.triu(A, 1)
    A = A + A.T
    return A

def fix_A():
    # A = [
    # [0,1,1,1,0,1,0],
    # [1,0,1,1,1,1,0],
    # [1,1,0,0,0,1,1],
    # [1,1,0,0,1,1,1],
    # [0,1,0,1,0,1,0],
    # [1,1,1,1,1,0,1],
    # [0,0,1,1,0,1,0],
    # ]
    A = [
        [0,1,0,1,0,1,0,0],
        [1,0,0,1,0,1,0,0],
        [0,0,0,0,1,0,1,0],
        [1,1,0,0,1,1,0,1],
        [0,0,1,1,0,0,1,0],
        [1,1,0,1,0,0,0,0],
        [0,0,1,0,1,0,0,0],
        [0,0,0,1,0,0,0,0]
    ]
    return np.array(A)
########################################### create graph end

########################################### helper functions
def sort_nodes_by_degree(A):
    G = nx.from_numpy_array(A)
    degrees = dict(G.degree())
    sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
    return sorted_nodes

def split_nodes(A, sorted_nodes):
    box = []
    A1 = A.copy()
    for node in range(len(sorted_nodes)):
        member = np.where(A1[sorted_nodes[node]] == 1)[0]
        box.append([[sorted_nodes[node]], member.tolist()])
        A1[:, sorted_nodes[node]] = 0
    return box

def find_n(row):
    sum = 0
    for i in row:
        sum += 1
    return sum

def find_k(A, row):
    A = A[:, row]
    A = A[row, :]
    return np.sum(A == 1)/2

def find_upb(A, box):
    A1 = A.copy()
    count = 0
    for i in box:
        A1[:, i[0]] = 0
        A1[i[0], :] = 0
        n = find_n(i[1])
        k = find_k(A1, i[1])
        upb = int((1+(1+8*k)**0.5)/2)
        box[count].append([upb])
        count += 1

def main():
    n = 5
    p = 0.8
    # A = random_adjacency_matrix(n, p)
    A = fix_A()
    print(A)

    sorted_nodes = sort_nodes_by_degree(A)
    print("Nodes sorted by degree:", sorted_nodes)

    box = split_nodes(A, sorted_nodes)

    find_upb(A, box)
    print(box)
    
if __name__ == "__main__":
    main()
