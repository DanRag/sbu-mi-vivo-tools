

from pyTripleSimple import SimpleTripleStore
from pyTripleSimple import ExtractGraphFromSimpleTripleStore
import sys
import os

url_get_tail = lambda x: x[x.rfind("/")+1:]


def main(ntriple_source_file, sab_class, child_of_predicate, file_name_prefix=""):

    if sab_class.__class__ == list:
        pass
    else:
        sab_class = [sab_class]

    fu = open(ntriple_source_file,"r")
    ts = SimpleTripleStore()

    print("Loading triples")
    ts.load_ntriples(fu)
    fu.close()

    graph_obj = ExtractGraphFromSimpleTripleStore(ts)
    graph_obj.register_label()

    graph_obj.register_class()
    graph_obj.register_node_predicate("<http://link.informatics.stonybrook.edu/umls/AUI/CODE>", "code")

    graph_obj.register_node_predicate("<http://link.informatics.stonybrook.edu/umls/hasCUI>", "CUI", url_get_tail)
    graph_obj.register_node_predicate("<http://link.informatics.stonybrook.edu/umls/hasSAB>", "SAB", url_get_tail)
    graph_obj.register_node_predicate("<http://link.informatics.stonybrook.edu/umls/hasTermType>", "TTY", url_get_tail)

    base_patterns = [("aui1","sab_predicate", "sab1"), ("aui1","childOf", "aui2"), ("aui2", "sab_predicate", "sab2")]
    base_restrictions = [("sab1", "in", sab_class), ("sab2", "in", sab_class), ("childOf", "in", [child_of_predicate])]

    print("Writing results to a file")

    graph_obj.add_pattern_for_links(base_patterns, base_restrictions, ["aui1", "aui2"], "childOf")
    directory,ntriple_source_base_file_name = os.path.split(ntriple_source_file)
    graphML_base_file_name = file_name_prefix + ntriple_source_base_file_name + ".network.hierarchy.graphml"
    graphML_file_name = os.path.join(directory, graphML_base_file_name)

    fo = open(graphML_file_name, "w")
    graph_obj.translate_into_graphml_file(fo)
    fo.close()


if __name__ == '__main__':
#    umls_nt = sys.argv[1]
#    sab = sys.argv[2]
#    parent_term = sys.argv[3]
#    preferred_term_filter =  sys.argv[4]

    main("C:/users/janos/data/umls/umls_full_isf_micro.nt","<http://link.informatics.stonybrook.edu/umls/SAB/ICD9CM>","<http://link.informatics.stonybrook.edu/umls/REL#CHD>",file_name_prefix="icd9cm_")
    #main("C:/users/janos/data/umls/umls_full_isf_micro.nt","<http://link.informatics.stonybrook.edu/umls/SAB/NCI>","<http://link.informatics.stonybrook.edu/umls/RELA#isa>",file_name_prefix="nci_")
    main("/home/janos/rdf/umls_full_isf.nt","<http://link.informatics.stonybrook.edu/umls/SAB/MSH>","<http://link.informatics.stonybrook.edu/umls/REL#CHD>",file_name_prefix="msh_")