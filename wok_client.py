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
        self.auth_client = suds.client.Client(self.wok_auth_uri)
        self.auth_result = self.auth_client.service.authenticate()

        self.wok_client = suds.client.Client(self.wok_uri)
        self.wok_client.set_options(headers = {"Cookie" : '[SID="%s"]' % self.auth_result})
        self.auth_client.set_options(headers = {"Cookie" : '[SID="%s"]' % self.auth_result})
    def close(self):
        result = self.auth_client.service.closeSession()
        logging.info(result)

    def search(self, search_query, record_count = 100, first_record = 1):
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


if __name___== "__main__" :
    if len(sys.argv) == 1:
        pass
    else:
        woks = WebOfKnowledgeService()
        woks.open()
        r = woks.search(sys.argv[1])
        pprint.pprint(r)
        woks.close()
