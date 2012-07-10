"""
    This is an experimental script for interacting with the SOAP interface
    of Thomson Reuters Web of Knowledge (formerly Web of Science) Lite interface which is
    available to organizations which subscribe to it.

    It requires that you have the Python SUDS library installed.

"""

import suds
import logging
import pprint
import sys
import time
from wok_util import author_process_abbreviated as author_process

logging.basicConfig(level=logging.INFO)

class WebOfKnowledgeService(object):
    def __init__(self):
        self.wok_auth_uri = "http://search.isiknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate?wsdl"
        self.wok_uri = "http://search.isiknowledge.com/esti/wokmws/ws/WokSearchLite?wsdl"

    def open(self):
        """Authenticate against the WOK auth server"""
        self.auth_client = suds.client.Client(self.wok_auth_uri)
        self.auth_result = self.auth_client.service.authenticate()
        self.wok_client = suds.client.Client(self.wok_uri)
        self.wok_client.set_options(headers = {"Cookie" : '[SID="%s"]' % self.auth_result})
        self.auth_client.set_options(headers = {"Cookie" : '[SID="%s"]' % self.auth_result})
    def close(self):
        """Close the session"""
        result = self.auth_client.service.closeSession()
        logging.info(result)

    def search(self, search_query, record_count = 100, first_record = 1):
        """Perform a search of WOK"""
        queryParameters = self.wok_client.factory.create("queryParameters")
        queryParameters.databaseID = "WOS"
        queryParameters.queryLanguage = "en"
        queryParameters.userQuery = search_query
        queryParameters.editions= [{"collection" : "WOS", "edition" : "SCI"}]


        retrieveParameters = self.wok_client.factory.create("retrieveParameters")
        retrieveParameters.count = record_count
        retrieveParameters.firstRecord = first_record

        result = self.wok_client.service.search(queryParameters,retrieveParameters)
        return WokResults(result)

class WokResults(object):
    def __init__(self, search_results, prefix="http://link.informatics.stonybrook.edu/pub/"):
        self.search_results = search_results
        self.prefix = prefix

    def to_ntriples(self):
        return self._process_xml()
    
    def _process_xml(self):
        results = []
        for search_result in self.search_results.records:
            result_dict = {}
            result_dict["authors"] = []
            result_dict["id"] = search_result.UT
            result_dict["extract_date"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            result_dict["extract_source"] = "ISI Web of Knowledge"
            try:
                author_list_raw =  self.authors(search_result.authors)
                for article_author in author_list_raw:
                    result_dict["authors"].append(author_process(article_author))
            except AttributeError:
                authors = None

            try:
                keywords = search_result.keywords
                result_dict["keywords"] = keywords[0].values
            except AttributeError:          
                keywords = None

            try:
                title = search_result.title
                result_dict["title"] = title[0].values[0]
            except AttributeError:
                title = None

            try:
                source_xml = search_result.source
                result_dict["source"] = self.source(source_xml)

            except AttributeError:
                raise

            pprint.pprint(result_dict)
            results.append(result_dict)
            #pprint.pprint(results)

    def authors(self,authors_xml):
        author_list = authors_xml[0].values
        return author_list

    def source(self, source_xml):
        source_dict = {}
        for value_pair in source_xml:
            if value_pair.label == "Volume":
                source_dict["volume"] = value_pair.values[0]
            if value_pair.label == "SourceTitle":
                source_dict["title"] = value_pair.values[0]
            if value_pair.label == "Pages":
                page_range = value_pair.values[0]
                source_dict["page_range"] = page_range
                start_page, end_page = tuple(page_range.split("-"))
                source_dict["start_page"] = start_page
                source_dict["end_page"]  = end_page
            if value_pair.label == "Issue":
                source_dict["issue"] = value_pair.values[0]
            if value_pair.label == "Published.BiblioYear":
                source_dict["year"] = value_pair.values[0]

        return source_dict

a="""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

<http://dx.doi.org/10.1029/2003GL019117>
    <http://purl.org/dc/terms/identifier> "10.1029/2003GL019117";
    <http://www.w3.org/2002/07/owl#sameAs> <info:doi/10.1029/2003GL019117>, <doi:10.1029/2003GL019117>;
    <http://prismstandard.org/namespaces/basic/2.1/doi> "10.1029/2003GL019117";
    <http://purl.org/ontology/bibo/doi> "10.1029/2003GL019117";
    <http://purl.org/dc/terms/date> "2004";
    <http://purl.org/ontology/bibo/volume> "31";
    <http://prismstandard.org/namespaces/basic/2.1/volume> "31";
    <http://purl.org/dc/terms/title> "An analytical expression for predicting the critical radius in the autoconversion parameterization";
    a <http://purl.org/ontology/bibo/Article>;
    <http://purl.org/dc/terms/isPartOf> <http://id.crossref.org/issn/0094-8276>;
    <http://purl.org/dc/terms/creator> <http://id.crossref.org/contributor/yangang-liu-3ar8p7ef9uza0> .

<http://id.crossref.org/issn/0094-8276>
    <http://purl.org/dc/terms/title> "Geophysical Research Letters";
    <http://purl.org/ontology/bibo/issn> "0094-8276";
    <http://prismstandard.org/namespaces/basic/2.1/issn> "0094-8276";
    <http://purl.org/dc/terms/hasPart> <http://dx.doi.org/10.1029/2003GL019117>;
    a <http://purl.org/ontology/bibo/Journal>;
    <http://www.w3.org/2002/07/owl#sameAs> <urn:issn:0094-8276>;
    <http://purl.org/dc/terms/identifier> "0094-8276" .

<http://id.crossref.org/contributor/yangang-liu-3ar8p7ef9uza0>
    <http://xmlns.com/foaf/0.1/name> "Yangang Liu";
    <http://xmlns.com/foaf/0.1/givenName> "Yangang";
    <http://xmlns.com/foaf/0.1/familyName> "Liu";
    a <http://xmlns.com/foaf/0.1/Person> .

"""

if __name__ == "__main__" :
    if len(sys.argv) == 1:
        pass
    else:
        woks = WebOfKnowledgeService()
        woks.open()
        r = woks.search(sys.argv[1])
        r.to_ntriples()
        #pprint.pprint(r)
        woks.close()
