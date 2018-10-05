import math

def buildSieve (length):
    retList = []
    retList.append([2,1])
    for x in range(length):
        retList.append([((x+1)*2)+1, 0])
    return retList

def getPrimes(lst):
    retList = []
    for x in lst:
        if x[1] == 1:
            retList.append(x[0])

    return retList

def findFirstUnparsed(lst):
    
    for x in range(len(lst)):
        if lst[x][1] == 0:
            return x
    return -1

def sieveList(lst, n, start):
    place = start
    while place < len(lst):
        if lst[place][0] % n == 0 and lst[place][0] != n:
            lst[place][1] = 2
        elif lst[place][0] == n:
            lst[place][1] = 1
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
        avgVal = math.ceil(average/math.log(average))

        if avgVal > n:
            return findNum(average,lowNum)
        elif avgVal < n:
            return findNum(highNum,average)
        else:
            return int(average)
    return findNum(findLarger(2),findLarger(2)/2)
    
def findNthPrime(n):
    sieve = buildSieve(binarySearch(n))
    while findFirstUnparsed(sieve) > 0:
        sieveList(sieve,sieve[findFirstUnparsed(sieve)][0],findFirstUnparsed(sieve))
    return getPrimes(sieve)[n]

print(findNthPrime(10000))
#testSieve = buildSieve(20)
#print(testSieve)
#print (sieveList(testSieve,3)) 
#print(testSieve)
#print(binarySearch(10000))
