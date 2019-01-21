import sys
from NeuralNet import NeuralNet
from NeuralNet import NeuralNet
from mnist import MNIST
import random
import time

#Import the MNIST database

mnistData = MNIST("MNISTSamples")
images, labels = mnistData.load_training()
testImages, testLabels = mnistData.load_testing()

#These functions are what turn the MNIST database into something readable for our neural net
def makeMNISTTestcase(index):
    retInput = []
    retOutput = []
    for pixel in range(len(images[index])):
        retInput.append(images[index][pixel]/255)
    for num in range(10):
        if num == labels[index]:
            retOutput.append(1)
        else:
            retOutput.append(0)

    return (retInput,retOutput)

def makeMNISTTestcases(epochSize):
    dataSetSize = epochSize
    if epochSize > len(images):
        dataSetSize = len(images)

    cases = []
    allNums = []

    for x in range(len(images)):
        allNums.append(x)

    for case in range(0,dataSetSize):
        cases.append(makeMNISTTestcase(random.choice(allNums)))

    random.shuffle(cases)

    return cases

def makeMNISTTest(index):
    retInput = []
    retOutput = []
    for pixel in range(len(images[index])):
        retInput.append(testImages[index][pixel]/255)
    for num in range(10):
        if num == testLabels[index]:
            retOutput.append(1)
        else:
            retOutput.append(0)

    return (retInput,retOutput)

#I also was testing out an XOR function
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


if __name__ == "__main__":

    outputSize = 10
    inputSize = 784
    lengthOfEpoch = 1000
    batchesPerEpoch = 10
    learningRate = 0.01
    neuronsPerLayer = [inputSize, 64, 32, outputSize]

    testNet = NeuralNet(neuronsPerLayer, learningRate, lengthOfEpoch, batchesPerEpoch)

    #testNet.read("MNISTNet.txt")
    print("Hello! This is a demostration of a neural net I made. Here are the commands you can write:")
    print("The commands should be written exactly as they are inside of the parentheis")
    print("\'TrainOnce\' to train the neural net for one epoch, which is " + str(lengthOfEpoch) + " training examples. Prints the amount of examples it got right")
    print("\'TrainUntil\' to train the network until a certain error rate is reached")
    print("\'TrainTimes\' to train a certain amount of times")
    print("\'TestOnce\' to test out the network\'s intelligence with a single test. Without a ton of training, expect bad results")
    print("\'TestTimes\' to test the network\'s intelligence with multiple tests. Again, make sure it\'s trained well.")
    print("\'Load\' to load a network in. Include the file\'s ending!")
    print("\'Save\' to save your network. Include the file\'s ending, which in this case should be .txt")
    print("\'Quit\' to, well, quit.")

    while(True):

        currentChoice = input("->")

        if currentChoice == "TrainOnce":
            print("Current accuracy is: " + str(testNet.scholasticDescent(makeMNISTTestcases(testNet.epochSize))*100) + "%")
            #print("Current accuracy is: " + str(testNet.scholasticDescent(makeMNISTTestcases(testNet.epochSize))*100) + "%")
        elif currentChoice == "TrainUntil":
            print("What is the network\'s minimum error rate? Write a float from 0 to 1:")
            x = input("->")
            currentError = testNet.scholasticDescent(makeMNISTTestcases(testNet.epochSize))
            while currentError < float(x):
                print("Current accuracy is: " + str(currentError))
                currentError = testNet.scholasticDescent(makeMNISTTestcases(testNet.epochSize))
        elif currentChoice == "TrainTimes":
            print("How many epochs do you want to go through?")
            x = input("->")
            startTime = time.time()
            for iteration in range(int(x)):
                #currentError = testNet.scholasticDescent(makeMNISTTestcases(testNet.epochSize))
                currentError = testNet.scholasticDescent(makeMNISTTestcases(testNet.epochSize))
                print("Current accuracy is: " + str(currentError * 100) + "%")
            
            print("Took " + str(time.time() - startTime) + " seconds.")
        elif currentChoice == "TestOnce":
            print("A random test example will be accessed. Here\'s the number:")
            testIndex = random.randint(0,len(testImages)-1)
            print(mnistData.display(testImages[testIndex]))
            print("The number is a " + str(testLabels[testIndex]))
            print("The network guessed:")
            testNet.propagate(makeMNISTTest(testIndex)[0])
            #print(testNet.getStrongestOutputNeuron(makeMNISTTest(testIndex)[0]))
            print(testNet.getStrongestOutputNeuron(makeMNISTTest(testIndex)[0]))
        elif currentChoice == "TestTimes":
            print("How many test cases do you want to go throught?")
            x = input("->")
            for times in range(int(x)):
                print("A random test example will be accessed. Here\'s the number:")
                testIndex = random.randint(0,len(testImages)-1)
                print(mnistData.display(testImages[testIndex]))
                print("The number is a " + str(testLabels[testIndex]))
                print("The network guessed:")
                testNet.propagate(makeMNISTTest(testIndex)[0])
                #print(testNet.getStrongestOutputNeuron(makeMNISTTest(testIndex)[0]))
                print(testNet.getStrongestOutputNeuron())
        elif currentChoice == "Load":
            print("What\'s the file name? Make sure it\'s in the same directory!")
            x = input("->")
            testNet.read(x)
        elif currentChoice == "Save":
            print("What\'s the file name? Make sure you add .txt to the end!")
            x = input("->")
            testNet.export(x)
        elif currentChoice == "Quit":
            break