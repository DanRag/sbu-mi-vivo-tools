"""
    Builds an analytical RDF store that is based off of an RDF dump of a single or multiple VIVO
    installations.

    Reads in a configuration file in json format. See sample 'configuration.json' for example of formatting the file
    for a single VIVO installation.
"""

__author__ = 'Janos G. Hajagos'

import json
import sys
import pprint
import os
import time


import extract_rdf_data_from_vivo_site
import umls_alignment


def main(configuration_json):
    f=open(configuration_json,'r')
    configuration = json.load(f)
    f.close()

    i = 0
    for vivo_site in configuration["vivo-sites"]:
        base_file_name = vivo_site["name"]
        current_date_odbc = time.strftime("%Y-%m-%d",time.localtime())
        abox_file_name = base_file_name + "_abox_" + current_date_odbc + ".nt"
        tbox_file_name = base_file_name + "_tbox_" + current_date_odbc + ".nt"
        print("Dumping the ontology: %s to '%s'" % (vivo_site["site"],os.path.abspath(tbox_file_name)))
        extract_rdf_data_from_vivo_site.main(vivo_site["site"], vivo_site["username"], vivo_site["password"],tbox="TBOX", file_name=tbox_file_name, abox=None)
        print("Dumping instance data: %s to '%s'" % (vivo_site["site"],os.path.abspath(abox_file_name)))
        extract_rdf_data_from_vivo_site.main(vivo_site["site"], vivo_site["username"], vivo_site["password"],abox="ABOX", file_name=abox_file_name, tbox=None)

        vivo_site["abox_file_name"] = abox_file_name
        vivo_site["tbox_file_name"] = tbox_file_name

        print("Aligning research subject area phrases to the UMLS")

        umls_alignment_file_name = abox_file_name + ".umls.nt"
        umls_alignment.main(abox_file_name, umls_alignment_file_name)
        vivo_site["umls_alignment_file_name"] = umls_alignment_file_name
        
        i += 1

    pprint.pprint(configuration)






if __name__ == "__main__":
    if len(sys.argv) == 1:
        print """Usage:
python build_vivo_analytic_site.py configuration.json
"""
    else:
        main(sys.argv[1])