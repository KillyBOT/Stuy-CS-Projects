import sys, math
from EratSieve import findNthPrime

def findPrimeFactors(n):
    factors = []
    currentNum = n
    currentPrime = 1
    currentNthPrime = findNthPrime(currentPrime)

    while currentNum != 1:
        if currentNum % currentNthPrime == 0:
            factors.append(currentNthPrime)
            currentNum /= currentNthPrime
        else:
            currentPrime += 1
            currentNthPrime = findNthPrime(currentPrime)

    return factors

def findFactors(n):
    smallFactors = []
    largeFactors = []
    currentNum = 2

    while currentNum ** 2 < n:
        if n % currentNum == 0:
            smallFactors.append(currentNum)
            largeFactors.insert(0,int(n/currentNum))
        currentNum += 1

    smallFactors.insert(0, 1)

    return smallFactors + largeFactors

def buildNFactorSum(n):
    factorSumDict = {}
    for x in range(n):
        factorSumDict[x] = sum(findFactors(x))

    return factorSumDict

def findNthAmicable(n):
    amicableNums = []
    factorSumDict = buildNFactorSum((n*100)**2)
    for x in range(len(factorSumDict)):
        if factorSumDict[x] == factorSumDict[factorSumDict[x]]:
            amicableNums.append([factorSumDict[x],factorSumDict[factorSumDict[x]]])

    return amicableNums
print(findNthAmicable(1))
