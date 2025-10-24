# generate pivot Gray codes for all spanning trees of complete graphs

from k_ary import k_ary  

class Node:
    def __init__(self, val):
        self.val = val
        self.parent = None

class LinkedList:
    def __init__(self):
        self.map = {}
        self.last = -1
        self.len = 0

    def append(self, val):
        self.map[val] = [self.last, -1]
        if self.last != -1:
            self.map[self.last][1] = val
        self.last = val
        self.len += 1

    def remove(self, val):
        val_last = self.map[val][0]
        val_next = self.map[val][1]
        if val_last != -1:
            self.map[val_last][1] = val_next
        if val_next != -1:
            self.map[val_next][0] = val_last
            self.last = val_next
        else:
            self.last = val_last
        del self.map[val]
        self.len -= 1
    
node_list = []

def lift_node(node):
    if node.parent is not None:
        lift_node(node.parent)
        node.parent.parent = node

def spanning_level(V, t_, n_c):
    if n_c == 0:
        yield node_list
        return

    P = [V[i] for i in range(len(V)) if t_[i] > 0]
    C = [V[i] for i in range(len(V)) if t_[i] == 0]
    t_l = [0 for _ in range(n_c)]
    C_ = LinkedList()

    m = {}
    for i in range(len(P)):
        m[P[i].val] = i+1

    for i in range(len(C)):
        if C[i].parent.val in m:
            t_l[i] = m[C[i].parent.val]
            C_.append(i)

    yield from spanning_level(C, t_l, len(C) - C_.len)

    K = k_ary([len(P) for _ in range(n_c)], t_l)
    next(K)

    for t_l, idx in K:
        if len(idx) > 1:
            temp = C[idx[0]].parent
            C[idx[0]].parent = None
            lift_node(C[idx[1]])
            C[idx[1]].parent = temp
            C_.append(idx[1])
            C_.remove(idx[0])

        elif t_l[idx[0]] > 0:
            C[idx[0]].parent = P[t_l[idx[0]]-1]
            if not idx[0] in C_.map:
                C_.append(idx[0])

        else:
            C_.remove(idx[0])
            C[idx[0]].parent = C[C_.last]

        yield from spanning_level(C, t_l, len(C) - C_.len)

if __name__ == '__main__':

    def str_tree(nodes):
        res = ''
        for nd in nodes:
            res += '{}->{}; '.format(nd.val+1, nd.parent.val+1 if nd.parent is not None else -1)

        return res

    print('Enter n:')
    n = int(input())

    prev = None
    for i in range(0, n):
        new_node = Node(i)
        if prev is not None:
            new_node.parent = prev
        node_list.append(new_node)
        prev = new_node
    print('==============================================')

    cnt = 0
    for t in spanning_level(node_list, [1] + [0 for _ in range(n - 1)], n - 1):
        print(str_tree(t))
        cnt += 1

    print('Total: ' + str(cnt))
