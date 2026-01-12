import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

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
        k = find_k(A1, i[1])
        n = find_n(i[1])
        upb = int((1+(1+8*k)**0.5)/2)
        if n == 0:
            upb = 0
        box[count].append([upb+len(box[count][0])])
        count += 1

def find_lwb(A, box):
    A1 = A.copy()
    count = 0
    for i in box:
        A1[:, i[0]] = 0
        A1[i[0], :] = 0
        n = find_n(i[1])
        k = find_k(A1, i[1])
        if n == 0:
            lwb = 0
        else:
            lwb = 1
        for r in range(1,n+1,1):
            q = int(n/r)
            s = n - q*r
            km = math.comb(n,2) - math.comb(q+1,2)*s - math.comb(q,2)*(r-s)
            if km == k:
                lwb = r
                break
            if km > k:
                lwb = r-1
                break
        box[count][2].append(lwb+len(box[count][0]))
        count += 1

def deduct_nodes(box):
    max_lwb = max(a[2][1] for a in box)
    remove_list = []
    for i in box:
        if i[2][0] < max_lwb:
            remove_list.append(i)
    for j in remove_list:
        box.remove(j)

def check_clique(box, max_clique):
    remove_list = []
    for i in box:
        if i[2][0] == i[2][1] == len(i[0]) + len(i[1]):
            if len(max_clique) == 0:
                clique = [i[0]+i[1], i[2][0]]
                max_clique.append(clique)
                remove_list.append(i)
            else:
                if i[2][0] == max_clique[0][1]:
                    clique = [i[0]+i[1], i[2][0]]
                    max_clique.append(clique)
                    remove_list.append(i)

                elif i[2][0] > max_clique[0][1]:
                    max_clique.clear()
                    clique = [i[0]+i[1], i[2][0]]
                    max_clique.append(clique)
                    remove_list.append(i)
    for j in remove_list:
        box.remove(j)

def split_node_in_box(A, box):
    if len(box) == 0:
        return box
    
    A1 = A.copy()
    nodes = []
    for j in box[0][1]:
        nodes.append(box[0][0]+[j])
    box = box[1:]
    used_nodes = []
    box2 = []

    for n in nodes:
        member = np.where(np.all(A1[n] == 1, axis=0))[0].tolist()
        box2 = box2 + [[n, [x for x in member if x not in used_nodes]]] 
        used_nodes += [x for x in n if x not in used_nodes]
    return box2 + box
########################################### helper functions end

def find_nx(A):
    G = nx.from_numpy_array(A)
    return max(nx.find_cliques(G), key=len)


def main():
    max_clique = []
    n = 10
    p = 0.9
    A = random_adjacency_matrix(n, p)
    # A = fix_A()
    print(A)

    sorted_nodes = sort_nodes_by_degree(A)
    box = split_nodes(A, sorted_nodes)

    # find_upb(A, box)
    # find_lwb(A, box)
    # deduct_nodes(box)
    # check_clique(box, max_clique)
    # box = split_node_in_box(A, box)

    while box != []:
        find_upb(A, box)
        find_lwb(A, box)
        deduct_nodes(box)
        check_clique(box, max_clique)
        box = split_node_in_box(A, box)
    print("Max clique found :", max_clique)

    print("NetworkX Max clique:", find_nx(A), len(find_nx(A)))

if __name__ == "__main__":
    main()
