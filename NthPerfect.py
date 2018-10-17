import EratSieve as es
import sys
from math import pow

def findNthPerfectNum(n):
    x = es.findNthPrime(n)
    return int(pow(2,x-1) * (pow(2,x) - 1))

if __name__ == "__main__":
    print(findNthPerfectNum(6))
