__author__ = 'janos'
import sys
import networkx as nx

def main(graphml_file_name, cui_file_name, extracted_file_name):

    base_uri = 'http://link.informatics.stonybrook.edu/umls/CUI/'

    imported_graph = nx.read_graphml(graphml_file_name)
    fc = open(cui_file_name,"r")

    cuis_uri_dict = {}
    for line in fc:
        sline = line.strip()
        cuis_uri_dict[base_uri + sline] = None

    nodes_to_remove = []

    for node_name in imported_graph.nodes():
        node = imported_graph.node[node_name]

        node_uri = str(node["uri"])
        if base_uri in node_uri:
            if node_uri not in cuis_uri_dict:
                nodes_to_remove.append(node_name)
    imported_graph.remove_nodes_from(nodes_to_remove)

    nx.write_graphml(imported_graph, extracted_file_name)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2],sys.argv[3])
