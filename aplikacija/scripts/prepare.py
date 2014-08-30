from podaci.models import Beer, Review, UpdateBeer
from django.utils import timezone
import pickle
import sys
import random

#function for reading pickle file and database for analysis
def create_beer_city():
	reviews = Review.objects.all()
	#print sys.path[0]
	f = open(sys.path[1]+'/../pycode/files/usersS.txt','rb')
	users = pickle.load(f)
	f.close()
	city = dict()
	city_users = dict()
	for review in reviews:
		if review.user in users.keys():
			if users[review.user][1] not in city.keys():
				city[users[review.user][1]] = 1
				city_users[users[review.user][1]] = [review.user]
			else:
				city[users[review.user][1]] += 1
				city_users[users[review.user][1]].append(review.user)
	L = sorted(city.items(), key=lambda (k, v): v)
	print L[len(L) - 30:len(L)]
	f = open(sys.path[1]+'/../pycode/files/city_count.txt','wb')
	a = dict()
	for i in L[len(L) - 30:len(L)]:
		a[i[0]] = city_users[i[0]]
	pickle.dump([L[len(L) - 30:len(L)],a],f)
	f.close()

#function used by google maps
def det_grades_and_users():
	f = open(sys.path[1]+'/../pycode/files/city_count.txt','rb')
	cities = pickle.load(f)
	print cities[1].keys()
	f.close()
	grades = {}
	for city in cities[1].keys():
		print len(cities[1][city])
		grades[city] = {}
		random.shuffle(cities[1][city])
		l = len(cities[1][city])/20
		for us in cities[1][city][:l]:
			reviews = Review.objects.filter(user = us)
			m = len(reviews)
			for i in xrange(0,m,10):
				if reviews[i].beer not in grades[city].keys():
					grades[city][reviews[i].beer] = [float(reviews[i].grade)]
				else:
					grades[city][reviews[i].beer].append(float(reviews[i].grade))
	for city in grades.keys():
		for beer in grades[city].keys():
			grades[city][beer] = sum(grades[city][beer])/(len(grades[city][beer])*1.0)
		L = sorted(grades[city].items(), key=lambda (k, v): v)
		print city, L[-1][0], L[-1][1], L[-2][0], L[-2][1]
