import sys, os

digits = "0123456789abcdefghijklmnopqrstuvwxyz"
digitsDict = {}

for digit in range(len(digits)):
    digitsDict[digits[digit]] = digit

def findUpperBound(num, base):
    currentPow = 0
    while base ** currentPow <= num:
        currentPow += 1
    return currentPow - 1

#Convert from base 10 to any base, at least up to base 36
def convertTo(num, base):
    if num == 0:
        return "0"
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

#Convert from any base to base 10, at least up to base 36
def convertFrom(num, base):
    final = 0
    splitNum = []
    for x in range(len(str(num))):
        splitNum.append(str(num)[x])

    currentPow = len(splitNum)

    while currentPow > 0:
        if digitsDict[splitNum[-currentPow]] > base:
            print("You need to make sure your base matches up with your number")
            return 0
        final += digitsDict[splitNum[-currentPow]] * (base ** (currentPow-1))
        currentPow -= 1

    return final

#I could probably do both conversions in one function, but it was easier for me to do them seperately.
#Besides, that makes it easier to read!
def convertFromTo(start, startPow, endPow):
    return convertTo(convertFrom(start,startPow),endPow)

#print(findUpperBound(2,2))
if __name__ == "__main__":
    start = "feea"
    startPow = 16
    endPow = 20
    if len(sys.argv) >= 4:
        start = str(sys.argv[1])
        startPow = int(sys.argv[2])
        endPow = int(sys.argv[3])
    if startPow > 36:
        print("Starting base too high! Using base 36")
        startPow = 36
    if endPow > 36:
        print("Ending base too high! Using base 36")
        endPow = 36

    #print(convertFrom("ff",16))
    print(convertFromTo(start,startPow,endPow))

    
