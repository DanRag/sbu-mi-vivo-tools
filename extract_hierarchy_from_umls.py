

from pyTripleSimple import SimpleTripleStore
from pyTripleSimple import ExtractGraphFromSimpleTripleStore
import sys
import os

url_get_tail = lambda x: x[x.rfind("/")+1:]


def search_patterns(sab, child_of_predicate):

    if len(sab) == 1:
        base_patterns = [("aui1", "sab_predicate", "sab"), ("aui1", "childOf", "aui2"), ("aui2", "sab_predicate", "sab")]
        base_restrictions = [("sab", "in", sab), ("childOf", "in", [child_of_predicate])]

    elif len(sab) == 2:
        sab1_class = [sab[0]]
        sab2_class = [sab[1]]

        base_patterns = [("aui1", "sab_predicate", "sab1"), ("aui1", "childOf", "aui2"), ("aui2", "sab_predicate", "sab2")]
        base_restrictions = [("sab1", "in", sab1_class), ("sab2", "in", sab2_class), ("childOf", "in", [child_of_predicate])]

    return base_patterns, base_restrictions


def create_graph_obj(ts):
    graph_obj = ExtractGraphFromSimpleTripleStore(ts)
    graph_obj.register_label()

    graph_obj.register_class()
    graph_obj.register_node_predicate("<http://link.informatics.stonybrook.edu/umls/AUI/CODE>", "code")

    graph_obj.register_node_predicate("<http://link.informatics.stonybrook.edu/umls/hasCUI>", "CUI", url_get_tail)
    graph_obj.register_node_predicate("<http://link.informatics.stonybrook.edu/umls/hasSAB>", "SAB", url_get_tail)
    graph_obj.register_node_predicate("<http://link.informatics.stonybrook.edu/umls/hasTermType>", "TTY", url_get_tail)

    return graph_obj


def main(ntriple_source_file, sab_class, child_of_predicate, file_name_prefix=""):

    if sab_class.__class__ == list:
        pass
    else:
        sab_class = [sab_class]

    if len(sab_class) == 1:
        base_patterns, base_restrictions = search_patterns(sab_class, child_of_predicate)
    elif len(sab_class) == 2:
        base_patterns11, base_restrictions11 = search_patterns([sab_class[0]], child_of_predicate)
        base_patterns22, base_restrictions22 = search_patterns([sab_class[1]], child_of_predicate)
        base_patterns12, base_restrictions12 = search_patterns(sab_class, child_of_predicate)
    else:
        raise RuntimeError, "Only one or two SABs supported"

    fu = open(ntriple_source_file,"r")
    ts = SimpleTripleStore()

    print("Loading triples")
    ts.load_ntriples(fu)
    fu.close()

    directory, ntriple_source_base_file_name = os.path.split(ntriple_source_file)
    if len(sab_class) == 1:

        graphML_base_file_name = file_name_prefix + ntriple_source_base_file_name + ".network.hierarchy.graphml"
        graphML_file_name = os.path.join(directory, graphML_base_file_name)

        print("Generating Graph")

        with open(graphML_file_name, "w") as fo:
            graph_obj = create_graph_obj(ts)
            graph_obj.add_pattern_for_links(base_patterns, base_restrictions, ["aui1", "aui2"], "childOf")
            graph_obj.translate_into_graphml_file(fo)

    elif len(sab_class) == 2:

        graphML_base_file_name11 = file_name_prefix + ntriple_source_base_file_name + "11" + ".network.hierarchy.graphml"
        graphML_file_name11 = os.path.join(directory, graphML_base_file_name11)

        graphML_base_file_name22 = file_name_prefix + ntriple_source_base_file_name + "22" + ".network.hierarchy.graphml"
        graphML_file_name22 = os.path.join(directory, graphML_base_file_name22)

        graphML_base_file_name12 = file_name_prefix + ntriple_source_base_file_name + "12" + ".network.hierarchy.graphml"
        graphML_file_name12 = os.path.join(directory, graphML_base_file_name12)

        print("Outputting Graph11")
        with open(graphML_file_name11, "w") as fo:
            graph_obj = create_graph_obj(ts)
            graph_obj.add_pattern_for_links(base_patterns11, base_restrictions11, ["aui1", "aui2"], "childOf")
            graph_obj.translate_into_graphml_file(fo)

        print("Outputting Graph22")
        with open(graphML_file_name22, "w") as fo:
            graph_obj = create_graph_obj(ts)
            graph_obj.add_pattern_for_links(base_patterns22, base_restrictions22, ["aui1", "aui2"], "childOf")
            graph_obj.translate_into_graphml_file(fo)

        print("Outputting Graph12")
        with open(graphML_file_name12, "w") as fo:
            graph_obj = create_graph_obj(ts)
            graph_obj.add_pattern_for_links(base_patterns12, base_restrictions12, ["aui1", "aui2"], "childOf")
            graph_obj.translate_into_graphml_file(fo)


if __name__ == '__main__':
#    umls_nt = sys.argv[1]
#    sab = sys.argv[2]
#    parent_term = sys.argv[3]
#    preferred_term_filter =  sys.argv[4]

    #main("E:/data/umls/umls_full_isf_micro.nt","<http://link.informatics.stonybrook.edu/umls/SAB/ICD9CM>","<http://link.informatics.stonybrook.edu/umls/REL#CHD>",file_name_prefix="icd9cm_")
    #main("C:/users/janos/data/umls/umls_full_isf_micro.nt","<http://link.informatics.stonybrook.edu/umls/SAB/NCI>","<http://link.informatics.stonybrook.edu/umls/RELA#isa>",file_name_prefix="nci_")
    #main("/home/janos/rdf/umls_full_isf.nt","<http://link.informatics.stonybrook.edu/umls/SAB/MSH>","<http://link.informatics.stonybrook.edu/umls/REL#CHD>",file_name_prefix="msh_")
    main("/home/janos/rdf/umls_full_isf.nt",["<http://link.informatics.stonybrook.edu/umls/SAB/CPT>","<http://link.informatics.stonybrook.edu/umls/SAB/MTHCH>"],"<http://link.informatics.stonybrook.edu/umls/REL#CHD>",file_name_prefix="cpt_")
    #main("E:/data/umls/umls_full_isf_micro_icd9.nt",["<http://link.informatics.stonybrook.edu/umls/SAB/CPT>","<http://link.informatics.stonybrook.edu/umls/SAB/MTHCH>"],"<http://link.informatics.stonybrook.edu/umls/REL#CHD>",file_name_prefix="cpt_")
