

class Node:
    def __init__(self, value, pnext=None):
        self.value = value
        self.next = pnext

class CircularList:
    def __init__(self, values):
        self.map = {}
        nodes = [Node(v) for v in values]
        self.max = max(n.value for n in nodes)
        self.min = min(n.value for n in nodes)
        for n in nodes:
            self.map[n.value] = n
        self.front = nodes[0]
        for i, node in enumerate(nodes):
            node.next = nodes[(i+1)%len(nodes)]
    def to_list(self):
        res = [self.front.value]
        i = self.front.next
        while i != self.front:
            res.append(i.value)
            i = i.next
        return res
    def str_from(self, v):
        at = self.find(v)
        scl = "(" + str(at.value) + ")"
        i = at.next
        while i != at:
            scl += f" {i.value}" 
            i = i.next
        return scl
    def __str__(self):
        scl = "(" + str(self.front.value) + ")"
        i = self.front.next
        while i != self.front:
            scl += f" {i.value}" 
            i = i.next
        return scl
    def __repr__(self):
        scl = f"CircularList([{self.front.value}"
        i = self.front.next
        while i != self.front:
            scl += f", {i.value}" 
            i = i.next
        scl += "])"
        return scl
    def pop(self):
        v = self.front.next
        self.front.next = v.next
        return v.value
    def cut(self):
        pn = self.front.next
        pnn = pn.next
        pnnn = pnn.next
        self.front.next = pnnn.next
        pnnn.next = None
        return (pn, pnnn, [pn.value, pnn.value, pnnn.value])
    def advance(self):
        self.front = self.front.next
    def insert_after(self, v, cf, cl):
        at = self.find(v)
        if not at: return False
        cl.next = at.next
        at.next = cf
        return True
    def find(self, v):
        return self.map[v]
    def next_insert(self, n):
        i = n - 1
        if i < self.min:
            return self.max
        return i
    def game(self):
        [cf, cl, nodes] = self.cut()
        f = self.next_insert(self.front.value)
        while f in nodes:
            f = self.next_insert(f)
        r = self.insert_after(f, cf, cl)
        while not r:
            f = self.next_insert(f)
            r = self.insert_after(f, cf, cl)
        self.advance()

cups = [5, 9, 8, 1, 6, 2, 7, 3, 4]
#cups = list(map(int, list("389125467")))
cl = CircularList(cups)

for _ in range(100):
    cl.game()

print(cl.str_from(1).replace(" ", ""))

###
## Part 2
###
from itertools import chain
game_size = 1_000_000
number_of_moves = 10_000_000
cl2 = CircularList(chain(cups, range(max(cups)+1, game_size+1)))

for _ in range(number_of_moves):
    cl2.game()

uno = cl2.find(1)
uno_n = uno.next
print(uno_n.value)
uno_nn = uno_n.next
print(uno_nn.value)
print("res: ", uno_n.value * uno_nn.value)



