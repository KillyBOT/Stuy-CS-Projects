# -*- coding: utf-8 -*-

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {} 

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = None
        self.parents = []
        self.children = []

    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endState)
        print ('parents:',self.parents)
        print ('children:',self.children)

def findPlayer(layout):
    numOfX = 0
    numOfO = 0
    anyEmpty = False
    for place in layout:
        if place == "_":
            anyEmpty = True
        if place == "x":
            numOfX += 1
        elif place == "o":
            numOfO += 1
    if not anyEmpty:
        return False
    elif numOfX > numOfO:
        return "o"
    elif numOfX == numOfO:
        return "x"
    

def CreateAllBoards(layout,parent):
    if layout not in AllBoards:
        AllBoards[layout] = BoardNode(layout)
        player = findPlayer(layout)
        if player != False:
            for place in range(len(layout)):
                if layout[place] == "_":
                    layoutCopy = list(layout)
                    layoutCopy[place] = player
                    print(layoutCopy)
                    AllBoards[layout].children.append("".join(layoutCopy))
                    CreateAllBoards("".join(layoutCopy),layout)
                    
    AllBoards[layout].parents.append(parent)

CreateAllBoards("_________",None)

print(len(AllBoards))