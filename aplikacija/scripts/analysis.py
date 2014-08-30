from podaci.models import Beer, Review, UpdateBeer
from django.utils import timezone
import pickle
import sys
import random
import csv

#translates beer grades per category in csv. format
def category_analysis():
	beers = Beer.objects.order_by('rDev')

	with open(sys.path[1]+'/static/json/podaci/beer_grade.csv', 'wb') as csvfile:
		f = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		pom_list = ['State','Opcenito( 50% )','Izgled( 5% )','Okus( 20% )','Miris( 15% )','Osjecaj( 10% )']
		f.writerow(pom_list)
		for beer in beers[247:]: # top
			if len(beer.name) <= 12:
				pom_list = [beer.name]
			else:
				pom_list = [beer.name[:12]+'...']
			pom_list.append(float(beer.overall))
			pom_list.append(float(beer.look))
			pom_list.append(float(beer.taste))
			pom_list.append(float(beer.smell))
			pom_list.append(float(beer.feel))
			f.writerow(pom_list)
		for beer in beers[:3]: #bottom
			if len(beer.name) <= 12:
				pom_list = [beer.name]
			else:
				pom_list = [beer.name[:12]+'...']
			pom_list.append(float(beer.overall))
			pom_list.append(float(beer.look))
			pom_list.append(float(beer.taste))
			pom_list.append(float(beer.smell))
			pom_list.append(float(beer.feel))
			f.writerow(pom_list)
		f.writerow([' ',0,0,0,0,0])

#compares grades between two beers for all categories
def analysis_vs(id1,id2):
	beer1 = Beer.objects.get(id=id1)
	beer2 = Beer.objects.get(id=id2)
	with open(sys.path[0]+'/static/json/podaci/beer_vs.tsv', 'wb') as csvfile:
		f = csv.writer(csvfile, delimiter='\t',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		f.writerow(['name','value'])
		f.writerow(['A',(float(beer1.overall)-float(beer2.overall))])
		f.writerow(['B',(float(beer1.look)-float(beer2.look))])
		f.writerow(['C',(float(beer1.smell)-float(beer2.smell))])
		f.writerow(['D',(float(beer1.taste)-float(beer2.taste))])
		f.writerow(['E',(float(beer1.feel)-float(beer2.feel))])

#returns 10 best beers per category
def analysis_top():
	beers = Beer.objects.all()
	look = []
	smell = []
	taste = []
	feel = []
	grade = []
	for beer in beers:
		look.append((beer.name,float(beer.look)))
		smell.append((beer.name,float(beer.smell)))
		taste.append((beer.name,float(beer.taste)))
		feel.append((beer.name,float(beer.feel)))
		grade.append((beer.name,float(beer.rDev)))
	look.sort(key = lambda x: x[1])
	look.reverse()
	smell.sort(key = lambda x: x[1])
	smell.reverse()
	taste.sort(key = lambda x: x[1])
	taste.reverse()
	feel.sort(key = lambda x: x[1])
	feel.reverse()
	grade.sort(key = lambda x: x[1])
	grade.reverse()
	return [[l[0] for l in look[:10]],[l[1] for l in look[:10]],[l[0] for l in smell[:10]],[l[1] for l in smell[:10]],[l[0] for l in taste[:10]],[l[1] for l in taste[:10]],[l[0] for l in feel[:10]],[l[1] for l in feel[:10]],[l[0] for l in grade[:10]],[l[1] for l in grade[:10]]]

#returns all grades per comment for the best beer
def time_analysis():
	beer = Beer.objects.get(name="Heady Topper") #insert the name of the best beer
	reviews = Review.objects.filter(beer_id=beer.id)
	with open(sys.path[1]+'/static/json/podaci/beer_graph.tsv', 'wb') as csvfile:
		f = csv.writer(csvfile, delimiter='\t',
	                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
		f.writerow(['data','close'])
		for review in reviews:
			f.writerow([review.data,float(review.grade)])

def time_analysis_full():
	reviews = Review.objects.all()
	time_analysis = dict()
	print "Start..."
	for review in reviews:
		date = review.data
		grade = float(review.grade)
		if date >= "13":
			print "skip"
			continue
		if date not in time_analysis.keys():
			time_analysis[date] = [1,grade]
		else:
			time_analysis[date][0] +=1
			time_analysis[date][1] += grade
	print "Prepare for storing..."
	for key in time_analysis.keys():
		time_analysis[key][1] = time_analysis[key][1]/time_analysis[key][0]

	print "Storing..."
	f = open(sys.path[1]+'/static/json/podaci/full_time.txt', 'wb')
	pickle.dump(time_analysis,f)
	f.close

