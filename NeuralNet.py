import sys
from math import exp
import random

#Sigmoid function

def sig(x):
    return 1 / (1 + exp(-x))

#This class represents the links between the neurons. It's main job is backpropagation
#StartPos is k, endPos is j

#This class represents the neurons in the network. It's mainly for organization.

class Neuron(object):

    def __init__(self):
        self.value = 0

    def setValue(self, value):
        self.value = value

#This is a class that represents a layer. Again, it's mainly for organization. It contains neurons, and a bias node. Note that links are not included
#The layer num is which layer it is, and the size is how many neurons are in the layer

class Layer(object):

    def __init__(self, layerNum, size):
        self.layerNum = layerNum
        self.size = size
        self.neurons = []
        self.bias = random.uniform(-1,1)

        for pos in range(self.size):
            self.neurons.append(Neuron())


#This is the actual neural net class, and is what does the propagation

class NeuralNet(object):

    def __init__(self, layerData, learningRate, epochSize, batchesPerEpoch):
        self.layers = []
        self.links = {}
        self.learningRate = learningRate
        self.epochSize = epochSize
        self.batchesPerEpoch = batchesPerEpoch

        for layer in range(len(layerData)):
            self.layers.append(Layer(layer,layerData[layer]))

        for layer in range(len(self.layers)-1):
            for startPos in range(self.layers[layer].size):
                for endPos in range(self.layers[layer+1].size):
                    #This is where the value of the links is initially set
                    #Remember j, k, l is how I am organizing the links. J is the end position, K is the start position, and L is the start layer
                    self.links[(endPos,startPos,layer)] = random.union(-1,1)

    def setStartingNeurons(self, startingNeuronsData):
        #You can edit this later to transalte any sort of input data into data for the starting neurons.
        #For now, I'm doing an xor function, so the data is just a list of 1s and 0s, with 2 bytes put together (i.e. [0,1,1,1,0,1,0,1,1,0,1,0,1,1,0,0])

        if len(startingNeuronsData) != len(self.layers[0]):
            print("The input data is a different size than the amount of input nodes")
            return False

        for dataPos in range(len(startingNeuronsData)):
            for pos in range(len(self.layers[0])):
                self.layers[0].neurons[pos].setValue(0)
                self.layers[0].neurons[pos].setValue(startingNeuronsData[dataPos])
        return True

    def propagate(self, inputData):
        if (setStartingNeurons(inputData) == False):
            return False

        for layer in range(1,len(self.layers)):
            for neuron in range(len(layer)):
                finalVal = 0

testNet = NeuralNet([16,8,8,4], 1, 100, 10)
