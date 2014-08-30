import pickle
import random
import numpy
from scipy.optimize import minimize

#data initialisation
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

#normalisation of matrix Y
def normalize(Y, R):
    (m, n) = Y.shape
    mean = numpy.zeros(m)
    for i in range(m):
        idx = numpy.where(R[i][:] == 1)[0]
        if idx.size:
            mean[i] = numpy.mean(Y[i][idx])
            Y[i][idx] = Y[i][idx] - mean[i]

    return Y, mean

#returns the value of the cost function
def cost(params, Y, R, num_beers, num_users):
    X = numpy.reshape(params[:num_beers*5], (num_beers, 5)) # beer features
    Theta = numpy.reshape(params[num_beers*5:], (num_users, 5)) # user features

    return numpy.sum(numpy.power(numpy.multiply(R, numpy.dot(X, numpy.transpose(Theta)) - Y), 2)) / 2.0

#returns a list of beers with best grades among those that haven't been graded
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

    return predictions[:5]

#uses all of the functions above and returns a prediction
def recommender(beers, users, ratings, userChoice):
    users.append('new_user') ## add new user for testing

    for choice in userChoice:
        ratings[(choice[0], 'new_user')] = choice[1] # choice = [beerName, grade]

    (params, Y, R) = initialize(beers, users, ratings)
    (Y, mean) = normalize(Y, R)
    num_beers = len(beers)
    num_users = len(users)
    result = minimize(cost, numpy.array(params), args=(Y, R, num_beers, num_users), method='BFGS', options={'maxiter': 15, 'disp': False})
    params = result.x # learned parameters
    predictions = predict('new_user', params, beers, users, ratings, mean)

    return predictions # [(,)]
