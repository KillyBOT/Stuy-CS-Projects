import math

def buildSieve (length):
    retList = []
    for x in range(length):
        retList.append(((x+1)*2)+1)
    return retList

def findFirstUnparsed(lst):
    
    for x in range(len(lst)):
        if lst[x] != 0:
            return x
    return -1

def sieveList(lst, n, start):
    place = start
    while place < len(lst):
        #print(len(lst))
        lst[place] = 0
        place += n
    #return nLst

def factorial(n):
    def factRec(total, num):
        if num <= 0:
            return total
        else:
            return factRec(total*num, num-1)
    return factRec(n,n-1)

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
    sieve = buildSieve(binarySearch(n))
    while currentPrimePlace < n:
        currentPrime = sieve[findFirstUnparsed(sieve)]
        sieveList(sieve,sieve[findFirstUnparsed(sieve)],findFirstUnparsed(sieve))
        currentPrimePlace += 1
    return currentPrime

print(findNthPrime(1))
#testSieve = buildSieve(20)
#print(testSieve)
#print (sieveList(testSieve,3)) 
#print(testSieve)
#print(binarySearch(10000))
