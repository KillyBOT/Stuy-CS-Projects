import sys,os
import copy

wordDict = open("dictall.txt","r")
wordList = []
    
for word in wordDict.readlines():
    wordList.append(word.split()[0])

def findLikeWords(word):
    letters = "abcdefghijklmnopqrstuvwxyz"
    wordSplit = list(word)
    likeWords = []
    for letter in range(len(wordSplit)):
        for singleLetter in letters:
            current = copy.deepcopy(wordSplit)
            current[letter] = singleLetter
            currentWord = "".join(current)
            if currentWord in wordList:
                likeWords.append(currentWord)

    return likeWords


print(findLikeWords("hand"))
#def astar(start, current, frontier, cost):
    
