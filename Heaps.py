import sys, math
from copy import deepcopy
from random import randint

class minHeap(object):
    rawData = []

    def __init__(self, listToHeapify):
        self.rawData = []
        for item in listToHeapify:
            self.addItem(item)

    def addItem(self, item):
        newRawData = deepcopy(self.rawData)
        newRawData.append(item)
        currentPlace = len(newRawData) - 1
        while currentPlace > 0:
            #print(currentPlace, math.floor(currentPlace/2), newRawData, item)
            if newRawData[currentPlace] < newRawData[math.floor(currentPlace/2)]:
                temp = newRawData[math.floor(currentPlace/2)]
                newRawData[math.floor(currentPlace/2)] = newRawData[currentPlace]
                newRawData[currentPlace] = temp
            currentPlace = math.floor(currentPlace/2)

        self.rawData = newRawData

    def fixHeap(self):
        for item in range(len(self.rawData)-1):
            if item * 2 < len(self.rawData):
                if self.rawData[item] > self.rawData[item*2]:
                    temp = self.rawData[item]
                    self.rawData[item] = self.rawData[item*2]
                    self.rawData[item*2] = temp
            if (item * 2) + 1 < len(self.rawData):
                if self.rawData[item] > self.rawData[(item*2) + 1]:
                    temp = self.rawData[item]
                    self.rawData[item] = self.rawData[(item*2) + 1]
                    self.rawData[(item*2) + 1] = temp

    def heapify(self, listToHeapify):
        newHeap = minHeap(listToHeapify)
        return newHeap

    def pop(self):

        temp = self.rawData[0]
        self.rawData[0] = self.rawData[len(self.rawData)-1]
        self.rawData[len(self.rawData) - 1] = temp

        toReturn = self.rawData.pop()
        self.fixHeap()

        return toReturn

    def __len__(self):
        return len(self.rawData)

    def __str__(self):
        return str(self.rawData)

class maxHeap(object):
    rawData = []

    def __init__(self, listToHeapify):
        self.rawData = []
        for item in listToHeapify:
            self.addItem(item)

    def addItem(self, item):
        newRawData = deepcopy(self.rawData)
        newRawData.append(item)
        currentPlace = len(newRawData) - 1
        while currentPlace > 0:
            if newRawData[currentPlace] > newRawData[math.floor(currentPlace/2)]:
                temp = newRawData[math.floor(currentPlace/2)]
                newRawData[math.floor(currentPlace/2)] = newRawData[currentPlace]
                newRawData[currentPlace] = temp
            currentPlace = math.floor(currentPlace/2)

        self.rawData = newRawData

    def fixHeap(self):
        for item in range(len(self.rawData)-1):
            if item * 2 < len(self.rawData):
                if self.rawData[item] < self.rawData[item*2]:
                    temp = self.rawData[item]
                    self.rawData[item] = self.rawData[item*2]
                    self.rawData[item*2] = temp
            if (item * 2) + 1 < len(self.rawData):
                if self.rawData[item] < self.rawData[(item*2) + 1]:
                    temp = self.rawData[item]
                    self.rawData[item] = self.rawData[(item*2) + 1]
                    self.rawData[(item*2) + 1] = temp

    def heapify(self, listToHeapify):
        newHeap = maxHeap(listToHeapify)
        return newHeap

    def pop(self):

        temp = self.rawData[0]
        self.rawData[0] = self.rawData[len(self.rawData)-1]
        self.rawData[len(self.rawData) - 1] = temp

        toReturn = self.rawData.pop()
        self.fixHeap()

        return toReturn

    def __len__(self):
        return len(self.rawData)

    def __str__(self):
        return str(self.rawData)

def simpleHeapSort(listToSort):
    retList = []
    toHeap = minHeap(listToSort)
    for x in range(len(toHeap.rawData)):
        retList.append(toHeap.pop())

    return retList

def createRandomList(min, max, size):
    retList = []
    for x in range(size):
        retList.append(randint(min,max))

    return retList

testHeapMin = minHeap([5,3,8,7,2,17,19,5,1037,-3,2])
testHeapMax = maxHeap([5,3,8,7,2,17,19,5,1037,-3,2])
#print(testHeapMin)
#print(testHeapMax)
#print(simpleHeapSort(createRandomList(0,50,50)))
