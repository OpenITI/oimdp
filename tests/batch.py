import sys
import os
import urllib.request
# import traceback
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import oimdp


if __name__ == "__main__":

    response = urllib.request.urlopen(
        "https://raw.githubusercontent.com/OpenITI/RELEASE/master/OpenITI_metatdata_2019_1_1"
    )
    release = response.read()
    release = release.decode('utf-8')

    for line in release.split("\n"):
        url = line.split('\t')[7]
        if (url.endswith('mARkdown') or url.endswith('completed')):
            # get file from GitHub
            print("Parsing " + url)
            try:
                response = urllib.request.urlopen(url)
                data = response.read()
                text = data.decode('utf-8')
                try:
                    oimdp.parse(text)
                except Exception as identifier:
                    # print(traceback.format_exc())
                    print("\tERR: ", identifier)
            except Exception as identifier:
                print("\t", identifier)
