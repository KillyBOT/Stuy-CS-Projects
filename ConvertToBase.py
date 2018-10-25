import sys, os

def findUpperBound(num, base):
    currentPow = 0
    while base ** currentPow < num:
        currentPow += 1
    return currentPow

#Convert from base 10 to any base, at least up to base 16
def convertTo(num, base):
    if num == 0:
        return "0"
    digits = "0123456789abcdef"
    currentNum = num
    currentPow = findUpperBound(num,base)
    returnString = []
    while currentPow >= 0:
        currentPlace = 0
        while base ** currentPow <= currentNum:
            currentNum -= base ** currentPow
            currentPlace += 1
        returnString.append(digits[currentPlace])
        currentPow -= 1

    return "".join(returnString)

#Convert from any base to base 10, at least up to base 10
def convertFrom(num, base):
    final = 0
    splitNum = []
    for x in range(len(str(num))):
        splitNum.append(int(str(num)[x]))

    currentPow = len(splitNum)
    print(splitNum, splitNum[-currentPow])

    while currentPow > 0:
        final += splitNum[-currentPow] * (base ** (currentPow - 1))
        currentPow -= 1
        print(final)

    return final

def convertFromTo(start, startPow, endPow):
    return convertTo(convertFrom(start,startPow),endPow)

#print(findUpperBound(2,2))
if __name__ == "__main__":
    start = 112
    startPow = 5
    endPow = 2
    if len(sys.argv) >= 4:
        start = int(sys.argv[1])
        startPow = int(sys.argv[2])
        endPow = int(sys.argv[3])

    print(convertFromTo(start,startPow,endPow))

    
