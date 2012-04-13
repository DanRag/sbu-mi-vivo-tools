__author__ = 'Janos G. Hajagos'

"""
    Generates coauthor network between members of a VIVO database. The member
    must have the property <http://vivoweb.org/ontology/core#hasMemberRole>

    Requires that you have the py-triple-simple library in your Python path.
"""

from pyTripleSimple import SimpleTripleStore
from pyTripleSimple import ExtractGraphFromSimpleTripleStore
import sys

def main(file_name):
    ts = SimpleTripleStore()
    f = open(file_name)
    print("Loading triples")
    ts.load_ntriples(f)
    f.close()
    print("Generating coauthor network")
    graph_obj = ExtractGraphFromSimpleTripleStore(ts)
    graph_obj.register_label()
    graph_obj.add_pattern_for_links([("a1","p1","c1"),("a1","t","f"),("c1","p2","ar1"),("c2","p2","ar1"),("a2","p1","c2"),("a2","t","f")],
                                     [("p1","in",["<http://vivoweb.org/ontology/core#authorInAuthorship>"]),
                                         ("p2", "in", ["<http://vivoweb.org/ontology/core#linkedInformationResource>"]),
                                         ("t","in", ["<http://vivoweb.org/ontology/core#hasMemberRole>"]),
                                         ("c1","!=","c2")],["a1","a2"],"coauthors")
    print("Writing results to a file")
    fo = open(file_name + ".coa.graphml","w")
    graph_obj.translate_into_graphml_file(fo)
    fo.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""Usage:
pypy-c generate_coauthor_graph.py reach_abox_2012-03-09.nt"""
            )
    else:
        main(sys.argv[1])


