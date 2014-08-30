import pickle
import random
import numpy

from scipy.optimize import minimize

def load_data():
    file = open('beersP.txt','rb')
    pos = pickle.load(file)
    file.close()
    # file = open('beersN.txt','rb')
    # neg = pickle.load(file)
    # file.close()
    # file = open('beersS.txt','rb')
    # avg = pickle.load(file)
    # file.close()

    beers = []
    users = []
    ratings = {}

    for beer in pos.keys()[:30]:
        beers.append(beer)
        for info in pos[beer][6]:
            ratings[(beer, info[0])] = info[1] # info[0] - user, info[1] - rating (.../5)
            if info[0] not in users:
                users.append(info[0])

    # for beer in neg.keys():
    #     beers.append(beer)
    #     for info in neg[beer][6]:
    #         ratings[(beer, info[0])] = info[1]
    #         if info[0] not in users:
    #             users.append(info[0])

    # for beer in avg.keys()[:100]:
    #     if beer not in beers and avg[beer]:
    #         beers.append(beer)
    #         for info in avg[beer][6]:
    #             ratings[(beer, info[0])] = info[1]
    #             if info[0] not in users:
    #                 users.append(info[0])

    random.shuffle(users)

    return beers, users[:100], ratings

def initialize(beers, users, ratings):
    num_beers = len(beers)
    num_users = len(users)
    params = [random.uniform(-1, 1) for _ in xrange((num_beers + num_users)*5)] # beer and user features

    Y = numpy.zeros((num_beers, num_users)) # Y[i][j] = rating given by user j to beer i if defined, 0 otherwise
    R = numpy.zeros((num_beers, num_users)) # R[i][j] = 1 if user j has rated beer i if defined, 0 otherwise

    for (beer, user) in ratings:
        if user in users:
            Y[beers.index(beer)][users.index(user)] = ratings[(beer, user)]
            R[beers.index(beer)][users.index(user)] = 1

    return params, Y, R

def normalize(Y, R):
    (m, n) = Y.shape
    mean = numpy.zeros(m)
    for i in range(m):
        idx = numpy.where(R[i][:] == 1)[0]
        if idx.size:
            mean[i] = numpy.mean(Y[i][idx])
            Y[i][idx] = Y[i][idx] - mean[i]

    return Y, mean

def cost(params, Y, R, num_beers, num_users):
    X = numpy.reshape(params[:num_beers*5], (num_beers, 5)) # beer features
    Theta = numpy.reshape(params[num_beers*5:], (num_users, 5)) # user features

    return numpy.sum(numpy.power(numpy.multiply(R, numpy.dot(X, numpy.transpose(Theta)) - Y), 2)) / 2.0

def predict(user, params, beers, users, ratings, mean):
    num_beers = len(beers)
    num_users = len(users)
    user_index = users.index(user)
    theta = params[(num_beers+user_index)*5:(num_beers+user_index+1)*5]
    predictions = []

    for beer in beers:
        if (beer, user) not in ratings.keys():
            beer_index = beers.index(beer)
            x = params[beer_index*5:(beer_index+1)*5]
            predictions.append((numpy.dot(numpy.transpose(theta), x) + mean[beer_index] - 1, beer))

    predictions.sort(reverse = True)

    return predictions[:10]

def main():
    print "Loading data..."
    (beers, users, ratings) = load_data()

    print "Entering ratings for a new user..."
    users.append('new_user')
    ratings[(beers[0], 'new_user')] = 5
    ratings[(beers[1], 'new_user')] = 1
    ratings[(beers[2], 'new_user')] = 4

    print "Training collaborative filtering..."
    (params, Y, R) = initialize(beers, users, ratings)
    (Y, mean) = normalize(Y, R)
    num_beers = len(beers)
    num_users = len(users)
    result = minimize(cost, numpy.array(params), args=(Y, R, num_beers, num_users), method='BFGS', options={'maxiter': 15, 'disp': False})
    params = result.x # learned parameters

    print "Predicting beer ratings for a new user..."
    predictions = predict('new_user', params, beers, users, ratings, mean)

    print "Top recommendations:"
    for (rating, beer) in predictions:
        print "\t" + beer + " (predicted rating: " + str(rating) + ")"

if __name__ == "__main__":
    main()
