#! /usr/bin/python

import time
import sys
import os
import pyTripleSimple
import urllib2
import httplib
import json
import pprint

def pubmed_to_cuis(pmid):
    
    base_server = "link.informatics.stonybrook.edu" 
    base_app = "/weaver/"
    service_fragment = "pubmed2cuis?pmid=%s" % urllib2.quote(str(pmid))
    conn = httplib.HTTPConnection(base_server,timeout=180)
    conn.request("GET",base_app + service_fragment)
    
    resp = conn.getresponse()
    result_set = []
    if str(resp.status)[0] =="2":
        response = resp.read()

        cuilist = json.loads(response)
        return cuilist
    else:
        print("Call to server timed out")
        return []
            

def main(ntriples_file_name,cuis_ntriples_file_name, predicate_uri = "http://purl.org/ontology/bibo/pmid"):
    f = open(ntriples_file_name,"r")
    ts = pyTripleSimple.SimpleTripleStore()
    results_ts = pyTripleSimple.SimpleTripleStore()

    print('Loading "%s"' % os.path.abspath(ntriples_file_name))
    start_time = time.clock()
    ts.load_ntriples(f)
    end_time = time.clock()
    print("Finished loading ntriples file in %s seconds" % (end_time - start_time,))

    output_triple_store =  pyTripleSimple.SimpleTripleStore()
    dc_subject = "http://purl.org/dc/elements/1.1/subject"
    pmid_to_cui_uris = ts.predicates(predicate_uri)
    print("PubMed articles found %s" % len(pmid_to_cui_uris))
    zero_counter = 0
    cuis_list = {}
    if pmid_to_cui_uris:
        i = 1
        for pmid_triple in pmid_to_cui_uris:
            pmid = pmid_triple[2][1:-1]
            cui_results = pubmed_to_cuis(pmid)
            if len(cui_results) == 0:
                zero_counter += 1
            print("Article (pmid:%s) %s of %s found %s cuis" % (pmid,i,len(pmid_to_cui_uris),len(cui_results)))
            for cui in cui_results:
                cui_uri = str(cui[u'cui'])
                cui_label = str(cui[u'cuilabel'])
                pmid_dc_triple = pmid_triple[0] + " <" + dc_subject + "> <" + cui_uri + "> .\n"
                if cuis_list.has_key(cui_uri):
                    cui_label_triple = ""
                    cuis_list[cui_uri] += 1
                else:
                    cui_label_triple = '<%s> <http://www.w3.org/2000/01/rdf-schema#label> "%s" .\n' % (cui_uri, cui_label)
                    cuis_list[cui_uri] = 1
                
                output_triple_store.load_ntriples([pmid_dc_triple + cui_label_triple])
            i+=1

    fo = open(cuis_ntriples_file_name,"w")
    output_triple_store.export_to_ntriples_file(fo)
    fo.close()
    f.close()

    pprint.pprint(cuis_list)
    print("Number of articles with no MeSH is %s out of %s" % (zero_counter,len(pmid_to_cui_uris)))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main("reach_abox_2011-08-22.nt","pubmed2cuis.nt")
    else:
        main(sys.argv[1],sys.argv[2])
    
