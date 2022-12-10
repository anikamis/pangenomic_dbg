import sys
import numpy as np
import json
import random

from edge_def import Edge as E
from node_def import Node as N
from graph_def import Graph as G


def main():
    ret = parse_args(sys.argv[1:])

    if ret is None:
        return

    files, json_outfix, k, compress, query, query_search = ret

    path = "/".join(files.split("/")[:-1])
    strainmap, graph, strains = build_all_files(path, files, k)

    if compress:
        graph, maxlen = get_non_branching(graph)


    colors = generate_colors(strains)
    nodes, strains, links = graph_to_json(graph, colors, strainmap, k, maxlen)
    write_json(nodes, strains, links, json_outfix)

    if query:
        unique = get_unique(query_search, graph, strainmap)
        graph_to_fasta(query_search, unique)

    return


def parse_args(args):
    file_list = ""
    json_outfix = ""
    k = 0
    compress = True
    query = False
    query_search = ""

    try:
        if args[0] == "-i":
            file_list = args[1]
        else:
            return print_usage()

        if args[2] == "-o":
            json_outfix = args[3]
        else:
            return print_usage()

        if args[4] == "-k":
            k = int(args[5])
        else:
            return print_usage()

        optargs = args[6:]

        if len(optargs):
            if optargs[0] == "-u":
                compress = False
                optargs = optargs[1:]

            if optargs[0] == "-q":
                query = True
                query_search = optargs[1].strip()

    except IndexError:
        return print_usage()

    return (file_list, json_outfix, k, compress, query, query_search)


def print_usage():
    print(
        "USAGE: python3 pangenome.py -i <input file> -o <output file> -k <kmer_size> [-u] [-q <query>]")
    return None


def graph_to_fasta(strain, graph):
    with open(strain + ".fasta", "w") as fp:
        for i, n in enumerate(graph.nodes.keys()):
            fp.write(">" + strain + "_unique_seq_" + str(i) + "\n")
            fp.write(n + "\n")


def filter_graph(graph, strains):
    genome = G(dict(), list())

    for n_label, n in graph.nodes.items():
        if n.strains == strains:
            genome.nodes[n_label] = n.copy()

    for e in graph.edges:
        if e.inn.strains == strains and e.outn.strains == strains:
            genome.edges.append(e.copy())

    return genome


def get_unique(query, graph, strainmaps):
    strains = {query} if query != "core" else {x for x in strainmaps.keys()}
    return filter_graph(graph, strains)


def graph_to_json(graph, colors, strainmap, k, maxlen):

    nodes = nodes_to_json(graph, colors, k, maxlen)
    strains = strains_to_json(strainmap, colors)
    links = links_to_json(graph)

    return nodes, strains, links


def write_json(nodes, strains, links, outfix):
    with open(outfix + ".json", "w") as fp:
        json.dump({"nodes": nodes, "links": links, "strains": strains}, fp)


def generate_colors(strains):
    colors = dict()

    # ensure all colors are unique
    all_colors = set(["#%06x" % random.randint(0, 0xFFFFFF)
                     for i in range(len(strains))])

    while len(all_colors) != len(strains):
        all_colors.add("#%06x" % random.randint(0, 0xFFFFFF))

    colors = dict(map(lambda i, j: (i, j), strains, list(all_colors)))

    return colors


def strains_to_json(strainmap, colors):
    strains = []

    for idx, name in strainmap.items():
        temp = dict()
        temp["id"] = idx
        temp["name"] = name
        temp["colors"] = [v for k, v in colors.items() if idx in k]

        strains.append(temp)

    return strains


def nodes_to_json(graph, colors, k, maxlen):
    nodes = []

    # hardcode max/min pixel size to 100, 4
    # scale each node size by relative length of sequence label
    def scale(x): return int((x - k)/(maxlen - k) * (100 - 4) + 5)

    for label, node in graph.nodes.items():
        temp = dict()
        temp["id"] = label
        temp["color"] = colors[frozenset(node.strains)]
        temp["strains"] = list(node.strains)
        temp["size"] = scale(len(label))
        nodes.append(temp)

    return nodes


def links_to_json(graph):
    links = []

    for e in graph.edges:
        temp = dict()
        temp["id"] = e.label
        temp["source"] = e.inn.label
        temp["target"] = e.outn.label
        links.append(temp)

    return links


def get_non_branching(graph):
    compress = G(dict(), list())
    maxlen = 0
    for n_label, n in graph.nodes.items():
        if n.is_branching():
            start = n.copy_in(
            ) if n_label not in compress.nodes else compress.nodes[n_label]
            compress.nodes[n.label] = start

            for out_edge, out_node in n.outgoing.items():

                curr_end = out_node
                label = curr_end.label

                count = 0

                while not curr_end.is_branching():
                    count += 1

                    next_edge, next_node = list(curr_end.outgoing.items())[0]

                    if not next_node.is_branching():
                        label += next_edge

                    curr_end = next_node

                end = curr_end.copy_out(
                ) if curr_end.label not in compress.nodes else compress.nodes[curr_end.label]
                compress.nodes[end.label] = end

                if count == 0:
                    compress.nodes[end.label].incoming[out_edge] = start
                    compress.nodes[start.label].outgoing[out_edge] = end
                    compress.edges.append(E(start, end))
                else:
                    middle = N(label)
                    middle.incoming[out_edge] = start
                    middle.outgoing[next_edge] = end
                    middle.strains = start.strains | end.strains

                    compress.nodes[start.label].outgoing[out_edge] = middle
                    compress.nodes[end.label].incoming[next_edge] = middle

                    compress.edges.append(E(start, middle))
                    compress.edges.append(E(middle, end))

                    compress.nodes[middle.label] = middle
                    maxlen = len(middle.label) if len(
                        middle.label) > maxlen else maxlen
    return compress, maxlen


def build_graph_from_seq(strain, seq, k, graph=None):
    nodes = dict() if graph is None else graph.nodes
    edges = list() if graph is None else graph.edges
    strains = set()

    for i in range(len(seq) - k + 1):
        if (i + k) == len(seq):
            nodes[seq[i:i+k]].strains.add(strain)
            break

        in_mer = seq[i:i+k]
        out_mer = seq[i+1:i+k+1]
        e_mer = out_mer[-1]

        if in_mer not in nodes:
            nodes[in_mer] = N(in_mer)
        if out_mer not in nodes:
            nodes[out_mer] = N(out_mer)

        in_node = nodes[in_mer]

        new_edge = False
        if e_mer in in_node.outgoing:
            out_node = in_node.outgoing[e_mer]
        else:
            new_edge = True
            out_node = nodes[out_mer]
            in_node.outgoing[e_mer] = out_node

        out_node.incoming[e_mer] = in_node

        in_node.strains.add(strain)
        out_node.strains.add(strain)

        strains.add(frozenset(in_node.strains))
        strains.add(frozenset(out_node.strains))

        if new_edge:
            edge = E(in_node, out_node)
            edges.append(edge)

    return G(nodes, edges), strains


def read_seq(infile):
    seq = np.str_("")

    with open(infile, 'r') as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            if line[0] == ">":
                continue

            seq += line

    return seq


def build_all_files(path, files, k):
    filemap = dict()
    strain_combs = set()

    graph = G()
    with open(files, "r") as fnames:
        for fidx, file in enumerate(fnames.readlines()):
            filemap[fidx] = file.strip().split('.')[0].split('/')[-1]
            seq = read_seq(path + '/' + file.strip())
            graph, strains = build_graph_from_seq(fidx, seq, k, graph)
            strain_combs.update(strains)

    return filemap, graph, strain_combs


if __name__ == "__main__":
    main()
