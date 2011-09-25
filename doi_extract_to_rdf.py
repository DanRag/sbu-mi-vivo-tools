import httplib2
import sys
import re

def curl(uri,headers={}):
    http_client = httplib2.Http()
    response, content = http_client.request(uri, "GET", body=None, headers = headers)
    if response:
        return content
    else:
        return None


def curl_content_negotiation(uri,content_type):
    return curl(uri,{"Accept" : content_type})

def main(uri):
    re_doi = re.compile(r'(Doi|doi|DOI)[: ]+([0-9a-zA-Z./]+)')
    source = curl(uri)
    if source:
        for line in source.split("\n"):
            
            match_doi = re_doi.search(line)
            if match_doi:
                result_groups = match_doi.groups()
                doi = result_groups[1].rstrip()
                if doi[-1] == ".":
                    doi = doi[0:-1]
                doi_uri = "http://dx.doi.org/" + doi

                content = curl_content_negotiation(doi_uri, "text/turtle")
                if "DOI Not Found" in content:
                    pass#print("DOI not found %s" % doi
                else:
                    print(content)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main("http://www.somas.stonybrook.edu/people/liuy.html")