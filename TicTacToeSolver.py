# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 23:41:53 2018

@author: edwar
"""

import sys
from random import choice
from time import sleep

cliques = [(0,1,2),
(3,4,5),
(6,7,8),
(0,3,6),
(1,4,7),
(2,5,8),
(0,4,8),
(2,4,6)]

emptyBoard = "_,_,_,_,_,_,_,_,_"

def printBoard(board):
    spaces = board.split(",")
    for row in range(int(len(spaces) / 3)):
        for column in range(int(len(spaces) / 3)):
            print(spaces[(row * 3) + column] + ",", end="")
        print("")

def findPlayer(board):
    x = 0
    o = 0
    for space in board:
        if space == "x":
            x += 1
        elif space == "o":
            o += 1

    if x == o:
        return "x"
    else:
        return "o"

def checkSolved(board):
    spaces = board.split(",")

    anyEmpty = False
    for space in spaces:
        if space == "_":
            anyEmpty = True

    if not anyEmpty:
        return True

    for player in ["x","o"]:
        for clique in cliques:
            if spaces[clique[0]] == player and spaces[clique[1]] == player and spaces[clique[2]] == player:
                return True

    return False

def checkPlayerSolved(board):
    spaces = board.split(",")

    anyEmpty = False
    for space in spaces:
        if space == "_":
            anyEmpty = True

    for player in ["x","o"]:
        for clique in cliques:
            if spaces[clique[0]] == player and spaces[clique[1]] == player and spaces[clique[2]] == player:
                return player

    if not anyEmpty:
        return True

    return False

def findMoves(board):
    moves = []
    currentPlayer = findPlayer(board)
    spaces = board.split(",")
    for space in range(len(spaces)):
        if spaces[space] == "_":
            newBoard = spaces[:]
            newBoard[space] = currentPlayer
            moves.append(",".join(newBoard))

    return moves

def findPath(origins, end, start):
    path = []
    currentPoint = end
    while currentPoint != start and origins[currentPoint] != 0:
        path.insert(0,currentPoint)
        currentPoint = origins[currentPoint]

    if origins[currentPoint] != 0:
        path.insert(0,start)
        return path

def findAllPossibleMoves(startingBoard):
    frontier = [startingBoard]
    seen = set()
    origins = dict()
    origins[startingBoard] = 0
    numOfMoves = 0
    allMoves = 0
    possibleEnds = 0
    possibleXWins = 0
    possibleOWins = 0
    possibleTies = 0
    #allPaths = []
    while len(frontier) > 0:
        current = frontier.pop()[:]
        if current not in seen:
            seen = seen | {current}
            allMoves += 1
        if checkSolved(current):
            possibleEnds += 1
            #allPaths.append(findPath(origins,current,startingBoard))
            if checkPlayerSolved(current) == "x":
                possibleXWins += 1
            elif checkPlayerSolved(current) == "o":
                possibleOWins += 1
            elif checkPlayerSolved(current) == True:
                possibleTies += 1
        else:
            for move in findMoves(current):
                origins[move] = current
                frontier.append(move)
                numOfMoves += 1

    printBoard(startingBoard)
    print("All possible boards from here: " + str(allMoves))
    print("All possible games from here: " + str(possibleEnds))
    print("All possible wins for X from here: " + str(possibleXWins))
    print("All possible wins for O from here: " + str(possibleOWins))
    print("All possible ties from here: " + str(possibleTies))
    #print("All possible games from here: " + str(len(allPaths)))

    return allMoves, possibleEnds, possibleXWins, possibleOWins, possibleTies

def findOutcome(startingBoard):
    player = findPlayer(startingBoard)
    frontier = [startingBoard]
    possibleXWins = 0
    possibleOWins = 0
    possibleTies = 0
    while len(frontier) > 0:
        current = frontier.pop()[:]
        if checkSolved(current):
            if checkPlayerSolved(current) == "x":
                possibleXWins += 1
            elif checkPlayerSolved(current) == "o":
                possibleOWins += 1
            elif checkPlayerSolved(current) == True:
                possibleTies += 1
        else:
            for move in findMoves(current):
                frontier.append(move)

    if player == "x":
        return possibleXWins - possibleOWins - possibleTies
    elif player == "o":
        return possibleOWins - possibleXWins - possibleTies
    else:
        print("There was some sort of error")
        return False

def findBestMove(board):
    if checkSolved(board):
        print("Game is already done!")
        return False
    else:
        moves = findMoves(board)
        best = findOutcome(moves[0])
        bestMove = [moves[0]]
        for move in moves:
            moveOutcome = findOutcome(move)
            if moveOutcome < best:
                best = moveOutcome
                bestMove = [move]
            elif moveOutcome == best:
                bestMove.append(move)

    return choice(bestMove)


findAllPossibleMoves(emptyBoard)
currentBoard = emptyBoard[:]
while not checkSolved(currentBoard):
    currentBoard = findBestMove(currentBoard)
    printBoard(currentBoard)
    print("")
    sleep(1)

if checkPlayerSolved(currentBoard) == True:
    print("Tie!")
else:
    print(checkPlayerSolved(currentBoard) + " wins!")
