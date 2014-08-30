
from pygoogle import pygoogle
import urllib

"""
@param: key -> keywords i.e ("beer", "good beer"...)
        numPages -> number of pages
        save   -> False (default) return list
               -> True save in file links.txt
@return: list<links> (each website can represent
                        more elements in the list)
"""
def findUrl(key, numPages, save = False):
    g = pygoogle(key)
    g.pages = numPages
    links = g.get_urls()
    if save:
        try:
            f = open("links.txt","w")
            for link in links:
                f.write(link+"\n")
            f.close()
        except IOError:
            print "cannot open new file"
    else:
        return links

"""
@param: url -> website url
@return: string html doc
"""

def returnHtmlByUrl(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

