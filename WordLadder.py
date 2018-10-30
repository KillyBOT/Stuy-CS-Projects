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
    path = {}
    costDict = {start: 0}
    current = frontier.pop(0)[1]
    while current != end:
        for newWord in findLikeWords(current):
            if newWord not in seen:
                seen.append(newWord)
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
    
    if len(sys.argv) > 2:
        start = str(sys.argv[1])
        end = str(sys.argv[2])

    print(astar(start,end))
