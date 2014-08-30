import os
from pyquery import PyQuery as pq
import urllib2
from time import sleep


"""
Top list 250 best beers by Beeradvocate
"""
def topList():
    req = urllib2.Request('http://www.beeradvocate.com/lists/fame/',
                          headers={'User-Agent': "Magic Browser"})
    d = pq(urllib2.urlopen(req).read())
    data = d("#baContent table td span")
    beers_address = []
    for x in data:
        l = []
        for k in x.findall('a'):
            l.append([k.get("href"), k.find('b').text if k.text == None else k.text])
        if len(l) : beers_address.append(l)

    f = open('../datares3/toplist.txt','w')
    for beer in beers_address:
        string_result = ""
        string_result += '['+beer[0][0]+']('+beer[0][1]+')'
        string_result += '['+beer[1][0]+']('+beer[1][1]+')'
        string_result += '['+beer[2][0]+']('+beer[2][1]+')'
        f.write(string_result.encode('utf-8')+'\n')
    return beers_address

"""
For all beers in beersList create file ad store all comments
Directory: datares
"""
def findData():
    beers = topList()
    """
    beer[0] -> beer name
    beer[1] -> place
    beer[2] -> style
    beer[i][0] -> url
    beer[i][1] -> title
    """
    for beer in beers:
        checker = False
        beer[0][1] = beer[0][1].replace('/','-')

        # create new file if before not exist. If file exist skip step.
        if not os.path.exists('../datares3/'+beer[0][1]+'.txt'):
            f = open('../datares3/'+beer[0][1]+'.txt','w')
        else:
            continue
        print '../datares3/'+beer[0][1]+'.txt'
        path = beer[0][0]
        while True : # more then one website about some beer
            req = urllib2.Request('http://www.beeradvocate.com'+path,
                          headers={'User-Agent' : "Magic Browser"})
            d = pq(urllib2.urlopen(req).read())
            string_result = ""
            temp = d(".BAscore_big").text().split()
            string_result += temp[0]+'?--?'+temp[1]+'?--?'
            temp = d('table').find('td').eq(5).text().split()

            for i in range(len(temp)):
                if temp[i].startswith("Ratings"):
                    string_result += temp[i+1] + "?--?"
                elif temp[i].startswith("Reviews"):
                    string_result += temp[i+1]+ "?--?"
                elif temp[i].startswith("rAvg"):
                    string_result += temp[i+1]+ "?--?"
                elif temp[i].startswith("pDev"):
                    string_result += temp[i+1]+ "?--?"
                else: continue
            f.write(string_result.encode('utf-8')+'\n')

            for temp in d('#rating_fullview_container #rating_fullview_content_2'):
                string_result = ""
                string_result ='['+pq(temp).find('h6 a').attr('href')+']'+  pq(temp).text()
                f.write(string_result.encode('utf-8')+'\n')

            if checker:
                break

            # find index for next website about beer
            index = 0;
            while d('.page-group_highlight').parent().find('a').eq(index).text() != None:
                index +=1

            if index != 0:
                _next = d('.page-group_highlight').parent().find('a').eq(index-2).attr('href')
                _last = d('.page-group_highlight').parent().find('a').eq(index-1).attr('href')
            else:
                break
            print _next
            print _last
            # if current website last for some beer
            if _next == _last:
                checker = True
            path = _next
        f.close()

def main():
    findData()


if __name__ == '__main__':
    main()
