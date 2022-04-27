import networkx as nx
import numpy as np

seed = 100


def gen_2d(n):
    """n is length of rectangle. Nodes number is n*n"""
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


def gen_bridge(n1, n2, dim):
    """n means half of nodes"""
    G1 = nx.random_regular_graph(dim, n1, seed)
    G2 = nx.random_regular_graph(dim, n2, seed)

    G2 = nx.relabel_nodes(G2, {old_val: old_val+n1 for old_val in list(G2.nodes())})
    R = nx.compose(G1, G2)
    R.add_edge(n1-1, n1)
    edges_str = ""
    for edge in list(R.edges()):
        edges_str += f"({edge[0]},{edge[1]},{np.random.randint(1, 30)});"

    return edges_str[0:-1]

def gen_built_in_bridge(n):
    G = nx.barbell_graph(n, 0)
    edges_str = ""
    for edge in list(G.edges()):
        edges_str += f"({edge[0]},{edge[1]},{np.random.randint(1, 30)});"

    return edges_str[0:-1]


def gen_3_regular(n):
    G = nx.random_regular_graph(3, n, seed)
    edges_str = ""
    for edge in list(G.edges()):
        edges_str += f"({edge[0]},{edge[1]},{np.random.randint(1, 30)});"

    return edges_str[0:-1]


# gen_small_world(100, 4, 0.5, 50)
#gen_spojny(150)
#print(gen_3_regular(120))
#print(gen_2d(4))
#print(gen_bridge(40, 40, 3))
#print(gen_built_in_bridge(6))
