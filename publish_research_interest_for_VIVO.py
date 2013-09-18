__author__ = 'janos'

import pyTripleSimple

URIS = {"hasResearchArea": "<http://vivoweb.org/ontology/core#hasResearchArea>",
        "skosConcept": "<http://www.w3.org/2004/02/skos/core#Concept>",
        "umlsVivo": "<http://link.informatics.stonybrook.edu/umls>",
        "owlThing": "<http://www.w3.org/2002/07/owl#Thing>",
        "rdfType": "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>",
        "rdfsLabel": "<http://www.w3.org/2000/01/rdf-schema#label>"
       }


("<http://link.informatics.stonybrook.edu/umls>","<http://link.informatics.stonybrook.edu/umls/SUIS0023577/>","Cellular senescence")

def main(vivo_abox_ntriples_file, list_of_research_interests):

    ts = pyTripleSimple.SimpleTripleStore()
    with open(vivo_abox_ntriples_file, "r") as f:
        ts.load_ntriples(f)


    ts_export = pyTripleSimple.SimpleTripleStore()

    ntriples_text = ""
    for list_of_research_interest in list_of_research_interests:
        defined_by, urlResearchConcept, label = list_of_research_interest

        result = ts.simple_pattern_match([("s","p","o")], [("o", "in",[urlResearchConcept])])
        if len(result):
            ntriples_text += "<%s> <%s> <%s> .\n" % ()
            ntriples_text += "<%s> <%s> <%s> .\n" % ()
        else:
            pass


        """
        """



if __name__ == "__main__":
    main()