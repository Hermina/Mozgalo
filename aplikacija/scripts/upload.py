import os
import re
import urllib2
from time import sleep
from pyquery import PyQuery as pq
from datetime import datetime as dt

"""
Upload list beers from www.beeradvocate.com.
List contains 250 beer.

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

    for beer in beers_address:
        string_result = ""
        string_result += '['+beer[0][0]+']('+beer[0][1]+')'
        string_result += '['+beer[1][0]+']('+beer[1][1]+')'
        string_result += '['+beer[2][0]+']('+beer[2][1]+')'
    return beers_address

"""
search web sources -> find review ->
first touch parsing (html)-> comments list
Data struct:
    beer[0] -> beer name
    beer[1] -> place
    beer[2] -> style
    beer[i][0] -> url
    beer[i][1] -> title
"""
def findData(beer, date):

    # @TODO try catch
    checker = False
    path = beer[0][0]
    newReview = [] # new beers
    while True : # more then one website about some beer
        req = urllib2.Request('http://www.beeradvocate.com'+path,
                      headers={'User-Agent' : "Magic Browser"})
        d = pq(urllib2.urlopen(req).read())

        for temp in d('#rating_fullview_container #rating_fullview_content_2'):
            string_result = ""
            string_result ='['+pq(temp).find('h6 a').attr('href')+']'+  pq(temp).text()
            new_date = re.findall(r'\d\d[-]\d\d[-]\d\d\d\d',string_result)[0]
            # @TODO parse time
            if dt.strptime(date,"%m-%d-%Y") < dt.strptime(new_date,"%m-%d-%Y"):
                newReview.append(string_result)
            else:
                checker = True
                break
        if checker: break

        # find index for next website about beer
        index = 0;
        while d('.page-group_highlight').parent().find('a').eq(index).text() != None:
            index +=1

        if index != 0:
            _next = d('.page-group_highlight').parent().find('a').eq(index-2).attr('href')
            _last = d('.page-group_highlight').parent().find('a').eq(index-1).attr('href')
        else:
            break
        # if current website last for some beer
        if _next == _last:
            checker = True
        path = _next
    return newReview

def parseReview(review):
    # @TODO parse time
    try:
        username = review.split("More by ")[-1]
        link = review[1:review.find(']')]
        rest = review.split(']' + username)[1]
        grade = re.findall(r"[-+]?\d[.]?[\d]*[ ]*[/]5", rest)[0].split(' /')[0]
        city = rest[1:rest.find(grade)-1]
        # rDev +171.7% look: 5 | smell: 5 | taste: 5 | feel: 5 |  overall: 5
        rDev = re.findall(r"rDev[ ].*%", rest)[0].split()[1]
        look = re.findall(r"look:[ ]\d[.]?[\d]*", rest)[0].split()[1]
        smell = re.findall(r"smell:[ ]\d[.]?[\d]*", rest)[0].split()[1]
        taste = re.findall(r"taste:[ ]\d[.]?[\d]*", rest)[0].split()[1]
        feel = re.findall(r"feel:[ ]\d[.]?[\d]*", rest)[0].split()[1]
        overall = re.findall(r"overall:[ ]\d[.]?[\d]*", rest)[0].split()[1]
        textBegining = review.find('overall: ' + overall) + len('overall: ' + overall)
        date = re.findall(r'\d\d[-]\d\d[-]\d\d\d\d',review)[0]
        textEnd = review.rfind("Serving type:")
        text = review[textBegining:textEnd]

        beerReview = []
        beerReview.append(str(username))
        beerReview.append(str(grade))
        beerReview.append(str(rDev))
        beerReview.append(str(look))
        beerReview.append(str(smell))
        beerReview.append(str(taste))
        beerReview.append(str(feel))
        beerReview.append(str(overall))
        beerReview.append(text)
        beerReview.append(str(date))

        return beerReview
    except:
        # @TODO catch errors (now not important)
        return []
