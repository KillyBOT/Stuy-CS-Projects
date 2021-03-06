import sys
from math import exp
import random
import numpy as np

#Sigmoid function

def sigmoid(x):
    return 1 / (1 + exp(-x))

#ReLu function, which may be better I dunno

def ReLu(x):
    return max([0,x])

#Leaky ReLu

def leakyReLu(x):
    return x if x > 0 else 0.01*x

#Get derivative of the sigmoid function
def dSigmoid(x):
    return (sigmoid(x) * (1 - sigmoid(x)))

def dReLu(x):
    return 1 if x > 0 else 0

#Derivative of leaky ReLu
def dLeakyReLu(x):
    return 1 if x > 0 else 0.01

#Just an average function. No literally, it finds the mean of a list
def avg(x):
    return sum(x) / float(len(x))

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

class NeuralNetOld(object):

    def __init__(self, layerData, learningRate, epochSize, batchesPerEpoch):
        self.layers = []
        self.links = []
        self.learningRate = learningRate
        self.epochSize = epochSize
        self.batchesPerEpoch = batchesPerEpoch
        self.activationType = leakyReLu
        self.dActivationType = dLeakyReLu

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

    #This prints the weights of all the links in the network
    def printLinks(self):
        for layer in range(1,len(self.links)):
            for endNeuron in range(len(self.links[layer])):
                for startNeuron in range(len(self.links[layer][endNeuron])):
                    print("Position: " + str([layer, endNeuron, startNeuron]) + "\tWeight: " + str(self.links[layer][endNeuron][startNeuron]))
    
    #This allows you to change the activation function of the network
    #It also requires that you put in a derivative function as well

    def changeActivation(newActivationType, newActivationTypeDerivative):
        self.activationType = newActivationType
        self.dActivationType = newActivationTypeDerivative


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
        return self.activationType(self.z(neuronPos, neuronLayer))

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

    #This gives you the raw values of the output neurons, which you can interpret however you want, making this more flexible

    def getAnswer(self):
        retList = []
        for neuron in self.layers[len(self.layers)-1].neurons:
            retList.append(neuron.value)

        return retList


    #These are the backpropagation functions, the heart of the neural net.
    #I can't explain it in a comment, so go look at this video for some help:
    #https://www.youtube.com/watch?v=Ilg3gGewQ5U&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=3

    #This function finds the error of each neuron in a specific layer
    def findLayerError(self, outputData, layerNum):
        errorList = []
        if layerNum >= len(self.layers) - 1:
            for neuron in range(len(self.layers[layerNum].neurons)):
                #The error for a specific node is the dell cost over dell neuron value times dell sigmoid over dell value

                errorList.append( 2 * (outputData[neuron] - self.layers[layerNum].neurons[neuron].value) * ( self.dActivationType(self.z(neuron,layerNum)) ))

            return errorList
        else:

            #You can recursively find the error by finding the error of the layer in front and multiplying that by the values of the links
            #The weights are multiplied by the sum of all the links going to the next layer times the error of their respective node
            errorToMultiply = self.findLayerError(outputData, layerNum + 1)
            weightMatrix = []
            for neuron in range(len(self.layers[layerNum].neurons)):
                finalToAdd = 0
                for endNeuron in range(len(self.layers[layerNum+1].neurons)):
                    finalToAdd += errorToMultiply[endNeuron]*self.links[layerNum+1][endNeuron][neuron]
                weightMatrix.append(finalToAdd * ( self.dActivationType(self.z(neuron,layerNum)) ))

            #Now, do the hadamard product of the new weight matrix transposed witht the
            for item in range(len(weightMatrix)):
                errorList.append( weightMatrix[item] )

            return errorList

    #This function finds the error of each neuron in a specific layer based on given outputs
    def findLayerErrorStatic(self, outputData, desiredOutput, layerNum):
        errorList = []
        if layerNum >= len(self.layers) - 1:
            for neuron in range(len(outputData)):
                #The error for a specific node is the dell cost over dell neuron value times dell sigmoid over dell value

                errorList.append( (desiredOutput[neuron] - outputData[neuron]) * ( outputData[neuron] * (1 - outputData[neuron]) ) )

            return errorList
        else:

            #You can recursively find the error by finding the error of the layer in front and multiplying that by the values of the links
            #The weights are multiplied by the sum of all the links going to the next layer times the error of their respective node
            errorToMultiply = self.findLayerErrorStatic(outputData, desiredOutput, layerNum + 1)
            weightMatrix = []
            for neuron in range(len(self.layers[layerNum].neurons)):
                finalToAdd = 0
                for endNeuron in range(len(self.layers[layerNum+1].neurons)):
                    finalToAdd += errorToMultiply[endNeuron]*self.links[layerNum+1][endNeuron][neuron]
                weightMatrix.append(finalToAdd * ( self.layers[layerNum].neurons[neuron].value * (1 - self.layers[layerNum].neurons[neuron].value) ))

            #Now, do the hadamard product of the new weight matrix transposed witht the
            for item in range(len(weightMatrix)):
                errorList.append( weightMatrix[item] )

            return errorList
        errorList = []
        if layerNum >= len(self.layers) - 1:
            for neuron in range(len(self.layers[layerNum].neurons)):
                #The error for a specific node is the dell cost over dell neuron value times dell sigmoid over dell value

                errorList.append( (outputData[neuron] - self.layers[layerNum].neurons[neuron].value) * ( self.dActivationType(self.z(neuron,layerNum)) ) )

            return errorList
        else:

            #You can recursively find the error by finding the error of the layer in front and multiplying that by the values of the links
            #The weights are multiplied by the sum of all the links going to the next layer times the error of their respective node
            errorToMultiply = self.findLayerError(outputData, layerNum + 1)
            weightMatrix = []
            for neuron in range(len(self.layers[layerNum].neurons)):
                finalToAdd = 0
                for endNeuron in range(len(self.layers[layerNum+1].neurons)):
                    finalToAdd += errorToMultiply[endNeuron]*self.links[layerNum+1][endNeuron][neuron]
                weightMatrix.append(finalToAdd * ( squishDer(self.z(neuron,layerNum)) ))

            #Now, do the hadamard product of the new weight matrix transposed witht the
            for item in range(len(weightMatrix)):
                errorList.append( weightMatrix[item] )

            return errorList

    #This function finds the error of each neuron in the network.
    def findTotalError(self, desiredOutput):
        errorList = [0]
        for layer in range(1,len(self.layers)):
            errorList.append(self.findLayerError(desiredOutput,layer))
        return errorList

    #This tells you the error based on an input, not the values of the output neurons
    def findTotalErrorStatic(self, outputData, desiredOutput):
        errorList = [0]
        for layer in range(1, len(self.layers)):
            errorList.append(self.findLayerErrorStatic(outputData,desiredOutput,layer))
        return errorList

    def backpropagate(self, error):

        #First, the biases. This is actually pretty easy, since the error itself is literally the gradient.
        for layer in range(1,len(self.layers)):
            for neuron in range(len(self.layers[layer].neurons)):
                self.layers[layer].neurons[neuron].bias += error[layer][neuron] * self.learningRate

        #Next, the weights
        for layer in range(1,len(self.layers)):
            for endNeuronError in range(len(self.layers[layer].neurons)):
                for startNeuron in range(len(self.layers[layer-1].neurons)):
                    #The rate of change for the links is the k value times j's error
                    self.links[layer][endNeuronError][startNeuron] += (error[layer][endNeuronError] * self.layers[layer-1].neurons[startNeuron].value) * self.learningRate

    #This just trains for one test case. Use this if you want scholastic descent

    def trainOnce(self, trainingData):
        self.propagation(trainingData[0])
        self.backpropagate(self.findTotalError(trainingData[1]))

    #This will do one epoch of training and adjust the weights one test case at a time
    #This will give theoretically the best descent, but it's quite slow

    def scholasticDescent(self, trainingData):
        if len(trainingData) < self.epochSize:
            print("The amount of training data must be at least as big as the size of the epoch")
        else:
            finalError = 0
            totalRight = 0
            for case in range(self.epochSize):
                self.propagation(trainingData[case][0])
                #print(trainingData[case][1],self.getAnswer())

                finalError += self.computeCost(trainingData[case][1])
                if (self.computeAnswer(trainingData[case][0]) == trainingData[case][1]):
                    totalRight += 1
                self.backpropagate(self.findTotalError(trainingData[case][1]))

            return (totalRight / self.epochSize)


    #This function trains an epoch in batches. Use this one since it's the best of both worlds
    def batchDescent(self, trainingData):
        if len(trainingData) < self.epochSize:
            print("There in not enough training data for one epoch")

        else:
            batchSize = self.epochSize // self.batchesPerEpoch
            for batch in range(self.batchesPerEpoch):
                testCases = trainingData[batch*(batchSize):((batch + 1)*(batchSize) + 1)]
                averageError = [0]
                averageErrorInt = 0
                for case in testCases:
                    self.propagation(case[0])
                    averageErrorInt += self.computeCost(case[1])
                    error = self.findTotalErrorStatic(self.getAnswer(),case[1])
                    if len(averageError) == 1:
                        averageError = error
                    else:
                        for layer in range(1,len(averageError)):
                            for neuron in range(len(averageError[layer])):
                                averageError[layer][neuron] += error[layer][neuron]

                averageErrorInt /= batchSize
                for layer in range(1,len(averageError)):
                    for neuron in range(len(averageError[layer])):
                        averageError[layer][neuron] /= batchSize

                self.backpropagate(averageError)
                print(averageErrorInt)



    #Once you have trained your neural net, this will be the function that will tell you your answer
    #Of course, you should change this so that it returns a value that suits you.
    #I'm using an XOR function, so I will just be returning a list of eight ones or zeroes given two lists of either ones or zeroes

    def computeAnswer(self, inputData):
        self.propagation(inputData)

        #Here's the stuff you want to change
        retList = []
        for neuron in self.layers[len(self.layers)-1].neurons:
            valToAppend = round(neuron.value) if neuron.value < 1 else 1
            retList.append(valToAppend)

        return retList

    #Get the strongest of the ending neurons
    def getStrongestOutputNeuron(self, inputData):
        self.propagation(inputData)
        highestPos = 0
        highestVal = 0
        for neuron in range(len(self.layers[len(self.layers)-1].neurons)):
            if self.layers[len(self.layers)-1].neurons[neuron].value > highestVal:
                highestPos = neuron
                highestVal = self.layers[len(self.layers)-1].neurons[neuron].value

        return highestPos

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


    #If you want to save your neural net's values, you can save it to a specific file that can be read

    def export(self, fileName):
        toWrite = open(fileName, "w")
        toWrite.write(str(self.learningRate)+"\n")
        toWrite.write(str(self.epochSize)+"\n")
        toWrite.write(str(self.batchesPerEpoch)+"\n")

        toWrite.write(str(len(self.layers)))
        for layerToWrite in range(len(self.layers)):
            toWrite.write("\n" + str(self.layers[layerToWrite].size))

        for linkLayer in range(1,len(self.links)):
            for endNeuron in range(len(self.links[linkLayer])):
                for startNeuron in range(len(self.links[linkLayer][endNeuron])):
                    toWrite.write("\n" + str(self.links[linkLayer][endNeuron][startNeuron]))

        toWrite.close()

    #Import saved neural nets

    def read(self, fileName):
        toRead = open(fileName, "r")

        toReadList = toRead.read().split("\n")

        currentPlace = 4

        self.learningRate = float(toReadList[0])
        self.epochSize = int(toReadList[1])
        self.batchesPerEpoch = int(toReadList[2])

        self.layers = []
        for layer in range(int(toReadList[3])):
            self.layers.append(Layer(layer,int(toReadList[currentPlace])))
            currentPlace += 1

        self.links = [0]

        for layer in range(1,len(self.layers)):
            layerToAdd = []
            for endNeuron in range(self.layers[layer].size):
                endNeuronToAdd = []
                for startNeuron in range(self.layers[layer-1].size):
                    endNeuronToAdd.append(float(toReadList[currentPlace]))
                    #print(linkLayerSize, linkEndNeuronSize, linkStartNeuronSize)

                    currentPlace += 1
                layerToAdd.append(endNeuronToAdd)
            self.links.append(layerToAdd)

        toRead.close()

#I'm working on using numpy for this neural network
#I won't comment since it has the exact same structure as above, just using different data representations

class NeuralNet(object):

    def __init__(self, layerData, learningRate, epochSize, batchesPerEpoch):
        self.learningRate = learningRate
        self.epochSize = epochSize
        self.batchesPerEpoch = batchesPerEpoch
        self.activationType = leakyReLu
        self.dActivationType = dLeakyReLu
        self.neurons = []
        self.links = [0]
        self.biases = [0]

        self.activationType = np.vectorize(self.activationType)
        self.dActivationType = np.vectorize(self.dActivationType)

        self.layerSize = len(layerData)

        for layer in range(len(layerData)):
            self.neurons.append(np.zeros((layerData[layer])))

        for layer in range(1,len(layerData)):
            self.biases.append(np.random.random((layerData[layer])) - 0.5)
            self.links.append(np.random.random((layerData[layer],layerData[layer-1])) - 0.5)

        #print(self.neurons, self.links, self.biases)


    def printLinks(self):
        print("Layers of links: " + str(len(self.links)))
        print("Link values: (end neuron layer, end neuron position, start neuron position")
        print(self.links)

    #For this, just make sure you are including a numpy array of the same size as the inputs
    def setInputNeurons(self, dataIn):

        self.neurons[0] *= 0

        if dataIn.size != self.neurons[0].size:
            print(dataIn.size, self.neurons[0].size)
            print("Error: wrong input size")

        else:
            self.neurons[0] += dataIn

    def z(self, layer):
        return (self.links[layer] @ self.neurons[layer-1]) + self.biases[layer]

    #def getNeuronVal(self, neuronLayer, neuronPos):
    #    return self.activationType(self.z(neuronLayer,neuronPos))

    #Again, make sure that your desired output is also a numpy array with the same size as the outputs
    def getCost(self, desiredOutput):
        return (np.array(desiredOutput) - self.neurons[-1]) ** 2

    def propagate(self, inputData):

        self.setInputNeurons(np.array(inputData))

        for layer in range(1,self.layerSize):
            self.neurons[layer] = self.activationType(self.z(layer))

    def getAnswersRaw(self):
        return self.neurons[-1]

    def getStrongestOutputNeuron(self):
        highestPos = 0
        highestVal = 0
        for neuron in range(self.neurons[-1].size):
            if self.neurons[-1][neuron] > highestVal:
                highestPos = neuron
                highestVal = self.neurons[-1][neuron]

        return highestPos

    def getAnswers(self):
        retList = np.zeros((self.neurons[-1].size))
        retList[self.getStrongestOutputNeuron()] = 1
        return retList

    def backpropagate(self, outputData):

        errorArray = [0]

        errorArray.append( (2 * (np.array(outputData) - self.neurons[-1])) * self.dActivationType(self.z(self.layerSize-1)) )

        for layer in range(self.layerSize-2,0,-1):
            errorArray.insert(1, (np.transpose(self.links[layer+1]) @ errorArray[1]) * self.dActivationType(self.z(layer)) )

        """print(outputData)
        print()
        print(self.getAnswers())
        print()
        print(errorArray)
        print()
        print(self.neurons)
        print()
        self.printLinks()
        print("\n")"""

        for layer in range(1,self.layerSize):
            self.biases[layer] += (errorArray[layer] * self.learningRate)
            for endNeuron in range(self.neurons[layer].size):
                self.links[layer][endNeuron] += (self.neurons[layer-1] * errorArray[layer][endNeuron]) * self.learningRate

    def trainOnce(self, data):
        self.propagate(data[0])
        self.backpropagate(data[1])

    def scholasticDescent(self, data):
        if len(data) != self.epochSize:
            print("Error: wrong data amount! Have as much data as the size of your epoch")
        else:
            totalRight = 0
            totalError = 0
            for case in data:
                self.propagate(case[0])
                if np.array_equal(self.getAnswers(),np.array(case[1])):
                    totalRight += 1
                totalError += sum(self.getCost(case[1]))
                self.backpropagate(case[1])


            return totalRight / self.epochSize

    def export(self, filename):
        toWrite = open(filename,"w")
        toWrite.write(str(self.learningRate)+"\n")
        toWrite.write(str(self.epochSize)+"\n")
        toWrite.write(str(self.batchesPerEpoch)+"\n")

        toWrite.write(str(self.layerSize))
        for layer in range(self.layerSize):
            toWrite.write("\n" + str(self.neurons[layer].size))

        for layer in range(1,self.layerSize):
            for endNeuron in range(self.neurons[layer].size):
                toWrite.write("\n" + str(self.biases[layer][endNeuron]))
                for startNeuron in range(self.neurons[layer-1].size):
                    toWrite.write("\n" + str(self.links[layer][endNeuron][startNeuron]))

        toWrite.close()

    def read(self, filename):
        toRead = open(filename, "r")
        
        toReadList = toRead.read().split("\n")

        self.learningRate = float(toReadList[0])
        self.epochSize = int(toReadList[1])
        self.batchesPerEpoch = int(toReadList[2])

        self.neurons = []
        self.links = [0]
        self.biases = [0]

        currentPlace = 4

        for layer in range(int(toReadList[3])):
            self.neurons.append(np.zeros((int(toReadList[currentPlace]))))
            currentPlace += 1

        self.layerSize = len(self.neurons)

        for layer in range(1,self.layerSize):
            self.links.append(np.zeros((self.neurons[layer].size,self.neurons[layer-1].size)))
            self.biases.append(np.zeros((self.neurons[layer].size)))

            for endNeuron in range(self.neurons[layer].size):
                self.biases[layer][endNeuron] = float(toReadList[currentPlace])
                currentPlace += 1
                for startNeuron in range(self.neurons[layer-1].size):
                    self.links[layer][endNeuron][startNeuron] = float(toReadList[currentPlace])
                    currentPlace += 1

        toRead.close()