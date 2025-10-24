# generate edge-exchange Gray codes for all spanning trees of general graphs

from k_ary import k_ary  
import numpy as np

class Node:
    def __init__(self, val):
        self.val = val
        self.parent = None

node_list = []
adj = [[0]]

def lift_node(node):
    if node.parent is not None:
        lift_node(node.parent)
        node.parent.parent = node

def get_connected_components(nodes):
    visited = {nd.val: False for nd in nodes}
    cc_list = []
    for nd in nodes:
        if not visited[nd.val]:
            visited[nd.val] = True
            group = [nd]
            dfs(nd, nodes, visited, group)
            cc_list.append(group)
    return cc_list

def dfs(cnode, nodes, visited, group):
    for nd in nodes:
        if not visited[nd.val] and adj[cnode.val][nd.val] == 1:
            visited[nd.val] = True
            group.append(nd)
            dfs(nd, nodes, visited, group)

def check_k(parents, children):
    c = [0 for _ in range(len(children))]
    p_list = [[] for _ in range(len(children))]
    for i_c in range(len(children)):
        n_p = 0
        for i_p in range(len(parents)):
            if adj[parents[i_p].val][children[i_c].val] == 1:
                p_list[i_c].append(parents[i_p])
                n_p += 1
                if children[i_c].parent.val == parents[i_p].val:
                    c[i_c] = n_p            
    k_list = [len(p) for p in p_list]
    return c, k_list, p_list

def get_connection(cnode, nodes):
    m = {nd.val: [] for nd in nodes}
    for nd in nodes:
        try:
            m[nd.parent.val].append(nd)
        except KeyError:
            pass

    nodes_under_c = [cnode]
    temp_nodes = [cnode]
    while len(temp_nodes) > 0:
        new_nodes = []
        for tnd in temp_nodes:
            new_nodes += m[tnd.val]
            del m[tnd.val]
        nodes_under_c += new_nodes
        temp_nodes = new_nodes

    nodes_other = [nd for nd in nodes
                   if m.get(nd.val) is not None and nd.val != cnode.val]

    for nd1 in nodes_under_c:
        for nd2 in nodes_other:
            if adj[nd1.val][nd2.val] == 1:
                return nd1, nd2

def spanning_level(V, t_):
    C = [V[i] for i in range(len(V)) if t_[i] == 0]
    if len(C) == 0:
        yield node_list
        return

    P = [V[i] for i in range(len(V)) if t_[i] > 0]
    C_ = get_connected_components(C)
    F = [check_k(P, C_sub) for C_sub in C_]

    def spanning_subtree(i_tree):
        if i_tree >= len(F):
            yield from spanning_level(sum(C_, []), sum([g[0] for g in F], []))
            return

        yield from spanning_subtree(i_tree+1)

        K = k_ary(F[i_tree][1].copy(), F[i_tree][0].copy())
        next(K)

        for t_l_i, idx in K:
            if len(idx) > 1:
                C_[i_tree][idx[0]].parent = None
                lift_node(C_[i_tree][idx[1]])
                C_[i_tree][idx[1]].parent = F[i_tree][2][idx[1]][t_l_i[idx[1]] - 1]

            elif t_l_i[idx[0]] > 0:
                C_[i_tree][idx[0]].parent = F[i_tree][2][idx[0]][t_l_i[idx[0]] - 1]

            else:
                nd1, nd2 = get_connection(C_[i_tree][idx[0]], C_[i_tree])
                C_[i_tree][idx[0]].parent = None
                lift_node(nd1)
                nd1.parent = nd2

            F[i_tree][0][:] = t_l_i[:]
            yield from spanning_subtree(i_tree+1)

    yield from spanning_subtree(0)

def get_first_spanning_tree():
    n = len(adj)
    check_list = [True for _ in range(n)]
    node_list[:] = [Node(i) for i in range(n)]
    check_list[0] = False
    for i in range(n):
        for j in range(n):
            if check_list[j] and adj[i][j] == 1:
                check_list[j] = False
                node_list[j].parent = node_list[i]

    return node_list

if __name__ == '__main__':
    def str_tree(nodes, vmap=None):
        res = ''
        for nd in nodes:
            res += '{}->{}; '.format(nd.val+1, nd.parent.val+1 if nd.parent is not None else -1)
        return res

    print('Enter type: #1 complete graph, #2 fan graph, #3 wheel graph, #4 petersen, #5 custom graph')
    i_type = int(input())

    if i_type != 4:
        print('Enter n:')
        n = int(input())
    else:
        n = 10

    if i_type == 1:
        adj = [[1 for _ in range(n)] for _ in range(n)]
        
    elif i_type == 2 or i_type == 3:
        # fan graph
        adj = np.zeros((n, n), dtype=int)
        adj[0, :] = 1
        adj[:, 0] = 1
        for i in range(1, n):
            adj[i, max(0, i - 1):min(n, i + 2)] = 1
            adj[max(0, i - 1):min(n, i + 2), i] = 1

        if i_type == 3:
            # wheel graph
            adj[1, -1] = 1
            adj[-1, 1] = 1

    elif i_type == 4:
        # petersen graph
        adj = np.array([
            [0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        ])
        
    elif i_type == 5:
        print('Enter edges: e.g., 1,2; 2,3')
        edge_str = input().replace(' ', '').split(';')
        edge_list = []
        for es in edge_str:
            if es:
                edge_list.append(tuple(map(int, es.split(','))))
        adj = np.zeros((n, n), dtype=int)
        for edge in edge_list:
            adj[edge[0]-1, edge[1]-1] = 1
            adj[edge[1]-1, edge[0]-1] = 1

    else:
        raise Exception('Invalid input')

    get_first_spanning_tree()  # bfs

    cnt = 0
    for t in spanning_level(node_list, [1] + [0 for _ in range(len(adj)-1)]):
        print(str_tree(t))
        cnt += 1
    print('Total: ' + str(cnt))
