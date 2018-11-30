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
                rawData.append[None]

    def __init__(self,rows,columns,firstPlayer):
        self.rows = rows
        self.column = columns
        if firstPlayer == "x":
            firstPlayer = False
        elif firstPlayer == "o":
            firstPlayer = True

        setEmpty()


    def __str__ (self):
        for row in range(self.rows):
            for column in range(self.columns)
