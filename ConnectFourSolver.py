# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 16:21:37 2018

@author: edwar
"""

import sys

class Board(object):
    rawData = []
    rows = 0
    columns = 0

    #False is x, true is o

    firstPlayer = False
    playersDict = {False:"x",True:"o"}
    players = ["x","o"]

    def setEmpty(self):
        rawData = []
        for row in range(self.rows):
            toAdd = []
            for column in range(self.columns):
                toAdd.append(None)
            rawData.append(toAdd)
        self.rawData = rawData

    def __init__(self,rows,columns,firstPlayer):
        self.rows = rows
        self.columns = columns
        if firstPlayer == "x":
            firstPlayer = False
        elif firstPlayer == "o":
            firstPlayer = True

        self.setEmpty()


    def __str__ (self):
        retString = []
        for row in range(self.rows):
            for column in range(self.columns):
                if self.rawData[row][column] == None:
                    retString.append(str(0))
                else:
                    retString.append(self.playersDict[self.rawData[row][column]])

        return "".join(retString)

    def printBoard(self):
        stringToPrint = str(self)
        for row in range(self.rows):
            for column in range(self.columns):
                #print((row*self.rows) + column)
                print(stringToPrint[(row*self.columns) + column],end=" ")
            print("")

    def findCurrentPlayer(self):
        numOfOne = 0
        numOfTwo = 0
        for row in self.rawData:
            for column in row:
                if column == self.firstPlayer:
                    numOfOne += 1
                elif column == (not self.firstPlayer):
                    numOfTwo += 1

        if numOfOne == numOfTwo:
            return self.firstPlayer
        elif numOfOne > numOfTwo:
            return not self.firstPlayer
        else:
            print("If you are getting this something weird happened")
            return None

    def checkWinPos(self, row, column):
        player = self.rawData[row][column]
        if player == None:
            return None

        directions = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]
        directionsCheck = [True, True, True, True, True, True, True, True]
        for out in range(4):
            for direction in range(len(directions)):
                toCheckRow = None
                toCheckColumn = None
                if row + (directions[direction][0] * out) >= 0 and row + (directions[direction][0] * out) < self.rows:
                    toCheckRow = row + (directions[direction][0] * out)
                if column + (directions[direction][1] * out) >= 0 and column + (directions[direction][1] * out) < self.columns:
                    toCheckColumn = column + (directions[direction][1] * out)
                                
                if toCheckRow == None or toCheckColumn == None:
                    directionsCheck[direction] = False
                elif self.rawData[toCheckRow][toCheckColumn] != player:
                    directionsCheck[direction] = False
        for item in directionsCheck:
            if item == True:
                return player
            
        return None
    
    def checkWin(self):
        for row in range(self.rows):
            for column in range(self.columns):
                win = self.checkWinPos(row, column)
                if win != None:
                    return win
        return None
        
    def play(self, column):
        player = self.findCurrentPlayer()
        if self.rawData[0][column] != None:
            return False
        for row in range(self.rows):
            if row + 1 >= self.rows:
                self.rawData[row][column] = player
                return True
            elif self.rawData[row + 1][column] != None:
                self.rawData[row][column] = player
                return True
testBoard = Board(7,9,"x")

def calculateHeuristics(board,player)

testBoard.printBoard()
print(testBoard.checkWin())