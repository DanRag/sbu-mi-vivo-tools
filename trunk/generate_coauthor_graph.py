__author__ = 'Janos G. Hajagos'

"""
    Generates coauthor network between members of a VIVO database. The member
    must have the property <http://vivoweb.org/ontology/core#hasMemberRole>

    Requires that you have the py-triple-simple library in your Python path.
"""

from pyTripleSimple import SimpleTripleStore
from pyTripleSimple import ExtractGraphFromSimpleTripleStore
import sys

def main(file_name,in_network_restriction=1):
    ts = SimpleTripleStore()
    f = open(file_name)
    print("Loading triples")
    ts.load_ntriples(f)
    f.close()
    print("Generating coauthor network")
    graph_obj = ExtractGraphFromSimpleTripleStore(ts)
    graph_obj.register_label()

    base_patterns = [("a1","p1","c1"),("c1","p2","ar1"),("c2","p2","ar1"),("a2","p1","c2")]
    base_restrictions = [("p1","in",["<http://vivoweb.org/ontology/core#authorInAuthorship>"]),
        ("p2", "in", ["<http://vivoweb.org/ontology/core#linkedInformationResource>"]),
        ("c1","!=","c2")]

    if in_network_restriction:
        membership_pattern = [("a2","t","f"), ("a1","t","f")]
        membership_restriction = ("t","in", ["<http://vivoweb.org/ontology/core#hasMemberRole>"])
        base_patterns += membership_pattern
        base_restrictions.append(membership_restriction)

    graph_obj.add_pattern_for_links(base_patterns,base_restrictions,["a1","a2"],"coauthors")
    print("Writing results to a file")
    if in_network_restriction:
        graphml_file_name = file_name + ".network.coa.graphml"
    else:
        graphml_file_name = file_name + ".full.coa.graphml"
    fo = open(graphml_file_name,"w")
    graph_obj.translate_into_graphml_file(fo)
    fo.close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("""Usage:
pypy-c generate_coauthor_graph.py reach_abox_2012-03-09.nt [full]"""
            )
    else:
        if len(sys.argv) == 2:
            main(sys.argv[1])
        else:
            main(sys.argv[1],0)


