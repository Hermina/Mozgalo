import sys
sys.path.append(sys.path[0]+"/../pycode")
import beer_rater as BA
from podaci.models import Beer, Review, UpdateBeer
from django.db import transaction

"""
Script for manually fixing data in database
"""

"""
Rate all not rated comment in database.
After this script should be run beer_grade() function from storing_data
"""
@transaction.commit_manually
def update_database():
    Beer = BA.Beer_rater()

    count = 1
    reviews = Review.objects.all() # get all reviews
    for review in reviews[:5000]:
        # if review.rDev == "#":
        #     continue
        #result = [grade, look, smell, taste, feel, overall]
        result = Beer.classify(review.text.encode('utf-8'))
        count += 1
        review.grade = result[0]
        review.look = result[1]
        review.smell = result[2]
        review.taste = result[3]
        review.feel = result[4]
        review.overall = result[5]
        review.rDev = '#'
        review.save()

        if count % 1000 == 0:
            transaction.commit()
            print count, review.id
    transaction.commit()

"""
Return rating for some text
"""
def new_grade(text):
    Beer = BA.Beer_rater()
    result = Beer.classify(text)
    return result

def new_grade_sin(text):
    Beer = BA.Beer_rater()
    result = Beer.classify_sin(text)
    return result

if __name__ == '__main__':
    main()
