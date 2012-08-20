import httplib2
import sys
import urllib

def main(site, username, password, tbox="TBOX",abox="ABOX",file_name = None):
    """Script logs into a VIVO 1.5 website and extracts ABOX and TBOX RDF data. No need to go directly
    to the underlying Jena storage but as we dump the entire data model."""

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
    if file_name is not None:
        f = open(file_name,"w")
    else:
        f=None
    if tbox:
        resp,cont = h.request(site + '/export?subgraph=tbox&assertedOrInferred=asserted&format=N-TRIPLE&submit=Export',headers=headers)
        if file_name is not None:
            f.write(cont)
        else:
            print(cont)
    if abox:
        resp,cont = h.request(site + '/export?subgraph=abox&assertedOrInferred=asserted&format=N-TRIPLE&submit=Export',headers=headers)
        if file_name is not None:
            f.write(cont)
        else:
            print(cont)

    if file_name is not None:
        f.close()

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        site = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
        tbox = None
        abox = None
        if len(sys.argv) >= 5:
            if sys.argv[4] == "TBOX":
                tbox="TBOX"
            elif sys.argv[4] == "ABOX":
                abox="ABOX"
        if len(sys.argv) >= 6:
            if sys.argv[5] == "TBOX":
                tbox="TBOX"
            elif sys.argv[5] == "ABOX":
                abox="ABOX"
        if len(sys.argv) == 4:
            tbox = "TBOX"
            abox = "ABOX"

        main(site, username, password,tbox,abox)
    else:
        print("""Usage:
python extract_rdf_data_from_vivo_site.py 'http://reach.suny.edu' username password [TBOX] [ABOX]

Logs into a remote VIVO 1.5 site and downloads ABOX and TBOX RDF serialized as ntriples to the
standard output.
""")