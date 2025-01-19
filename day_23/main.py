from utils import read_lines
from itertools import combinations
import networkx as nx

SAMPLE_INPUT = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""


def get_connections(connections):
    connected_sets = list()

    for from_node, to_node in connections:
        processed = False
        for connected_set in connected_sets:
            if from_node in connected_set:
                connected_set.add(to_node)
                processed = True
                break
            elif to_node in connected_set:
                connected_set.add(from_node)
                processed = True
                break
        if not processed:
            connected_sets.append(set([from_node, to_node]))
    return connected_sets


def get_connections(connections, node_count):

    connected_sets = list()

    for i, (from_node, to_node) in enumerate(connections):
        for j in range(i+1, len(connections)):
            if from_node in connections[j] or to_node in connections[j]:
                connected_sets.append(connections[j].union(connections[i]))
                break


    return connected_sets

def solve_part1():

    # G = nx.Graph()
    connections = set()
    vertices = set()
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        # print(report_line)
        from_node, to_node = report_line.split("-")
        # G.add_edge(from_node, to_node)
        connections.add((from_node, to_node))
        connections.add((to_node, from_node))
        vertices.add(from_node)
        vertices.add(to_node)

    result  = 0
    for three_nodes in combinations(vertices, 3):
        is_triangle = True
        for vertex1, vertex2 in combinations(three_nodes, 2):
            if (vertex1, vertex2) not in connections:
                is_triangle = False
                break

        if is_triangle:
            if three_nodes[0].startswith('t') or three_nodes[1].startswith('t') or three_nodes[2].startswith('t'):
                result += 1
            # print(f'Triangle: {three_nodes}')

    print(f'Found {result} triangles')


def solve_part2():

    connections = set()
    vertices = set()
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        from_node, to_node = report_line.split("-")
        # G.add_edge(from_node, to_node)
        connections.add((from_node, to_node))
        connections.add((to_node, from_node))
        vertices.add(from_node)
        vertices.add(to_node)


    edge_counnt = dict()
    for node in vertices:
        connection_count = len([from_node for from_node, _ in connections if from_node == node])
        edge_counnt[node] = connection_count

    is_triangle = False
    for node_count in range(5, len(vertices)):
        print(f'Checking {node_count} nodes')


        # filter the nodes thst have at least node_count connections
        check_vertices = []

        for nodes in combinations(check_vertices, node_count):
            is_triangle = True
            for vertex1, vertex2 in combinations(nodes, 2):
                if (vertex1, vertex2) not in connections:
                    is_triangle = False
                    break

            if is_triangle:
                print(f'Triangle: {sorted(nodes)}')
                break
                # print(f'Triangle: {three_nodes}')
        if is_triangle:
            break


if __name__ == "__main__":
    solve_part2()
