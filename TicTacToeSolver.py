cliques = [(0,1,2),
(3,4,5),
(6,7,8),
(0,3,6),
(1,4,7),
(2,5,8),
(0,4,8),
(2,4,6)]

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
    print(spaces)
    for player in ["x","o"]:
        for clique in cliques:
            if spaces[clique[0]] == player and spaces[clique[1]] == player and spaces[clique[2]] == player:
                return True

    return False

def findMoves(board):
    moves = []
    currentPlayer = findPlayer(board)
    spaces = board.split(",")

print(findPlayer("x,x,o,x,o,_,_,_,_"))
