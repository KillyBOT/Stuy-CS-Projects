import sys,os
import copy

wordDict = open("dictall.txt","r")
inputFile = open("wordladder_input.txt","r")
outFile = open("wout.txt","r+")
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
    frontier = [(findDistToGoal(start,end),start,0)]
    seen = {start}
    path = {}
    current = frontier.pop(0)
    while current[1] != end:
        for newWord in findLikeWords(current[1]):
            if newWord not in seen:
                seen = seen | {newWord}
                frontier.append((findDistToGoal(newWord,end) + current[2] + 1,newWord,current[2] + 1))
                path[newWord] = current[1]
        frontier.sort()
        current = frontier.pop(0)

    current = current[1]
    returnString = current
    while current != start:
        current = path[current]
        returnString = current + "," + returnString
    returnString = start + "," + returnString
    return returnString
    
if __name__ == "__main__":

    start = "head"
    end = "tail"

    #otherPair = [["head","tail"],["five","four"],["like","flip"],["drive","sleep"]]
    pairs = []
    if len(sys.argv) > 2:
        start = str(sys.argv[1])
        end = str(sys.argv[2])
        print(astar(start,end))
    else:
        for line in inputFile.readlines():
            pairs.append(line.split("\n")[0].split(","))
        print(pairs)
        for x in range(len(pairs)):
            outFile.writelines(astar(pairs[x][0],pairs[x][1]))
            outFile.write("\n")
        outFile.read()
        wordDict.close()
        inputFile.close()
        outFile.close()
    
