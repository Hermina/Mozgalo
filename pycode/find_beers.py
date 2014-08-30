import google_search.google_find_urls as gs
from time import sleep

#in progress
def find_beers():
    beers = [line.rstrip() for line in open('beer_list.txt')]
    #keywords = [line.rstrip() for line in open('keywords.txt')]

    # beeradvocate
    file = open('beeradvocate.urls','w')
    for b in beers:
        file.write(gs.findUrl(b+' beeradvocate',1)[0]+'\n')
        print b+' beeradvocate'
        print gs.findUrl(b+' beeradvocate',1)[0]+'\n'
        sleep(60)
    file.close()

