import sys
from math import exp
import random

#Sigmoid function

def sig(x):
    return 1 / (1 + exp(-x))

#This class represents the links between the neurons. It's main job is backpropagation

class Link(object):

    def __init__(self, startNeuron, endNeuron):
        self.startNeuron = startNeuron
        self.endNeuron = endNeuron
        self.weight = random.uniform(-2,2)

    def getVal(self):
        return this.startNeuron.value * this.weight

#This class represents the neurons in the network. It's mainly for organization.

class Neuron(object):

    def __init__(self, layer, layerPos, isBias):
        self.value = 0
        self.enterLinks = []
        self.endLinks = []
        self.layer = layer
        self.layerPos = layerPos
        self.isBias = isBias

    def setValueManual(self, value):
        self.value = value

    def addEnterLink(self, link):
        self.enterLinks.append(link)

    def addEndLink(self, link):
        self.endLinks.append(link)

    def setValue(self):
        if self.layer != 0:
            finalVal = 0
            for link in self.enterLinks:
                finalVal = finalVal + (link.getVal())

            return sig(finalVal)
        else:
            return False

#This is the actual neural net class, and is what does the propagation

class NeuralNet(object):

    def __init__(self, layerData):
        self.neurons = []
        self.links = []
        self.layers = len(layerData)
        for layer in range(self.layers):
            toAdd = []
            for layerPos in range(layerData[layer]):
                toAdd.append(Neuron(layer, layerPos, False))

            self.neurons.append(toAdd)

        for startLayer in range(len(self.neurons)-1):
            endLayer = startLayer + 1
            for startLayerPos in range(len(self.neurons[startLayer])):
                for endLayerPos in range(len(self.neurons[endLayer])):
                    linkToAdd = Link(self.neurons[startLayer][startLayerPos],self.neurons[endLayer][endLayerPos])
                    self.neurons[startLayer][startLayerPos].addEndLink(linkToAdd)
                    self.neurons[endLayer][endLayerPos].addEnterLink(linkToAdd)
                    self.links.append(linkToAdd)


testNet = NeuralNet([16,8,8,4])
for link in testNet.links:
    print(link.weight)
