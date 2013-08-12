__author__ = 'janos'

import pyTripleSimple
import json
import httplib
import urllib2
import csv


def pubmed_info(pmid):
    base_server = "link.informatics.stonybrook.edu"
    base_app = "/weaver/"
    service_fragment = "pubmed2abstract?pmid=%s" % urllib2.quote(str(pmid))
    conn = httplib.HTTPConnection(base_server,timeout=180)
    conn.request("GET", base_app + service_fragment)

    resp = conn.getresponse()
    result_set = []
    if str(resp.status)[0] == "2":
        response = resp.read()

        article_information = json.loads(response)
        return article_information
    else:
        print("Call to server timed out")
        return []


def main(vivo_triple_file_name, regenerate_json_from_vivo=False, regenerate_pubmed_article_details=False, regenerate_csv=True):

    pubmed_lookup_results = None
    pmid_author_json = vivo_triple_file_name + ".pmid.author.json"
    pmid_information_json = vivo_triple_file_name + ".pmid.info.json"

    if regenerate_json_from_vivo:
        generate_json_extracted_from_vivo(vivo_triple_file_name)

    with open(vivo_triple_file_name + ".pmid.json","r") as f:
        pmid_result = json.load(f)

    if regenerate_pubmed_article_details:
        vivo_pubmed_pmid_json = vivo_triple_file_name + ".pmid.json"
        with open(vivo_pubmed_pmid_json,"r") as f:
            pmid_result = json.load(f)

        pubmed_lookup_results = []

        n_pmids = len(pmid_result)
        i = 0
        for result in pmid_result:
            pmid = result[0][1][1:-1]
            print("Extracting information for %s; %s out of %s" % (pmid, i + 1, n_pmids))
            pubmed_info_result = pubmed_info(str(pmid))

            if len(pubmed_info_result):
                pubmed_lookup_results += [pubmed_info_result]

            i += 1

        with open(pmid_information_json,"w") as fw:
            json.dump(pubmed_lookup_results, fw)

    if regenerate_csv:

        if pubmed_lookup_results is None:
            with open(pmid_information_json,"r") as f:
                pubmed_lookup_results = json.load(f)

        pubmed_details_dict = {}
        for result in pubmed_lookup_results:
            abstract = result[0]["abstract"]
            pmid = result[0]["pmid"]
            pub_date = result[0]["pub_date"].encode("utf8","ignore")
            title = result[0]["title"]
            if abstract is not None:
                abstract = ""

            for i in range(1,len(result)):
                abstract += (" " + result[i]["abstract"])

            if abstract == "":
                has_abstract = False
            else:
                has_abstract = True

            pubmed_details_dict[pmid] = {"title" :title, "pmid":pmid, "abstract": abstract,
                                         "has_abstract": has_abstract, "pub_date": pub_date}

        pubmed_details_dict_json = "pubmed_details_dict.json"
        with open(pubmed_details_dict_json,"w") as fw:
            json.dump(pubmed_details_dict, fw)


        with open(pmid_author_json, "r") as f:
            pmid_author = json.load(f)

        vivo_column_order = ["vivoMemberURI", "vivoMember", "articleURI", "pmid"]
        pmid_author_dict = {}
        for result in pmid_author:
            data = result[0]
            data_dict = {"vivoMemberURI": data[0], "vivoMember": data[1][1:-1], "articleURI": data[2],"pmid": data[3][1:-1]}
            pmid_author_dict[data[2] + "." + data[3]] = data_dict

        pmid_author_dict_json = "pmid_author_dict.json"
        with open(pmid_author_dict_json,"w") as fw:
            json.dump(pmid_author_dict_json, fw)

        pmid_details_column_order = ["title","abstract","has_abstract", "pub_date"]

        csv_export_file_name = vivo_triple_file_name + ".pubmed.csv"
        with open(csv_export_file_name,"wb") as fwc:
            csv_writer = csv.writer(fwc)
            header = vivo_column_order + pmid_details_column_order
            csv_writer.writerow(header)
            for pmid_author in pmid_author_dict:
                row_to_write = []
                pmid_author_data = pmid_author_dict[pmid_author]
                pmid = pmid_author_data["pmid"]
                for vivo_column in vivo_column_order:
                    row_to_write += [pmid_author_data[vivo_column]]

                if pmid in pubmed_details_dict:
                    pmid_detail = pubmed_details_dict[pmid]
                    for pmid_detail_column in pmid_details_column_order:
                        row_to_write += [pmid_detail[pmid_detail_column]]

                try:
                    csv_writer.writerow(row_to_write)
                except UnicodeEncodeError:
                   print(row_to_write)


def generate_json_extracted_from_vivo(vivo_triple_file_name, custom_vivo_member_type="<http://reach.suny.edu/ontology/core#SUNY_REACH_Investigator>"):

    ts = pyTripleSimple.SimpleTripleStore()

    print("Loading N-triples dump from VIVO site")
    with open(vivo_triple_file_name,"r") as f:
        ts.load_ntriples(f)
    print("Finished loading")

    result_pmid = ts.simple_pattern_match([("article","hasPmid", "pmid")], [("hasPmid", "in", ["<http://purl.org/ontology/bibo/pmid>"])], ["article", "pmid"])

    print("Extracted %s pmids from VIVO site" % len(result_pmid))

    vivo_pubmed_pmid_json = vivo_triple_file_name + ".pmid.json"

    with open(vivo_pubmed_pmid_json,"w") as fw:
        json.dump(result_pmid, fw)


    restrictions = [("a", "in", ["<" + pyTripleSimple.common_prefixes["rdf"] + "type" + ">"]),
                                      ("type", "in", [custom_vivo_member_type]),
                                      ("hasLabel", "in", ["<" + pyTripleSimple.common_prefixes["rdfs"] + "label" + ">"]),
                                      ("authorshiptype", "in", ["<http://vivoweb.org/ontology/core#Authorship>"]),
                                      ("hasPmid", "in", ["<http://purl.org/ontology/bibo/pmid>"])]

    result_author_with_pmid = ts.simple_pattern_match([("vivoMember","a", "type"),
                                      ("vivoMember", "hasLabel", "label"),
                                      ("vivoMember","authorInAuthorship","authorship"),
                                      ("authorship", "a", "authorshiptype"),
                                      ("article", "ResourceInAuthorship","authorship"),
                                      ("article", "hasPmid", "pmid")
                                      ],
                                      restrictions,
                                      ["vivoMember","label","article","pmid"]
                                      )

    print("Extracted %s associations between Pmid and author" % len(result_author_with_pmid))

    vivo_author_pmid_json = vivo_triple_file_name + ".pmid.author.json"
    with open(vivo_author_pmid_json, "w") as fw:
        json.dump(result_author_with_pmid, fw)


if __name__ == "__main__":
    main("reach_abox_2013-08-11.nt")
