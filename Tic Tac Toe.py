# Program Name: Tic Tac Toe.py
# Description: A board game played against a bot in terminal.
#  A connection of 3 marks on a 3x3 grid wins the game.
import random

board = ["_","_","_","_","_","_","_","_","_"]
next = True
first = random.randint(0,1)

def displayBoard(board):
    out = ""
    for i in range(len(board)):
        out += board[i] + " "
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
        
#determines whether player goes second or first
if first == 0:
    next = True
if first == 1:
    next = False

displayBoard(board)
running = True
while running:
    player, bot = selectPlayerToken()
        if playerGoesFirst():
        #TODO: Ask for player input
        pass
