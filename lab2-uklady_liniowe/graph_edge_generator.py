import networkx as nx
import numpy as np

seed = 100


def gen_2d(n):
    edges_str = ""
    for i in range(n ** 2):
        if i % n != n - 1:  # patrz w prawo
            R = np.random.randint(1, 30)
            edges_str += f"({i},{i + 1}, {R});"
        if i // n != n - 1:  # patrz w doł
            R = np.random.randint(1, 30)
            edges_str += f"({i},{i + n}, {R});"

    return edges_str[0:-1]


def gen_spojny(n):
    G = nx.erdos_renyi_graph(n, 0.3, seed)

    nodes = np.arange(0, n)
    np.random.shuffle(nodes)
    for i in range(n - 1):
        G.add_edge(nodes[i], nodes[i + 1])

    edges_str = ""
    for edge in list(G.edges()):
        edges_str += f"({edge[0]},{edge[1]},{np.random.randint(1, 30)});"

    return edges_str[0:-1]


def gen_small_world(n, k, p, tries):
    G = nx.connected_watts_strogatz_graph(n=n, k=k, p=p, tries=tries)

    edges_str = ""
    for edge in list(G.edges()):
        edges_str += f"({edge[0]},{edge[1]},{np.random.randint(1, 30)});"

    return edges_str[0:-1]


def gen_bridge():
    pass


def gen_3_regular(n):
    G = nx.random_regular_graph(3, n, seed)
    edges_str = ""
    for edge in list(G.edges()):
        edges_str += f"({edge[0]},{edge[1]},{np.random.randint(1, 30)});"

    return edges_str[0:-1]


# gen_small_world(100, 4, 0.5, 50)
#gen_spojny(150)
print(gen_3_regular(120))
#%%
