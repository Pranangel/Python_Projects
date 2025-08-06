# Program Name: Tic Tac Toe.py
# Description: A board game played against a bot in terminal on a 3x4 grid.
#  A connection of 3 consecutive marks (X or O) in a vertical, diagonal, or horizontal line wins the game.
import random
import sys

def display(board):
    out = ""
    for i in range(len(board)):
        out += f"{board[i]} "
        if ((i+1)%3==0):
            print(out)
            out = ""

def selectPlayerToken():
    choice = input("X or O? ")
    while choice.upper() != "O" and choice.upper() != "X":
        choice = input("Please try again: X or O? ")
    if choice.upper() == "X":
        return("X", "O")
    else:
        return ("O", "X")

def playerGoesFirst():
    coin = random.randint(0,1)
    if (coin == 0):
        return True
    else:
        return False

def isValidSpot(spot):
    if spot == "X" or spot == "O":
        return False
    return True
    
def getPlayerChoice(board, player):
    spot = int(input("Player's turn. Pick a number you want to fill in: "))
    while (spot > 8) or (spot < 0) or (type(board[spot]) is not int):
        spot = int(input("Please choose an open spot numbered 0-8: "))
    #mark out which spot is marked on the board
    for mark in board:
        if mark == spot:
            board.remove(mark)
            board.insert(spot,player)
    return board

def evaluate(board, botToken, depth):
    if checkWinner(board, botToken) == (True, "bot"):
        return 10-depth
    if checkWinner(board, botToken) == (True, "player"):
        return -10+depth
    return 0
    
def minimax(board, depth = 10, isBotsTurn = True, botToken = "X", playerToken = "O"):
    winnerExists, winner = checkWinner(board, botToken)
    #breakpoint for when the game ends, or the depth limit is reached
    if winnerExists == True or checkTie(board) == True or depth <= 0:
        return evaluate(board, botToken, depth), -1

    eval = -(sys.maxsize-1) if isBotsTurn else sys.maxsize #bot is maximizing, player is minimizing
    
    #searching through the tree for all possible moves, adding their scores and indices to evalScores
    evalScores = []
    for i in range(len(board)):
        if isValidSpot(board[i]):
            board[i] = botToken if isBotsTurn else playerToken
            if isBotsTurn:
                nextEval, _ = minimax(board, depth-1, False, botToken, playerToken)
                eval = max(eval, nextEval)
            else:
                nextEval, _ = minimax(board, depth-1, True, botToken, playerToken)
                eval = min(eval, nextEval)
            board[i] = i

            evalScores.append((eval, i))
    
    #determining the best possible move for minimizing and maximizing player
    bestSpot = -1
    if isBotsTurn:
        bestEval = -(sys.maxsize-1)
        for score, spot in evalScores:
            if score > bestEval:
                bestEval = score
                bestSpot = spot

    if not isBotsTurn:
        bestEval = sys.maxsize
        for score, spot in evalScores:
            if score < bestEval:
                bestEval = score
                bestSpot = spot

    return bestEval, bestSpot

def getBotChoice(board, bot):
    print("Bot's turn.")
    boardCopy = [val for val in board]
    _, bestSpot = minimax(boardCopy, 10, True, bot, "X" if bot == "O" else "O")
    print(f"Bot chooses spot {bestSpot}.")
    board[bestSpot] = bot
    return board

def checkWinner(board, botToken):
    #horizontal wins
    for i in range(0,int(len(board)), 3):
        if (board[i] == board[i+1] == board[i+2]):
            return (True, "bot" if board[i] == botToken else "player")
    #vertical wins
    for i in range(0, int(len(board)/3)):
        if (board[i] == board[i+3] == board[i+6]):
            return (True, "bot" if board[i] == botToken else "player")
    #diagonal wins
    if (board[0] == board[4] == board[8]) or (board[2] == board[4] == board[6]):
        return (True, "bot" if board[4] == botToken else "player")
    return (False, None)

def checkTie(board):
    numCount = 0
    for val in board:
        if type(val) == int:
            numCount += 1
    if (numCount == 0):
        return True
    else:
        return False

def calculateWinLoss(wins, losses):
    return wins/losses if losses > 0 else wins

def getRetry():
    choice = input("Would you like to retry? (Y/N): ")
    validInput = False
    while not validInput:
        if (choice.lower() == "y") or (choice.lower() == "n"):
            validInput = True
            break
        choice = input("Please try again. Would you like to retry? (Y/N): ")
    if (choice.lower() == "y"):
        return True
    else:
        return False

board = [0,1,2,3,4,5,6,7,8]
display(board)
player, bot = selectPlayerToken()
playersTurn = playerGoesFirst()
playerWins = 0
playerLosses = 0
running = True
roundOver = False
while running:
    if roundOver:
        retry = getRetry()
        if (retry == True):
            board = [0,1,2,3,4,5,6,7,8]
            display(board)
            player, bot = selectPlayerToken()
            playersTurn = playerGoesFirst()
            roundOver = False
        else:
            print("Thanks for playing!")
            running = False
            break

    if playersTurn and not checkTie(board):
        display(board)
        board = getPlayerChoice(board, player)
        if checkWinner(board, bot) == (True, "player"):
            playerWins += 1
            display(board)
            print("You win! Your win/loss ratio is:", calculateWinLoss(playerWins, playerLosses))
            roundOver = True
        elif checkTie(board) == True:
            display(board)
            print("It's a tie!")
            roundOver = True
        print("\n---------------------------------\n")
        playersTurn = False

    elif not playersTurn and not checkTie(board):
        board = getBotChoice(board, bot)
        if checkWinner(board, bot) == (True, "bot"):
            playerLosses += 1
            display(board)
            print("You lose! Your win/loss ratio is:", calculateWinLoss(playerWins, playerLosses))
            roundOver = True
        elif checkTie(board) == True:
            display(board)
            print("It's a tie!")
            roundOver = True
        print("\n---------------------------------\n")
        playersTurn = True
