import sys
from math import exp
import random

#Sigmoid function

def sigmoid(x):
    return 1 / (1 + exp(-x))

#This is just for making random test cases, at least for xor

def makeXORTestcase(size):
    firstInput = []
    secondInput = []
    output = []

    for place in range(size):
        firstToAdd = random.randint(0,1)
        secondToAdd = random.randint(0,1)
        outputToAdd = 0
        if firstToAdd != secondToAdd:
            outputToAdd = 1

        firstInput.append(firstToAdd)
        secondInput.append(secondToAdd)
        output.append(outputToAdd)

    firstInput.extend(secondInput)
    return (firstInput,output)

#This class represents the neurons in the network. It's mainly for organization.

class Neuron(object):

    def __init__(self):
        self.value = 0

#This is a class that represents a layer. Again, it's mainly for organization. It contains neurons, and a bias node. Note that links are not included
#The layer num is which layer it is, and the size is how many neurons are in the layer

class Layer(object):

    def __init__(self, layerNum, size):
        self.layerNum = layerNum
        self.size = size
        self.neurons = []
        self.bias = random.uniform(-5,5)

        for pos in range(self.size):
            self.neurons.append(Neuron())

    def clear(self):
        for pos in range(self.size):
            self.neurons[pos].value = 0


#This is the actual neural net class, and is what does the propagation

class NeuralNet(object):

    def __init__(self, layerData, learningRate, epochSize, batchesPerEpoch):
        self.layers = []
        self.links = []
        self.learningRate = learningRate
        self.epochSize = epochSize
        self.batchesPerEpoch = batchesPerEpoch

        for layer in range(len(layerData)):
            self.layers.append(Layer(layer,layerData[layer]))

        for layer in range(len(self.layers)-1):
            layerToAdd = []
            for startPos in range(self.layers[layer].size):
                startPosToAdd = []
                for endPos in range(self.layers[layer+1].size):
                    #This is where the value of the links is initially set
                    #You should be able to access the links in the list by doing:
                    # [starting neuron layer][starting neuron position][ending neuron position]
                    startPosToAdd.append(random.uniform(-5,5))
                layerToAdd.append(startPosToAdd)
            self.links.append(layerToAdd)

    #This function sets the values of the starting neurons for propagation

    def setStartingNeurons(self, startingNeuronsData):
        #You can edit this later to transalte any sort of input data into data for the starting neurons.
        #For now, I'm doing an xor function, so the data is just a list of 1s and 0s, with 2 bytes put together (i.e. [0,1,1,1,0,1,0,1,1,0,1,0,1,1,0,0])

        if len(startingNeuronsData) != len(self.layers[0].neurons):
            print("The input data and the neurons in the first layer must have the same size")
            return False

        for dataPos in range(len(startingNeuronsData)):
            for pos in range(len(self.layers[0].neurons)):
                self.layers[0].neurons[pos].value = startingNeuronsData[dataPos]
        return True

    #This function gets the cost of the neural network, based on how close the output neurons are to the desired output
    #For now, the desired output is simply a list of eight ones or zeroes, since I'm testing the network with an XOR function
    #The code below should be altered if you plan on doing something different

    def computeCost(self, desiredOutput):

        #This is just to make sure that something weird doesn't happen

        finalLayerNeurons = len(self.layers[len(self.layers)-1].neurons)

        if len(desiredOutput) != finalLayerNeurons:
            print("The output data and the neurons in the last layer must have the same size")
            return False

        returnVal = 0

        for outputNeuron in range(finalLayerNeurons):

            #The way I am computing the cost is doing (expectedValue - currentValue) ^ 2
            #This can be changed, but keep in mind the backpropagation algorithm also needs to be changed

            returnVal += pow((desiredOutput[outputNeuron] - self.layers[len(self.layers)-1].neurons[outputNeuron].value ),2)

        return returnVal

    #This function does all the actual propagation for one test case. The training data is a tuple that looks like: (input data, desired output data)
    def propagation(self, inputData):

        for layer in range(len(self.layers)):
            self.layers[layer].clear()

        if self.setStartingNeurons(inputData) == False:
            return False

        for layer in range(1,len(self.layers)):
            for neuron in range(len(self.layers[layer].neurons)):

                #Here's where we do the propagation

                neuronVal = 0
                neuronVal += self.layers[layer].bias

                #We are adding the bias to the final value

                for startingNeuron in range(len(self.layers[layer-1].neurons)):

                    neuronVal += self.layers[layer-1].neurons[startingNeuron].value * self.links[layer-1][startingNeuron][neuron]
                    #Now, we sum the values of the neurons in the previous layer times their respective weight

                #Finally, set the value of the neuron to the number computed above going through the sigmoid function
                self.layers[layer].neurons[neuron].value = sigmoid(neuronVal)


    #These are the backpropagation functions, the heart of the neural net.
    #I can't explain it in a comment, so go look at this video for some help:
    #https://www.youtube.com/watch?v=Ilg3gGewQ5U&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=3

    

    def backpropagation(self, outputData):









    #This just trains for one test case. Use this if you want scholastic descent

    def trainOnce(self, trainingData):
        self.propagation(trainingData[0])
        return self.computeCost(trainingData[1])

    #This will do a whole bunch of training, giving you the average cost in the end
    #Keep in mind that this doesn't use batches, and is here just for fun

    def trainEpoch(self,trainingData):
        finalVal = 0

        if len(trainingData) != self.epochSize:
            print("The amount of training data must be at least as big as the size of the epoch")

        for iteration in range(self.epochSize):

            finalVal += self.trainOnce(trainingData[iteration])

        return finalVal / self.epochSize

    #Once you have trained your neural net, this will be the function that will tell you your answer
    #Of course, you should change this so that it returns a value that suits you.
    #I'm using an XOR function, so I will just be returning a list of eight ones or zeroes given two lists of either ones or zeroes

    def computeAnswer(self, inputData):
        self.propagation(inputData)

        #Here's the stuff you want to change
        retList = []
        for neuron in self.layers[len(self.layers)-1].neurons:
            retList.append(round(neuron.value))

        return retList

    #Returns the amount that the network got right over the total amount of training data
    def getAccuracy(self, trainingData):

        timesRight = 0
        for case in range(self.epochSize):
            if trainingData[case][1] == self.computeAnswer(trainingData[case][0]):
                timesRight += 1

        return timesRight / self.epochSize


if __name__ == "__main__":

    outputSize = 4
    lengthOfEpoch = 100
    batchesPerEpoch = 10
    learningRate = 0.5

    testNet = NeuralNet([outputSize * 2,outputSize,outputSize], learningRate, lengthOfEpoch, batchesPerEpoch)

    testingTestCases = []
    for case in range(testNet.epochSize):
        testingTestCases.append(makeXORTestcase(outputSize))

    print(testNet.getAccuracy(testingTestCases))