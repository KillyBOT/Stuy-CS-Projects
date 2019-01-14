import sys
from math import exp
import random
from time import sleep

#Sigmoid function

def sigmoid(x):
    return 1 / (1 + exp(-x))

#Get derivative of the sigmoid function
def dSigmoid(x):
    return (sigmoid(x) * (1 - sigmoid(x)))

#Just an average function. No literally, it finds the mean of a list
def avg(x):
    return sum(x) / float(len(x))

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

#This function makes a bunch of test cases for the xor function
def makeXORTestcases(totalSize,caseSize):
    output = []
    for case in range(totalSize):
        output.append(makeXORTestcase(caseSize))

    return output

#This class represents the neurons in the network. It's mainly for organization.

class Neuron(object):

    def __init__(self):
        self.value = 0
        self.bias = random.uniform(-0.1,0.1)

    def __str__(self):
        return str(self.value)

#This is a class that represents a layer. Again, it's mainly for organization. It contains neurons, and a bias node. Note that links are not included
#The layer num is which layer it is, and the size is how many neurons are in the layer

class Layer(object):

    def __init__(self, layerNum, size):
        self.layerNum = layerNum
        self.size = size
        self.neurons = []

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
        self.links.append(0)
        for layer in range(1,len(self.layers)):
            layerToAdd = []
            for endPos in range(self.layers[layer].size):
                endPosToAdd = []
                for startPos in range(self.layers[layer-1].size):
                    #This is where the value of the links is initially set
                    #You should be able to access the links in the list by doing:
                    # [ending neuron layer][ending neuron position][starting neuron position]
                    endPosToAdd.append(random.uniform(-0.1,0.1))
                layerToAdd.append(endPosToAdd)
            self.links.append(layerToAdd)

    #This function sets the values of the starting neurons for propagation

    def setStartingNeurons(self, startingNeuronsData):
        #You can edit this later to transalte any sort of input data into data for the starting neurons.
        #For now, I'm doing an xor function, so the data is just a list of 1s and 0s, with 2 bytes put together (i.e. [0,1,1,1,0,1,0,1,1,0,1,0,1,1,0,0])

        if len(startingNeuronsData) != len(self.layers[0].neurons):
            print("The input data and the neurons in the first layer must have the same size")
            return False

        for pos in range(len(self.layers[0].neurons)):
            self.layers[0].neurons[pos].value = startingNeuronsData[pos]
        return True

    #This gets the sum of all the weights times their respective neurons plus the bias
    #This will be squished by the sigmoid function
    def z(self, neuronPos, neuronLayer):
        if neuronLayer < 1 or neuronLayer >= len(self.layers):
            return False

        retVal = 0

        #Add the bias
        retVal += self.layers[neuronLayer].neurons[neuronPos].bias
        for neuron in range(len(self.layers[neuronLayer - 1].neurons)):

            #We add the values of the previous neurons times the weights assigned to them
            retVal += self.layers[neuronLayer-1].neurons[neuron].value * self.links[neuronLayer][neuronPos][neuron]

        #Now, sigmoid the value and return
        return retVal

    #This sets the value of a specific neuron based on the previous neurons times their respective weights
    #The neuron needs to not be an input neuron, and it needs to be inside the net

    def getNeuronVal(self, neuronPos, neuronLayer):
        return sigmoid(self.z(neuronPos, neuronLayer))

    #This is for finding the error of a specific neuron. As such, the desired output should be a single number as well
    #Change this to calculate the error differently
    #This also assumes that the neuron is in the last layer

    def getError(self, neuronPos, desiredOutput):
        if neuronPos >= len(self.layers[len(self.layers)-1].neurons):
            return False
        return pow((desiredOutput - self.layers[len(self.layers)-1].neurons[neuronPos].value),2)

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
            returnVal += self.getError(outputNeuron, desiredOutput[outputNeuron])

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
                #Now, we sum the values of the neurons in the previous layer times their respective weight

                #Finally, set the value of the neuron to the number computed above going through the sigmoid function
                self.layers[layer].neurons[neuron].value = self.getNeuronVal(neuron, layer)


    #These are the backpropagation functions, the heart of the neural net.
    #I can't explain it in a comment, so go look at this video for some help:
    #https://www.youtube.com/watch?v=Ilg3gGewQ5U&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=3

    #This function finds the error of each neuron in a specific layer
    def findLayerError(self, outputData, layerNum):
        errorList = []
        if layerNum >= len(self.layers) - 1:
            for neuron in range(len(self.layers[layerNum].neurons)):
                #The error for a specific node is the dell cost over dell neuron value times dell sigmoid over dell value

                errorList.append( (outputData[neuron] - self.layers[layerNum].neurons[neuron].value) * ((self.layers[layerNum].neurons[neuron].value) * (1 - self.layers[layerNum].neurons[neuron].value)))

        else:

            #You can recursively find the error by finding the error of the layer in front and multiplying that by the values of the links
            #The weights are multiplied by the sum of all the links going to the next layer times the error of their respective node
            errorToMultiply = self.findLayerError(outputData, layerNum + 1)
            weightMatrix = []
            for neuron in range(len(self.layers[layerNum].neurons)):
                finalToAdd = 0
                for endNeuron in range(len(self.layers[layerNum+1].neurons)):
                    finalToAdd += errorToMultiply[endNeuron]*self.links[layerNum+1][endNeuron][neuron]
                weightMatrix.append(finalToAdd)

            #Now, do the hadamard product of the new weight matrix transposed witht the
            for item in range(len(weightMatrix)):
                errorList.append(weightMatrix[item] * ((self.layers[layerNum].neurons[neuron].value) * (1 - self.layers[layerNum].neurons[neuron].value)))

        return errorList

    #This function finds the error of each neuron in the network.
    def findTotalError(self, desiredOutput):
        errorList = [0]
        for layer in range(len(self.layers)-1,0,-1):
            errorList.insert(1,self.findLayerError(desiredOutput,layer))
        return errorList

    def backpropagate(self, error):

        #First, the biases. This is actually pretty easy, since the error itself is literally the gradient.
        for layer in range(1,len(self.layers)):
            for neuron in range(len(self.layers[layer].neurons)):
                self.layers[layer].neurons[neuron].bias += error[layer][neuron] * self.learningRate

        #Next, the weights
        for layer in range(1,len(self.links)):
            for endNeuronError in range(len(self.links[layer])):
                for startNeuron in range(len(self.links[layer][endNeuronError])):
                    #The rate of change for the links is the k value times j's error
                    self.links[layer][endNeuronError][startNeuron] += (error[layer][endNeuronError] * self.layers[layer-1].neurons[startNeuron].value) * self.learningRate

    #This just trains for one test case. Use this if you want scholastic descent

    def trainOnce(self, trainingData):
        self.propagation(trainingData[0])
        self.backpropagate(self.findTotalError(trainingData[1]))

    #This will do a whole bunch of training, giving you the average cost in the end
    #Keep in mind that this doesn't use batches, and is here just for fun

    def trainEpoch(self, trainingData):
        if len(trainingData) < self.epochSize:
            print("The amount of training data must be at least as big as the size of the epoch")
        else:
            finalError = 0
            for case in range(self.epochSize):
                self.propagation(trainingData[case][0])
                finalError += self.computeCost(trainingData[case][1])
                self.backpropagate(self.findTotalError(trainingData[case][1]))

            print(finalError / self.epochSize)

    #This function trains an epoch in batches. Use this one since it's the best of both worlds
    def trainBatch(self, trainingData):
        if len(trainingData) < self.epochSize:
            print("There in not enough training data for one epoch")

        #else:
            #for batch in range(self.epochSize / self.batchesPerEpoch):


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
            anyWrong = False
            for item in range(len(trainingData[case][1])):
                if trainingData[case][1][item] != self.computeAnswer(trainingData[case][0])[item]:
                    anyWrong = True
            if anyWrong == False:
                timesRight += 1

        return timesRight / self.epochSize


if __name__ == "__main__":

    outputSize = 1
    inputSize = outputSize * 2
    lengthOfEpoch = 10000
    batchesPerEpoch = 10
    learningRate = 1
    neuronsPerLayer = [inputSize, inputSize, outputSize]

    testNet = NeuralNet(neuronsPerLayer, learningRate, lengthOfEpoch, batchesPerEpoch)

    print(testNet.getAccuracy(makeXORTestcases(testNet.epochSize,outputSize)))
    while(True):
        testNet.trainEpoch(makeXORTestcases(testNet.epochSize,outputSize))
        #print(testNet.getAccuracy(makeXORTestcases(testNet.epochSize,outputSize)))
        #sleep(0.5)