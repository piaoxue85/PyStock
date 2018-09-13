
import csv
import random
import math
import operator

import itertools

import knndata
import sharedfunctions as fn

from timeit import default_timer as timer
import datetime as dt

import glob

#Example of kNN implemented from Scratch in Python
#ORIGINAL SOURCE CODE - NOT EDITABLE

def loadDataset(filename, split, trainingSet=[] , testSet=[]):
	with open(filename, 'rb') as csvfile:
	    lines = csv.reader(csvfile)
	    dataset = list(lines)

	    #For sample data iris.data
            #z = 4
	    z = len(dataset[0])-1
	    
	    for x in range(len(dataset)-1):
                for y in range(z):
	            dataset[x][y] = float(dataset[x][y])
	        if random.random() < split:
	            trainingSet.append(dataset[x])
	        else:
	            testSet.append(dataset[x])

def euclideanDistance(instance1, instance2, length):
        distance = 0
        for x in range(length):
                distance += pow((instance1[x] - instance2[x]), 2)
        return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
        distances = []
        length = len(testInstance)-1
        for x in range(len(trainingSet)):
                dist = euclideanDistance(testInstance, trainingSet[x], length)
                distances.append((trainingSet[x], dist))
        distances.sort(key=operator.itemgetter(1))
        neighbors = []
        for x in range(k):
                neighbors.append(distances[x][0])
        return neighbors

def getResponse(neighbors):
        classVotes = {}
        for x in range(len(neighbors)):
                response = neighbors[x][-1]
                if response in classVotes:
                        classVotes[response] += 1
                else:
                        classVotes[response] = 1
        sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedVotes[0][0]

def getAccuracy(testSet, predictions):
        correct = 0
        for x in range(len(testSet)):
                if testSet[x][-1] == predictions[x]:
                        correct += 1
        return (correct/float(len(testSet))) * 100.0

def main():
	# prepare data
	trainingSet=[]
	testSet=[]
	split = 0.67
	loadDataset('iris.data', split, trainingSet, testSet)
	print 'Train set: ' + repr(len(trainingSet))
	print 'Test set: ' + repr(len(testSet))
	# generate predictions
	predictions=[]
	k = 3
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')


def testrun():
        main()
	
# main()

#ORIGINAL SOURCE CODE - NOT EDITABLE

def getKeys(dataset):

        headers = []
        lines = []
        
        headers = dataset[0]
        
        r = len(dataset)
        keylist = []
        c = len(dataset[0])

        for i in range(0, c):
                
                j = -1 
                try:
                        j = headers.index(headers[i]+"CHG")
                except ValueError:
                        j = -1

                k = -1 
                try:                        
                        k = headers.index(headers[i][:-3])
                except ValueError:
                        k = -1

                #Rule out absolute value                        
                #if j >0:
                #        keylist.append([i ,j])
                #        print headers[i] + ', ' + headers[j]

                #if j < 0 and k < 0:
                #        keylist.append([i])
                #        print headers[i]

                if headers[i][-3:] == "CHG":
                        keylist.append([i])
                        #fn.dprint(headers[i])

        return keylist


#Return rows with selected columns
def selectRows(dataset, rangeFrom, rangeTo, column=[]):

        resultSet = []
        for x in range(rangeFrom, rangeTo):
                d = []
                for y in column:
                        try:
                                d.append(float(dataset[x][y]))
                        except:
                                d.append(dataset[x][y])
                resultSet.append(d)

        return resultSet

#KNN.loadDataset() separates data into training set and test set randomly by a given ratio
#The training set of stock data should be in date sequence.
#KNN.splitData() is a replacement function of KNN.loadDataset which separates data into training set and test set in date sequence.
def splitData(dataset, trainingSize, testSize, column=[]):

        r = trainingSize + testSize

        trainingSet = []
        testSet = []
        problemSet = []

        tr = []
        te =[]
        
        for x in range(1, r):
                d = []
                for y in column:
                        try:
                                d.append(float(dataset[x][y]))
                        except:
                                d.append(dataset[x][y])
                d.append(dataset[x][-1])

                if x < trainingSize:
                        trainingSet.append(d)
                        tr = dataset[x]
                else:
                        testSet.append(d)
                        te = dataset[x]
                        
        d = []
        
        for y in column:
                try:
                        d.append(float(dataset[r][y]))
                except:
                        d.append(dataset[x][y])
        d.append('')
        problemSet.append(d)

        return trainingSet, testSet, problemSet


def analyse(trainingSet, testSet):

        resultSet= []

        k = 5
        testSize = len(testSet)
        r = len(testSet)

        for x in range(0, r):
                neighbors = getNeighbors(trainingSet, testSet[x], k)
                result = getResponse(neighbors)
                #result = testSet[x][-1]
                trainingSet.append(testSet[x])
                resultSet.append(result)
                
                
        return resultSet


        

                

