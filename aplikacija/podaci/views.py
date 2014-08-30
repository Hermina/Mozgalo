from django.shortcuts import render
from django.http import HttpResponse
from podaci.models import Beer, Review, UpdateBeer
import scripts.upload as upl
import scripts.recommender as rec
import scripts.google_recommender as g
import scripts.algorithms as alg
import scripts.analysis as an
from django.utils import timezone
import sys
from var_dump import var_dump

def index(request):
    context = {}
    return render(request, 'podaci/index.html', context)

#################### UPDATE DATA ########################

"""
Find last stored date in database(for all beers)
and refresh data from sources
"""
def update(request):
    beersList = upl.topList()
    good_rev = 0
    for beer in beersList:
        try:
            q = UpdateBeer.objects.get(beerName=beer[0][1].replace('/','-'))
            b = Beer.objects.get(name=beer[0][1].replace('/','-'))
            reviews = upl.findData(beer,q.date)
            checker = False
            for review in reviews:
                r = upl.parseReview(review)
                if len(r) != 10: # if unicode error skip
                    continue
                #set new update data
                if checker == False:
                    q.date = r[9]
                    checker = True
                    q.save()
                ########## calculus ###################
                result = alg.new_grade(r[8])
                all_review_by_beer = Review.objects.filter(beer_id=b.id)
                old_counter = len(all_review_by_beer)
                b.rDev = "{0:.2f}".format((float(b.rDev)*old_counter + float(result[0]))/(old_counter+1))
                b.look = "{0:.2f}".format((float(b.look)*old_counter + float(result[1]))/(old_counter+1))
                b.smell = "{0:.2f}".format((float(b.smell)*old_counter + float(result[2]))/(old_counter+1))
                b.taste = "{0:.2f}".format((float(b.taste)*old_counter + float(result[3]))/(old_counter+1))
                b.feel = "{0:.2f}".format((float(b.feel)*old_counter + float(result[4]))/(old_counter+1))
                b.overall = "{0:.2f}".format((float(b.overall)*old_counter + float(result[5]))/(old_counter+1))
                b.save() # save new data about some beer
                #add review
                b.review_set.create(user = r[0], grade = result[0], rDev = "#",
                                    look = result[1], smell = result[2], taste = result[3],
                                    feel = result[4], overall = result[5], text = r[8],
                                    data = r[9], created = timezone.now())
                good_rev +=1 # counting good reviews
        except:
            # @TODO catch errors about storing data (if new -> create new)
            continue

    context = {'good': good_rev}
    return render(request, 'podaci/update_info.html', context)

"""
Start the whole process
"""
def full_update(request):
    context = {}
    return render(request, 'podaci/full_update.html', context)

def manually(request):
    beers = Beer.objects.all()
    context = {'beers' : beers}
    return render(request, 'podaci/manually.html', context)

"""
Save partial data by beer or save user comment (nacin = 1 user, nacin = 2 partial update)
"""
def storing(request):
    context = {}
    try:
        # open beer by name
        b = Beer.objects.get(pk=request.GET.get('pivo'))
        # if user create comment
        if request.GET.get('nacin') == '1':
            ################ calculus ###################
            result = alg.new_grade_sin(request.GET.get('textarea').encode('utf-8'))
	    context = {'podatak':2}
            all_review_by_beer = Review.objects.filter(beer_id=b.id)
            old_counter = len(all_review_by_beer)
            b.rDev = "{0:.2f}".format((float(b.rDev)*old_counter + float(result[0]))/(old_counter+1))
            b.look = "{0:.2f}".format((float(b.look)*old_counter + float(result[1]))/(old_counter+1))
            b.smell = "{0:.2f}".format((float(b.smell)*old_counter + float(result[2]))/(old_counter+1))
            b.taste = "{0:.2f}".format((float(b.taste)*old_counter + float(result[3]))/(old_counter+1))
            b.feel = "{0:.2f}".format((float(b.feel)*old_counter + float(result[4]))/(old_counter+1))
            b.overall = "{0:.2f}".format((float(b.overall)*old_counter + float(result[5]))/(old_counter+1))
            b.save() # save new data
            b.review_set.create(user = 'NoName', grade = result[0], rDev = '#',
                                            look = result[1], smell = result[2], taste = result[3],
                                            feel = result[4], overall = result[5], text = request.GET.get('textarea'),
                                            data = 'NoDate', created = timezone.now())
            # user view in browser
            category = ['Ocjena', 'Izgled', 'Miris', 'Okus', 'Osjecaj','Opcenito']
            value = zip(result, category)
            context = {'podatak' : b.name, 'result' : value, 'comment': request.GET.get('textarea')}
            return render(request, 'podaci/user_storing.html', context)
        # if user start update by beer name
        elif request.GET.get('nacin') == '2':
            beerLink = None
            # open file with beer name and link on resource
            beer = UpdateBeer.objects.get(beerName = b.name )
            f = open(sys.path[0]+'/../datares3/toplist.txt','r')
            lines = f.readlines()

            # find user beer in file (because need link)
            for line in lines:
                # line.encode('utf-8')
                beerName = line[line.find(']')+2:line[1:].find('[')]
                if beerName.decode('utf-8') == b.name:
                    beerLink = line[line.find('[')+1:line.find(']')]
                    break
            # unicode: in some case can not find bear
            if beerLink == None:
                raise "Wrong", beerLink

            updateBeer = [[beerLink,beerName]] # create data for findData func
            reviews = upl.findData(updateBeer,beer.date)
            checker = False
            # # store new review
            for review in reviews:
                r = upl.parseReview(review)
                if len(r) != 10: # if unicode error skip
                    continue
                # set new update data
                if checker == False:
                    beer.date = r[9]
                    checker = True
                    beer.save()
                ######### calculus ###################
                result = alg.new_grade(r[8].encode('utf-8'))
                all_review_by_beer = Review.objects.filter(beer_id=b.id)
                old_counter = len(all_review_by_beer)
                b.rDev = "{0:.2f}".format((float(b.rDev)*old_counter + float(result[0]))/(old_counter+1))
                b.look = "{0:.2f}".format((float(b.look)*old_counter + float(result[1]))/(old_counter+1))
                b.smell = "{0:.2f}".format((float(b.smell)*old_counter + float(result[2]))/(old_counter+1))
                b.taste = "{0:.2f}".format((float(b.taste)*old_counter + float(result[3]))/(old_counter+1))
                b.feel = "{0:.2f}".format((float(b.feel)*old_counter + float(result[4]))/(old_counter+1))
                b.overall = "{0:.2f}".format((float(b.overall)*old_counter + float(result[5]))/(old_counter+1))
                b.save()
                b.review_set.create(user = r[0], grade = result[0], rDev = "#",
                                    look = result[1], smell = result[2], taste = result[3],
                                    feel = result[4], overall = result[5], text = r[8],
                                    data = r[9], created = timezone.now())
            context = {'podatak' : b.name }
            f.close()
        else:
            # if wrong nacin
            raise "Invalid type", request.GET.get('nacin')
    except Exception, err:
        # wrong : nacin, storing, beerLink
	print err
        return render(request, 'podaci/storing_error.html', context)

    return render(request, 'podaci/storing.html', context)

########### END UPDATE #################################

########### ANALYSIS ###################################
"""
Represent top analysis.
For the client, it is the first page about analysis.
"""
def analysis_index(request):
    context = {}
    return render(request, 'podaci/analysis_index.html', context)

def analysis_basic(request):
    context = {}
    result = an.analysis_top()
    look = zip(result[0], result[1])
    smell = zip(result[2], result[3])
    taste = zip(result[4], result[5])
    feel = zip(result[6], result[7])
    grade = zip(result[8], result[9])
    context = {'look': look, 'smell': smell,'taste':taste, 'feel':feel, 'grade': grade}
    return render(request, 'podaci/analysis_basic.html', context)

def analysis_google_map(request):
    context={}
    return render(request, 'podaci/analysis_google.html', context)

def analysis_vs(request):
    beers = Beer.objects.all()
    context = {'beers' : beers}
    return render(request, 'podaci/analysis_vs.html', context)

def analysis_vs_result(request):
    beer1 = Beer.objects.get(id=request.GET.get('selectbeer1'))
    beer2 = Beer.objects.get(id=request.GET.get('selectbeer2'))
    an.analysis_vs(request.GET.get('selectbeer1'),request.GET.get('selectbeer2'))
    context={'beer1': beer1.name, 'beer2': beer2.name}
    return render(request, 'podaci/analysis_vs_result.html', context)

#### Other pages of analysis #####

##################################

############## END ANALYSIS ################################


############## RECOMMENDER ################################
def recommender(request):
    beers = Beer.objects.all()
    context = {'beers' : beers[:30]}
    return render(request, 'podaci/recommender.html', context)

def recommender_result(request):
    userChoice = []
    beerId = []
    if request.GET.get('selectbeer1') != "0" and request.GET.get('selectbeer1') not in beerId:
        beerId.append(request.GET.get('selectbeer1'))
        userChoice.append([Beer.objects.get(pk=request.GET.get('selectbeer1')).name,int(request.GET.get('beer1'))])
    if request.GET.get('selectbeer2') != "0" and request.GET.get('selectbeer2') not in beerId:
        beerId.append(request.GET.get('selectbeer2'))
        userChoice.append([Beer.objects.get(pk=request.GET.get('selectbeer2')).name,int(request.GET.get('beer2'))])
    if request.GET.get('selectbeer3') != "0" and request.GET.get('selectbeer3') not in beerId:
        beerId.append(request.GET.get('selectbeer3'))
        userChoice.append([Beer.objects.get(pk=request.GET.get('selectbeer3')).name,int(request.GET.get('beer3'))])
    if request.GET.get('selectbeer4') != "0" and request.GET.get('selectbeer4') not in beerId:
        beerId.append(request.GET.get('selectbeer4'))
        userChoice.append([Beer.objects.get(pk=request.GET.get('selectbeer4')).name,int(request.GET.get('beer4'))])
    if request.GET.get('selectbeer5') != "0" and request.GET.get('selectbeer5') not in beerId:
        beerId.append(request.GET.get('selectbeer5'))
        userChoice.append([Beer.objects.get(pk=request.GET.get('selectbeer5')).name,int(request.GET.get('beer5'))])

    beers = []
    users = []
    ratings = {}
    beerID = []
    tempData = Beer.objects.all()
    for beer in tempData[:30]:
        beers.append(beer.name)
        beerID.append(beer.id)

    for Id in beerID:
        reviews = Review.objects.filter(beer_id= Id)
        b_name = Beer.objects.get(id = Id).name
        for review in reviews:
            users.append(review.user)
            ratings[(b_name, review.user)] = float(review.grade)
    users = list(set(users))
    predictions = rec.recommender(beers, users[:10], ratings, userChoice)

    string = ""
    data = []
    grade=[]
    links = []
    for res in predictions:
        data.append(res[1])
        if res[0] > 5.0:
            res[0] = 5.0
        grade.append("{0:.2f}".format(res[0]))
        # @TODO google search (error in get_urls())
        #links.append(g.google(res[1].decode('utf-8'))[0])

    values = zip(data,grade)
    return render(request, 'podaci/recommender_result.html',{'values' : values})

################### END RECOMMENDER ###############################
