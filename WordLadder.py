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
            if currentWord in wordList and currentWord != word:
                likeWords.append(currentWord)

    return likeWords

#This only works when the words are of the same length
def findDistToGoal(current, end):
    cost = len(current)
    for letter in range(len(current)):
        if current[letter] == end[letter]:
            cost -= 1

    return cost

def astar(start, end):
    frontier = [(findDistToGoal(start,end),start)]
    seen = [start]
    cost = 0
    path = {}
    current = frontier.pop(0)[1]
    while current != end:
        cost += 1
        for newWord in findLikeWords(current):
            #print(newWord)
            if newWord not in seen:
                seen.append(newWord)
                frontier.append((findDistToGoal(newWord,end) + cost,newWord))
                path[newWord] = current
        frontier.sort()
        #print(frontier)
        current = frontier.pop(0)[1]
        #print(current,frontier)
            

#print(findLikeWords("teal"))
print(findDistToGoal("tall","tail"))
print(astar("head","tail"))
    
