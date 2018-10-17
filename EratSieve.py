import math, sys

def buildSieve (length):
    retList = []
    for x in range(length):
        retList.append(((x+1)*2)+1)
    return retList

def findFirstUnparsed(lst, lastPrime):
    
    for x in range(lastPrime, len(lst)):
        if lst[x] != 0:
            return x
    return -1

def sieveList(lst, n, start):
    place = start
    while place < len(lst):
        lst[place] = 0
        place += n

def binarySearch(n):
    def findLarger(currentNum):
        if currentNum/math.log(currentNum) >= n:
            return currentNum
        return findLarger(currentNum*2)
    def findNum(highNum,lowNum):
        average = (highNum+lowNum)/2

        if math.log(average) == 0:
            return 3
        
        avgVal = math.ceil(average/math.log(average))
        
        if avgVal > n:
            return findNum(average,lowNum)
        elif avgVal < n:
            return findNum(highNum,average)
        else:
            return int(average)
    return findNum(findLarger(2),findLarger(2)/2)+3
    
def findNthPrime(n):

    if n < 1:
        return -1
    
    currentPrime = 2
    currentPrimePlace = 1
    lastPrimePlace = 0
    sieve = buildSieve(binarySearch(n))
    while currentPrimePlace < n:
        nextPrimePlace = findFirstUnparsed(sieve, lastPrimePlace)
        currentPrime = sieve[nextPrimePlace]
        sieveList(sieve,currentPrime,nextPrimePlace)
        lastPrimePlace = nextPrimePlace
        currentPrimePlace += 1
    return currentPrime

if __name__ == "__main__":
    prime = 10
    if (len(sys.argv)) > 1:
        prime = int(sys.argv[1])

    print(findNthPrime(prime))
#testSieve = buildSieve(20)
#print(testSieve)
#print (sieveList(testSieve,3)) 
#print(testSieve)
#print(binarySearch(10000))
