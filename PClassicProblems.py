def reverseString(inString):
    splitList = inString.split(" ")
    for w in range(len(splitList)):
        rev = ""
        for l in splitList[w]:
            rev = l + rev
        splitList[w] = rev
    ret = ""
    for w in splitList:
        ret = ret + w + " "

    return ret
    

#print(reverseString("Big boy string that is really long"))

def joinList(lst):
    retString = ""
    if(len(lst) == 0):
        return "0"
    for x in lst:
        retString = retString + str(x)

    return retString

def avg(lst):
    return sum(lst) / len(lst)

def standDev(lst):
    n = len(lst)
    lstAvg = avg(lst)
    arg1 = 1 / (n-1)
    arg2 = 0
    for x in range(n):
        arg2 += (lst[x] - lstAvg) ** 2

    return (arg1 * arg2) ** 0.5

def correlation(lst1, lst2):
    n = len(lst1)
    avg1 = avg(lst1)
    avg2 = avg(lst2)
    sd1 = standDev(lst1)
    sd2 = standDev(lst2)
    arg1 = 1 / (n - 1)
    arg2 = 0
    for x in range(n):
        arg2 += ((lst1[x] - avg1)/sd1) * ((lst2[x] - avg2)/sd2)

    return arg1 * arg2

#print(correlation([10,8,6,4],[4,3,2,1]))

def checkPhil(n):

    strDigits = str(n ** 2)
    digits = []
    for i in strDigits:
        digits.append(int(i))

    for x in digits:
        if x == 0:
            return False
    if digits[0] + int(joinList(digits[1:])) == n:
        return True
    elif int(joinList(digits[:len(digits)-2])) + digits[len(digits)-1] == n:
        return True
    return False

#print(checkPhil(14))

def cyborgDNA(dnaA, dnaB):
    sim = dnaA ^ dnaB
    currentNum = 1
    amount = 0
    while currentNum < sim:
        #print(bin(sim & currentNum))
        if sim & currentNum != 0:
            amount += 1
        currentNum *= 2

    return amount

#print(cyborgDNA(1,1))

def goldSwap(doors):

    biggestList = []
    
    for x in range(len(doors)):
        currentBiggest = 0
        for y in range(len(doors)):
            if doors[y] > currentBiggest:
                currentBiggest = doors[y]
        biggestList.append(currentBiggest)
        doors.remove(currentBiggest)
    return joinList(biggestList)

#print(goldSwap([1,2,3]))

def quickMath(exp):
    splitExp = exp
    orderOfOps = "()^*/+-"
    for x in orderOfOps:
        splitExp = splitExp.split(x)

    return splitExp

#print(quickMath("(2+3)*4"))

def maxSum(nums):
    biggest = 0

    for x in range(1,len(nums)):
        for y in range(x-1,len(nums)):
            current = nums[-x] + nums[y]
            dist = abs((len(nums)- x) - y)
            #print(y,-x,current,dist)
            if dist == 0 and nums[y] > biggest:
                #print(nums[y])
                biggest = nums[y]
            elif current > biggest and dist > 1:
                biggest = current


    return biggest

#print(maxSum([1,100,10]))

def robotLogic(instructions):
    for examine in instructions:
        for x in instructions:
            for instruction in x:
                if instruction + examine[0] == 0 and instruction + examine[1] == 0:
                    return False

    return True

print(robotLogic([[1,2],[-2,3],[3,1]]))
