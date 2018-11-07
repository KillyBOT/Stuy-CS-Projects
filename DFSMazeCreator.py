# -*- coding: utf-8 -*-
import sys, os
import random

#Up is 1st place
#Right is 2nd place
#Down is 3rd place
#Left is 4th place
#Think NESW

pD = {
      "u":0,
      "r":1,
      "d":2,
      "l":3}

dD = {
      "u":[-1,0],
      "r":[0,1],
      "d":[1,0],
      "l":[0,-1]}
prD = {
      "u":"d",
      "d":"u",
      "l":"r",
      "r":"l"}

testMaze = []
mazeSize = 15

def createEmptyMaze(size):
    returnMaze = []
    for row in range(size):
        rowToAdd = []
        for column in range(size):
            #False means there is no wall, true means there is one
            toAdd = [False,False,False,False]
            if column == 0:
                toAdd[pD["l"]] = None
            elif column >= size-1:
                toAdd[pD["r"]] = None
                
            if row == 0:
                toAdd[pD["u"]] = None
            elif row >= size-1:
                toAdd[pD["d"]] = None
                
            rowToAdd.append(toAdd)
        returnMaze.append(rowToAdd)
        
    return returnMaze

def printMaze(maze):
    for row in maze:
        for column in row:
            for thing in column:
                toPrint = None
                if thing == None:
                    toPrint = 0
                elif thing == False:
                    toPrint = 1
                else:
                    toPrint = 2
                print(toPrint, end="")
            print(" ", end="")
        print("")

def findUnseenRoutes(pos,maze):
    place = maze[pos[0]][pos[1]]
    retList = []
    directions = list("udlr")
    for direction in directions:
        dirAddX = pos[0] + dD[direction][0]
        dirAddY = pos[1] + dD[direction][1]
        if dirAddX > 0 and dirAddX < len(maze)-1 and dirAddY > 0 and dirAddY < len(maze)-1:
            placeToCheck = maze[dirAddX][dirAddY]
            if place[pD[direction]] == False and placeToCheck[pD[prD[direction]]] == False:
                retList.append(direction)
    return retList

def buildMaze(maze, startPos, endPos):
    frontier = [startPos]
    while len(frontier) > 0:
        currentPos = frontier[0]
        if len(findUnseenRoutes(currentPos,maze)) <= 0 or currentPos == endPos:
            frontier.pop(0)
            #printMaze(maze)
        else:
            placeToGo = random.choice(findUnseenRoutes(currentPos,maze))
            direction = dD[placeToGo]
            nextPos = [currentPos[0] + direction[0],currentPos[1] + direction[1]]
            maze[currentPos[0]][currentPos[1]][pD[placeToGo]] = True
            maze[nextPos[0]][nextPos[1]][pD[prD[placeToGo]]] = True
            frontier.insert(0, nextPos)
    
testMaze = createEmptyMaze(mazeSize)

printMaze(testMaze)
#print(findUnseenRoutes([0,0],testMaze))
buildMaze(testMaze, [mazeSize-1,mazeSize-2], [0,1])
printMaze(testMaze)