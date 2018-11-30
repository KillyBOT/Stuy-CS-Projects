import sys

class Board(object):
    rawData = []
    rows = 0
    columns = 0

    #False is x, true is o

    firstPlayer = False
    players = ["x","o"]

    def setEmpty(self):
        rawData = []
        for row in range(self.rows):
            for column in range(self.columns):
                rawData.append(None)

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
                if self.rawData[(row * self.rows) + column] == None:
                    retString.append(str(0))
                else:
                    retString.append(str(self.players[int(self.rawData[(row * self.rows) + column])]))

        return "".join(retString)

    def printBoard(self):
        stringToPrint = str(self)
        for row in range(self.rows):
            for column in range(self.columns):
                print(stringToPrint[(row * self.rows) + column],end=" ")
            print("")

    def checkPositionWin(self,row,column):
        toRawData = (row * self.rows) + column
        if self.rawData(toRawData) == None:
            return False
        player = self.rawData[toRawData]
        outer = len(self.rawData)
        for x in range(4):
            if toRawData + 1 < outer:
                if self.rawData[toRawData + 1] != player:
                    return False
            if toRawData + 

    def findCurrentPlayer(self):
        numOfOne = 0
        numOfTwo = 0
        for item in self.rawData:
            if item == self.firstPlayer:
                numOfOne += 1
            elif item == (not self.firstPlayer):
                numOfTwo += 1

        if numOfOne == numOfTwo:
            return self.firstPlayer
        elif numOfOne > numOfTwo:
            return not self.firstPlayer
        else:
            print("If you are getting this something weird happened")
            return None



testBoard = Board(7,9,"x")
testBoard.printBoard()
print(testBoard.findCurrentPlayer())
