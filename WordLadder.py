import sys,os
import copy

wordDict = open("dictall.txt","r")
wordList = []
    
for word in wordDict.readlines():
    wordList.append(word.split()[0])

wordList = set(wordList)

def findLikeWords(word):
    letters = "abcdefghijklmnopqrstuvwxyz"
    wordSplit = list(word)
    likeWords = []
    for letter in range(len(wordSplit)):
        for singleLetter in letters:
            current = copy.deepcopy(wordSplit)
            current[letter] = singleLetter
            currentWord = "".join(current)
            if currentWord != word:
                likeWords.append(currentWord)
    likeWords = set(likeWords)
    
    return  wordList.intersection(likeWords)

#This only works when the words are of the same length
def findDistToGoal(current, end):
    cost = len(current)
    for letter in range(len(current)):
        if current[letter] == end[letter]:
            cost -= 1

    return cost

def astar(start, end):
    frontier = [(findDistToGoal(start,end),start)]
    seen = {start}
    path = {}
    costDict = {start: 0}
    current = frontier.pop(0)[1]
    while current != end:
        for newWord in findLikeWords(current):
            if newWord not in seen:
                seen = seen | {newWord}
                costDict[newWord] = costDict[current] + 1
                frontier.append((findDistToGoal(newWord,end) + costDict[newWord],newWord))
                path[newWord] = current
        frontier.sort()
        current = frontier.pop(0)[1]

    returnPath = []
    while current != start:
        returnPath.insert(0,current)
        current = path[current]
    returnPath.insert(0,start)
    return returnPath
    
if __name__ == "__main__":

    start = "head"
    end = "tail"

    otherStart = ["head","five","like","drive"]
    otherEnd = ["tail","four","flip","sleep"]
    
    if len(sys.argv) > 2:
        start = str(sys.argv[1])
        end = str(sys.argv[2])
        print(astar(start,end))
    else:
        for x in range(len(otherStart)):
            print(astar(otherStart[x],otherEnd[x]))
    
