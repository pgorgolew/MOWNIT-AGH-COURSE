import networkx as nx
import random

def gen_2d(n):
    edges_str = ""
    for i in range(n**2):
        if i%n != n-1: #patrz w prawo
            R = random.randint(0, 15)
            edges_str += f"({i},{i+1}, {R});"
        if i//n != n-1: #patrz w doł
            R = random.randint(0, 15)
            edges_str += f"({i},{i+n}, {R});"

    print(edges_str[0:-1])

def gen_spojny(n):
    edges_str = ""
    for s in range(n):
        edges_str += f"({s},{(s+1)%n},{random.randint(0, 15)});"

    for s in range(n):
        for t in range(s+1, n):
            if s==t or (s+1)%n==t or (s-1)%n==t:
                continue
            if random.random() < 0.2:
                edges_str += f"({s},{t},{random.randint(0, 15)});"

    print(edges_str[0:-1])

gen_spojny(100)


#%%
