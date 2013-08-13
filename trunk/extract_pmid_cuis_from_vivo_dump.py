__author__ = 'janos'
import pyTripleSimple
import csv

def main(main_abox_ntriple_file, umls_alignment_file, csv_ouput_file, custom_vivo_member_type="<http://reach.suny.edu/ontology/core#SUNY_REACH_Investigator>"):

    ts = pyTripleSimple.SimpleTripleStore()

    print("Loading ntriples")
    with open(main_abox_ntriple_file,"r") as f:
        ts.load_ntriples(f)

    with open(umls_alignment_file, "r") as f:
        ts.load_ntriples(f)

    restrictions = [("a", "in", ["<" + pyTripleSimple.common_prefixes["rdf"] + "type" + ">"]),
                                      ("type", "in", [custom_vivo_member_type]),
                                      ("hasLabel", "in", ["<" + pyTripleSimple.common_prefixes["rdfs"] + "label" + ">"]),
                                      ("authorshiptype", "in", ["<http://vivoweb.org/ontology/core#Authorship>"]),
                                      ("hasPmid", "in", ["<http://purl.org/ontology/bibo/pmid>"]),
                                      ("dcsubject", "in", ["<http://purl.org/dc/elements/1.1/subject>"])
                                       ]
    print("Running query")
    result_author_with_pmid_cui = ts.simple_pattern_match([("vivoMember","a", "type"),
                                      ("vivoMember", "hasLabel", "label"),
                                      ("vivoMember","authorInAuthorship","authorship"),
                                      ("authorship", "a", "authorshiptype"),
                                      ("article", "ResourceInAuthorship","authorship"),
                                      ("article", "hasPmid", "pmid"),
                                      ("article", "dcsubject","cui"),
                                      ("cui", "hasLabel","cuilabel")
                                      ],
                                      restrictions,
                                      ["vivoMember","label","article","pmid","cui","cuilabel"]
                                      )

    header = ["vivoMemberURI", "vivoMember", "articleURI", "pmid", "cuiURI", "MeSH"]

    with open(csv_ouput_file, "wb") as fw:
        csv_writer = csv.writer(fw)
        csv_writer.writerow(header)
        for row in result_author_with_pmid_cui:
            data = row[0]
            csv_writer.writerow([data[0], data[1][1:-1], data[2], data[3][1:-1], data[4], data[5][1:-1]])

if __name__ == "__main__":
    main("reach_abox_2013-08-11.nt", "reach_abox_2013-08-11.nt.pmid2cuis.nt", "E:/data/alignment/cui_aligned.csv")