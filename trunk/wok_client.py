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
        return result

class WokResultToNtriple(object):
    def __init__(self, search_results, prefix="http://link.informatics.stonybrook.edu/pub/"):
        self.search_results
    
    def wok_result_to_ntriples(self):

        for search_result in search_results.records:
            pprint.pprint(search_result)
            try:
                authors = search_result.authors
            except AttributeError:
                authors = None

            try:
                keywords = search_result.keywords
            except AttributeError:
                keywords = None

            try:
                title = search_result.title
            except AttributeError:
                title = None

            try:
                source = search_result.source
            except AttributeError:
                source = None

    def authors(self,authors):
        pass

    def author(self,author):
        pass

    def keywords(self,keywords):
        pass

    def source(self, source):
        pass


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
        wok_result_to_ntriples(r)
        #pprint.pprint(r)
        woks.close()
