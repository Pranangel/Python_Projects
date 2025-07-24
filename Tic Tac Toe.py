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
    if spot != "X" or spot != "O":
        return True
    return False
    
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

#TODO: implement minmax algorithm
def minmax(board, depth, botsTurn = False, botToken = 'X'):
    #breakpoint for when the game ends, or the depth limit is reached
    if checkWinner(board) == True or checkTie(board) == True or depth <= 0:
        return 0
    
    #searching through the tree
    bestSpot = -1
    evalMax = sys.maxsize
    if botsTurn: #bot is maximizing player
        evalMax = -(sys.maxsize-1)
    for i in range(len(board)):
        if isValidSpot(board[i]):
            if botsTurn:
                board[i] = botToken
            else:
                board[i] = 'X' if botToken != 'X' else 'O'
            print(board)
            evaluation = minmax(board, depth-1, True if botsTurn else False)
            if evaluation > evalMax and botsTurn:
                evalMax = evaluation
                bestSpot = i
            if evaluation < evalMax and not botsTurn:
                evalMax = evaluation
                bestSpot = i
    return bestSpot

def getBotChoice(board, bot):
    print("Bot's turn.")
    valid_spot = False
    while not valid_spot:
        rand_spot = random.randint(0, 9)
        for val in board:
            #if there is an open spot, put it there
            if (rand_spot == val) and (isValidSpot(val)):
                board.remove(val)
                board.insert(val, bot)
                valid_spot = True
                break
    return board

def checkWinner(board):
    #horizontal wins
    for i in range(0,int(len(board)), 3):
        if (board[i] == board[i+1] == board[i+2]):
            return True
    #vertical wins
    for i in range(0, int(len(board)/3)):
        if (board[i] == board[i+3] == board[i+6]):
            return True
    #diagonal wins
    if (board[0] == board[4] == board[8]) or board[2] == board[4] == board[8]:
        return True
    return False

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
        if checkWinner(board) == True:
            playerWins += 1
            display(board)
            print("You win! Your win/loss ratio is:", calculateWinLoss(playerWins, playerLosses))
            roundOver = True
        elif checkTie(board) == True:
            print("It's a tie!")
            roundOver = True
        playersTurn = False

    elif not playersTurn and not checkTie(board):
        board = getBotChoice(board, bot)
        if checkWinner(board) == True:
            playerLosses += 1
            display(board)
            print("You lose! Your win/loss ratio is:", calculateWinLoss(playerWins, playerLosses))
            roundOver = True
        elif checkTie(board) == True:
            print("It's a tie!")
            roundOver = True
        playersTurn = True
