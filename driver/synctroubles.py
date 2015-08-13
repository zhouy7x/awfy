import urllib2
import re
import os

def fetchGsFileByHttp(output, repo_path):
    lines = output.splitlines()

    for l in lines:
        #m = re.search("Failed to fetch file gs://(.+) for ([\w/\-]+(\.tar\.bz2)?)", l)
        m = re.search("Failed to fetch file gs://(.+) for ([\w/\-\.]+)(\.$|,|\. )", l)

        if m:
            print("SYNC TROUBLE: try to download gs file using http.")
            objname = m.group(1)
            target = os.path.join(repo_path, m.group(2))

            url = "http://storage.googleapis.com/" + objname
            response = urllib2.urlopen(url)

            dstfile = open(target, "wb")
            dstfile.write(response.read())
            dstfile.close()

            print ("SYNC TROUBLE: download " + target + " finished.")
            return True

    return False

