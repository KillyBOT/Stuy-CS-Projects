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
    num = 2
    numOfAmicable = 0
    seenPair = []
    currentAmicable = 0

    while numOfAmicable < n:
        numPair = sum(findFactors(num))
        ifNumAmicable = sum(findFactors(numPair))
        #print(num)
        if num == ifNumAmicable and num not in seenPair and num != numPair:
            currentAmicable = [num,numPair]
            numOfAmicable += 1
            seenPair.append(numPair)
        num += 2

    return currentAmicable

def buildAmicablePath(mx, n):
    currentDegree = 1
    nxt = sum(findFactors(n))
    if nxt == n:
        return False
    path = [n,nxt]
    #print(n,nxt)
    while len(path) <= mx:
        nxt = sum(findFactors(nxt))
        if nxt == n:
            return path
        path.append(nxt)
        if nxt == path[-1]:
            return False
    return False

def findNthAmicableDegree(degree,sz):
    place = 2
    amicables = []
    while place <= sz:
        path = buildAmicablePath(degree, place)
        if path != False:
            amicables.append(path)
        place += 1
    return amicables
    
#print(findNthAmicableDegree(3,100000))
#print(findNthAmicable(10))

if __name__ == "__main__":
    amicable = 3
    if (len(sys.argv) > 1):
        amicable = sys.argv[1]

    print(findNthAmicable(amicable))
