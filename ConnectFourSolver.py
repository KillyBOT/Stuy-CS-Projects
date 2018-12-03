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
                    retString.append(str(self.players[int(self.rawData[row][column])]))

        return "".join(retString)

    def printBoard(self):
        stringToPrint = str(self)
        for row in range(self.rows):
            for column in range(self.columns):
                print(stringToPrint[(row*self.rows) + column],end=" ")
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
            return False

        directions = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]
        directionsCheck = [True, True, True, True, True, True, True, True]
        for out in range(4):
            for direction in range(len(directions)):
                toCheck = []
                if row + (directions[direction][0] * out) >= 0 and row + (directions[direction][0]) < len(self.rows):
                    toCheck.append(row + (directions[direction][0] * out))
                if column + (directions[direction][1] * out) >= 0 and column + (directions[direction][1] < len(self.columns)):
                    toCheck.append((directions[direction]))

                if len(toCheck) == 2:
                    



testBoard = Board(7,9,"x")
testBoard.printBoard()
print(testBoard.findCurrentPlayer())
