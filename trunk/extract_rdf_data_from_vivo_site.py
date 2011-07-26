import httplib2
import sys
import urllib

def main(site, username, password):
    """
    Script logs into a VIVO website and extracts ABOX and TBOX RDF data. No need to go directly
    """

    headers = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset'	: 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding'	: 'gzip,deflate,sdch',
'Accept-Language'	: 'en-US,en;q=0.8',
'Cache-Control'	 : 'max-age=0',
'Connection'	 : 'keep-alive',
'Content-Length' :	 '66',
'Content-Type'	 : 'application/x-www-form-urlencoded',
'User-Agent'	: 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30'}

    login_data = 'loginName=%s&loginPassword=%s&loginForm=Log+in' % (urllib.quote(username), urllib.quote(password))
    h = httplib2.Http()
    resp,cont = h.request(site + "/authenticate",method="POST",headers=headers, body=login_data)
    headers = {}
    headers["Cookie"] = resp["set-cookie"]

    resp,cont = h.request(site + '/export?subgraph=tbox&assertedOrInferred=asserted&format=N-TRIPLES&submit=Export',headers=headers)
    print(cont)
    resp,cont = h.request(site + '/export?subgraph=abox&assertedOrInferred=asserted&format=N-TRIPLES&submit=Export',headers=headers)
    print(cont)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        site = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]

        main(site, username, password)
    else:
        print("""Usage:
python extract_rdf_data_from_vivo_site.py 'http://reach.suny.edu' username password

Logins into a VIVO site and downloads ABOX and TBOX and outputs to standard output.
""")