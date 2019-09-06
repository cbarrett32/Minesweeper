import math
import random

#Generic space class that covers both bomb spaces and number spaces.
class space:
    revealed = False
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
    def __str__(self):
        return 'Space(xpos: ' + str(self.xpos) + ' ypos: ' + str(self.ypos) + ' Revealed: ' + str(self.revealed) + ')'
    def showContent(self):
        pass

#Bomb Space class that inherits from space class
class bombSpace(space):
    def __str__(self):
        return "Bomb "+ space.__str__(self)
    def showContent(self):
        return 'x'

#Number Space class that inherits from space class. Also has a number affiliated with it.
class numSpace(space):
    number = 0
    def __str__(self):
        return "Number "+ space.__str__(self)
    def changeNum (self, newNum):
        self.number = newNum
    def showContent(self):
        return str(self.number)

#Global variables to represent number of rows and columns in matrix
numX=0
numY=0

#Function that creates the board
def createBoard(bSpaces, nSpaces):
    tupleArray = []
    x=1
    y=1
    #Creates a temporary Array containing (x, y) coordinates in chronological order.
    for i in range(numX*numY):
        if x<=numX:
            tupleArray.append((x, y))
            x+=1
        else:
            y+=1
            tupleArray.append((1, y))
            x=2 
    #initialize array that will become the board
    board = [None]*(numX*numY)
    counter=0
    #Creates all of the bomb spaces by taking a random tuple from the tupleArray, creating a bombSpace
    #with those coordinates, and putting it in the right order in the board Array
    while counter<bSpaces:
        temp = random.randint(0, len(tupleArray)-1)
        (x, y) = tupleArray[temp]
        #removes coordinates from Tuple Array after they are assigned
        tupleArray.pop(temp)
        b = bombSpace(x, y)
        arrayNum = (y-1)*numY+x
        board[arrayNum-1]=b
        counter+=1
    counter=0
    #Similarly creates the number spaces (which all currently have the value 0)
    while counter<nSpaces:
        #print(len(tupleArray))
        temp = random.randint(0, len(tupleArray)-1)
        (x, y) = tupleArray[temp]
        tupleArray.pop(temp)
        n = numSpace(x, y)
        arrayNum = (y-1)*numY+x
        board[arrayNum-1]=n
        counter+=1
    return board

#returns the number of the tile or an x for all revealed spaces, and a ? for unrevealed spaces
def getType(unknownSpace):
    if unknownSpace.revealed:
        if isinstance(unknownSpace, bombSpace):
            return unknownSpace.showContent()
        else:
            return unknownSpace.showContent()
    else:
        return '?'

#Counts number of adjacent bombs for each number space, and assigns itself that number. 
def numberBoard(currentBoard):
    for cSpace in currentBoard:
        if isinstance(cSpace, numSpace):
            counter=0
            x = cSpace.xpos
            y = cSpace.ypos
            i = currentBoard.index(cSpace)
            #various if/else statements to take care of tiles on the edge. Commented numbers represent
            #which tiles to look at with this specification:
            # 1  2  3
            # 4  c  5
            # 6  7  8
            #index i -> [i-numX-1, i-numX, i-numX+1, i-1, i+1, i+numX-1, i+numX, i+numX+1]
            if x>1 and x<numX:
                if y>1 and y<numY:
                    #all 8
                    neighbors = [i-numX-1, i-numX, i-numX+1, i-1, i+1, i+numX-1, i+numX, i+numX+1]
                elif y==1:
                    #4 5 6 7 8
                    neighbors = [i-1, i+1, i+numX-1, i+numX, i+numX+1]                  
                else:
                    #1 2 3 4 5
                    neighbors = [i-numX-1, i-numX, i-numX+1, i-1, i+1]                  
            elif x==1:
                if y>1 and y<numY:
                    #2 3 5 7 8
                    neighbors = [i-numX, i-numX+1, i+1, i+numX, i+numX+1]                   
                elif y==1:
                    #5 7 8
                    neighbors = [i+1, i+numX, i+numX+1]                  
                else:
                    #2 3 5
                    neighbors = [i-numX, i-numX+1, i+1]                   
            else:
                if y>1 and y<numY:
                    #1 2 4 6 7
                    neighbors = [i-numX-1, i-numX, i-1, i+numX-1, i+numX]                  
                elif y==1:
                    #4 6 7
                    neighbors = [i-1, i+numX-1, i+numX]                  
                else:
                    #1 2 4
                    neighbors = [i-numX-1, i-numX, i-1]
            for j in neighbors:
                if isinstance(currentBoard[j], bombSpace):
                    counter+=1                   
            cSpace.number=counter
            ##arrayNumbers
            #11 -> [10, 12, 1, 2, 3, 19, 20, 21]

#Creates the string that is the board
def printBoard(board):
    counter=0
    #to guarantee we start in the else case
    x=numX+1
    y=0
    printedBoard = ""
    j=0
    # Creates the first row of indices
    while j<=numX:
        printedBoard+=str(j) + "  "
        j+=1
    for i in board:  
        if(x<=numX):
            printedBoard += getType(i) + "  "
            x+=1
        else:
            y+=1
            printedBoard += "\n" + str(y) + "  " + getType(i) + "  "
            x=2
        counter+=1
    print(printedBoard)

def revealBoard(board):
    for x in board:
        x.revealed=True
    printBoard(board)

#Reveals all neighbors of a 0 space. Recursively called if any of the neighbors are themselves 0s.
def revealNumbers(board, cSpace):
    x = cSpace.xpos
    y = cSpace.ypos
    i = board.index(cSpace)
    #Same if/else specifications as in numberBoard.
    #index i -> [i-numX-1, i-numX, i-numX+1, i-1, i+1, i+numX-1, i+numX, i+numX+1]
    if x>1 and x<numX:
        if y>1 and y<numY:
            #all 8
            neighbors = [i-numX-1, i-numX, i-numX+1, i-1, i+1, i+numX-1, i+numX, i+numX+1]
        elif y==1:
            #4 5 6 7 8
            neighbors = [i-1, i+1, i+numX-1, i+numX, i+numX+1]
        else:
            #1 2 3 4 5
            neighbors = [i-numX-1, i-numX, i-numX+1, i-1, i+1]                  
    elif x==1:
        if y>1 and y<numY:
            #2 3 5 7 8
            neighbors = [i-numX, i-numX+1, i+1, i+numX, i+numX+1]                   
        elif y==1:
            #5 7 8
            neighbors = [i+1, i+numX, i+numX+1]                 
        else:
            #2 3 5
            neighbors = [i-numX, i-numX+1, i+1]                 
    else:
        if y>1 and y<numY:
            #1 2 4 6 7
            neighbors = [i-numX-1, i-numX, i-1, i+numX-1, i+numX]                    
        elif y==1:
            #4 6 7
            neighbors = [i-1, i+numX-1, i+numX]                  
        else:
            #1 2 4
            neighbors = [i-numX-1, i-numX, i-1]
    for j in neighbors:
        if board[j].revealed==False:
            board[j].revealed=True
            if board[j].number==0:
                revealNumbers(board, board[j])

#Tests if only bomb tiles remain
def youWin(board):
    for x in board:
        if x.revealed == False and isinstance(x, numSpace):
            return False
    return True

#Core function
def playGame(board):
    gameOver = False
    while(gameOver!=True):
        x = input("Type x coordinate: ")
        y = input("Type y coordinate: ")
        #checks for legal input
        if x>0 and x<=numX and y>0 and y<=numY:
            cSpace = board[(y-1)*numY + x-1]
            cSpace.revealed = True
            #if a bomb space is typed, trigger game over.
            if(isinstance(cSpace, bombSpace)):
                gameOver=True
                revealBoard(board)
                print("You hit a bomb! Game Over")
            #if a 0 space is revealed, reveal all its neighbors
            elif cSpace.number==0:
                revealNumbers(board, cSpace)
                printBoard(board)
            #if no number spaces remain
            elif youWin(board):
                gameOver=True
                revealBoard(board)
                print("Congratulations! You win!")
            else:
                printBoard(board)
        else:
            print("Indices out of bound, please try again")

def startGame():
    global numX
    global numY
    print("Welcome to Minesweeper! Type an x and y coordinate to reveal it's space.")
    numX = 9
    numY = 9
    bSpaces = 10
    nSpaces = numX*numY-bSpaces
    #Creates the board of bombs and numbered spaces
    board = createBoard(bSpaces, nSpaces)
    #Accurately numbers the board
    numberBoard(board)
    printBoard(board)
    playGame(board)
   
startGame()

