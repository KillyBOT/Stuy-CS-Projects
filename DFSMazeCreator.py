# -*- coding: utf-8 -*-
import sys, os
import random
from tkinter import *

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

pvrD = {
0:"u",
1:"r",
2:"d",
3:"l"
}

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

drawOffsets = {
"u":[0.25,0,0.75,0.75],
"d":[0.25,0.25,0.75,1],
"l":[0,0.25,0.75,0.75],
"r":[0.25,0.25,1,0.75]
}

testMaze = []
mazeSize = 32
mazeBoxSize = 16

window = Tk()
window.title("Random Maze")

cv = Canvas(window, width=mazeSize*mazeBoxSize, height=mazeSize*mazeBoxSize)
cv.pack()

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

def findUnseenRoutes(pos,maze,seen):
    place = maze[pos[0]][pos[1]]
    retList = []
    directions = list("urdl")
    for direction in directions:
        dirAddX = pos[0] + dD[direction][0]
        dirAddY = pos[1] + dD[direction][1]
        if dirAddX >= 0 and dirAddX < len(maze) and dirAddY >= 0 and dirAddY < len(maze):
            placeToCheck = maze[dirAddX][dirAddY]
            if place[pD[direction]] == False and placeToCheck[pD[prD[direction]]] == False and (dirAddX, dirAddY) not in seen:
                retList.append(direction)
    return retList

def buildMaze(maze, startPos, endPos):
    frontier = [startPos]
    seen = {tuple(startPos)}
    while len(frontier) > 0:
        currentPos = frontier[0]
        seen = seen | {tuple(currentPos)}
        if len(findUnseenRoutes(currentPos,maze,seen)) <= 0 or currentPos == endPos:
            frontier.pop(0)
            #printMaze(maze)
            #return 0
        else:
            #print(findUnseenRoutes(currentPos,maze))
            placeToGo = random.choice(findUnseenRoutes(currentPos,maze,seen))
            direction = dD[placeToGo]
            nextPos = [currentPos[0] + direction[0],currentPos[1] + direction[1]]
            print(currentPos,nextPos,pD[prD[placeToGo]])
            maze[currentPos[0]][currentPos[1]][pD[placeToGo]] = True
            maze[nextPos[0]][nextPos[1]][pD[prD[placeToGo]]] = True
            frontier.insert(0, nextPos)

def displayMaze(maze, c, start, end):
    c.create_rectangle(0,0,mazeSize*mazeBoxSize,mazeSize*mazeBoxSize,fill="#000000")
    for row in range(mazeSize):
        for column in range(mazeSize):
            for directions in range(4):
                if maze[row][column][directions] == True:
                    fillColor = "#ffffff"
                    if [row,column] == start:
                        fillColor = '#ff0000'
                    elif [row,column] == end:
                        fillColor = '#0000ff'
                    c.create_rectangle(
                    (column*mazeBoxSize)+(mazeBoxSize*drawOffsets[pvrD[directions]][0]),
                    (row*mazeBoxSize)+(mazeBoxSize*drawOffsets[pvrD[directions]][1]),
                    (column*mazeBoxSize)+(mazeBoxSize*drawOffsets[pvrD[directions]][2]),
                    (row*mazeBoxSize)+(mazeBoxSize*drawOffsets[pvrD[directions]][3]),
                    fill=fillColor,
                    width=0)

testMaze = createEmptyMaze(mazeSize)

mazeStart = [mazeSize-2,mazeSize-1]
mazeEnd = [1,0]

#printMaze(testMaze)
#print(findUnseenRoutes([0,0],testMaze))

if __name__ == "__main__":
    #if len(sys.argv) > 1:
#        mazeSize = int(sys.argv[1])
#        mazeBoxSize = mazeSize/2

    buildMaze(testMaze, mazeStart, mazeEnd)
    printMaze(testMaze)
    displayMaze(testMaze,cv, mazeStart, mazeEnd)
    window.mainloop()
