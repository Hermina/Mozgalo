from podaci.models import Beer, Review, UpdateBeer
from django.utils import timezone
import pickle
import sys

"""
Script for manually fixing data in database
"""

"""
Function translate data from txt file to database
"""
def translate():
    # neutral reviews
    File = open(sys.path[0]+'/../pycode/files/beersO.txt','rb')
    data = pickle.load(File) # dict structure

    for key in data.keys():
        # update date (beer-> last review)
        beer = UpdateBeer(beerName=key, date=data[key][6][0][9])
        beer.save()
        # update all beers in table podaci_beer
        beer = Beer(name = key, rDev = data[key][0],
                    look = data[key][1], smell =data[key][2],
                    taste = data[key][3], feel = data[key][4],
                    overall = data[key][5] )
        beer.save()
        # find and save all reviews for some beer
        for r in data[key][6]:
            beer.review_set.create(user = r[0], grade = r[1], rDev = r[2],
                                    look = r[3], smell = r[4], taste = r[5],
                                    feel = r[6], overall = r[7], text = r[8],
                                    data = r[9], created = timezone.now())

"""
Select all review by beer and create avarage grade for all category
"""
def beer_grade():
    beers = Beer.objects.all()
    for beer in beers:
        reviews = Review.objects.filter(beer_id = beer.id)
        look = 0.0
        smell = 0.0
        taste = 0.0
        feel = 0.0
        overall = 0.0
        grade = 0.0
        count = 0
        for review in reviews:
            look += float(review.look)
            smell+= float(review.smell)
            taste+=float(review.taste)
            feel += float(review.feel)
            overall+= float(review.overall)
            grade+= float(review.grade)
            count +=1
        beer.rDev = "{0:.2f}".format(grade/count) # rDev = grade
        beer.look = "{0:.2f}".format(look/count)
        beer.smell = "{0:.2f}".format(smell/count)
        beer.taste = "{0:.2f}".format(taste/count)
        beer.feel = "{0:.2f}".format(feel/count)
        beer.overall = "{0:.2f}".format(overall/count)
        beer.save()
        #print "finished one beer"

if __name__ == '__main__':
    main()
