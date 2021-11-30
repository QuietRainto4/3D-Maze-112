from cmu_112_graphics import*
from MazeClass import*
from ButtonClass import*
from Show2DMaze import*
from show3DMaze import*
import time

# this page is 99% pieced together from the 2D and 3D page
# the only new function if the layer3D_includeSign function

def layer3D_redrawAll(app, canvas):
    layer3D_drawTime(app, canvas)
    # the normal layer board
    board = getBoard(app, app.board3L)
    board = layer3D_includeSign(app, board)
    # the layer board with solution
    sBoard = getBoard(app, layer3D_includeSolution(app))
    sBoard = layer3D_includeSign(app, sBoard)
    if app.enlarge3L == False:
        if app.drawSolution3L == True:
            layer3D_drawLayer(app, canvas, sBoard)
        else:
            layer3D_drawLayer(app, canvas, board)
    else:
        if app.drawSolution3L == True:
            newBoard = layer3D_partOfBoard(app, sBoard)
        else:
            newBoard = layer3D_partOfBoard(app, board)
        layer3D_drawLayer(app, canvas, newBoard)

    # if the player has reached the end, draw the end screen    
    if app.finish3L == True:
        layer3L_drawEnd(app, canvas)
    # draws the buttons
    for button in app.button3L:
        button.drawButton(app, canvas)
    # for the flickering bar
    if app.timePassed % 10 < 5 and app.input3L.type == True:
        app.input3L.drawInsersionPoint(app, canvas)
    if app.error3L == True:
        layer3D_drawError(app, canvas)

def layer3D_drawLayer(app, canvas, layer):
    width = (app.width - 2 * app.margin) / (len(layer))
    height = (app.height - 2 * app.margin) / (len(layer))
    for numRow in range(len(layer)):
        for numCol in range(len(layer[0])):
            if isinstance(layer[numRow][numCol], int):
                if layer[numRow][numCol] == 1:
                    canvas.create_rectangle(
                        app.margin + width * numCol,
                        app.margin + height * numRow,
                        app.margin + width * (numCol + 1),
                        app.margin + height * (numRow + 1),
                        fill = "black")
                else:
                    # draws the player
                    if app.enlarge3L == False:
                        if (numRow == app.pRow3L and 
                                numCol == app.pCol3L):
                            if app.player == 6:
                                canvas.create_oval(
                                    app.margin + width * numCol,
                                    app.margin + height * numRow,
                                    app.margin + width * (numCol + 1),
                                    app.margin + height * (numRow + 1),
                                    fill = "red")
                            else:
                                cx = (2 * app.margin + width *(2 * 
                                                    numCol + 1)) / 2
                                cy = (2 * app.margin + height *(2 * 
                                                    numRow + 1)) / 2
                                # 400 is the size of the image
                                size = width / 300 
                                image = app.players[app.player]
                                player = app.scaleImage(image, size)
                                canvas.create_image(cx, cy, 
                                        image=ImageTk.PhotoImage(player))
                    else:
                        if (numRow == len(layer) // 2 and 
                            numCol == len(layer[0]) // 2):
                            if app.player == 6:
                                canvas.create_oval(
                                    app.margin + width * numCol,
                                    app.margin + height * numRow,
                                    app.margin + width * (numCol + 1),
                                    app.margin + height * (numRow + 1),
                                    fill = "red")
                            else:
                                cx = (2 * app.margin + width *(2 * 
                                                    numCol + 1)) / 2
                                cy = (2 * app.margin + height *(2 * 
                                                    numRow + 1)) / 2
                                # 400 is the size of the image
                                size = width / 300 
                                image = app.players[app.player]
                                player = app.scaleImage(image, size)
                                canvas.create_image(cx, cy, 
                                        image=ImageTk.PhotoImage(player))
            else:
                if layer[numRow][numCol][0] == "e":
                    canvas.create_rectangle(
                        app.margin + width * numCol,
                        app.margin + height * numRow,
                        app.margin + width * (numCol + 1),
                        app.margin + height * (numRow + 1),
                        fill = "pink")
                elif layer[numRow][numCol][0] == "b":
                    canvas.create_rectangle(
                        app.margin + width * numCol,
                        app.margin + height * numRow,
                        app.margin + width * (numCol + 1),
                        app.margin + height * (numRow + 1),
                        fill = "light blue", outline = "light blue")
                # draws the player
                if app.enlarge3L == False:
                    if (numRow == app.pRow3L and 
                            numCol == app.pCol3L):
                        if app.player == 6:
                            canvas.create_oval(
                                app.margin + width * numCol,
                                app.margin + height * numRow,
                                app.margin + width * (numCol + 1),
                                app.margin + height * (numRow + 1),
                                fill = "red")
                        else:
                            cx = (2 * app.margin + width *(2 * 
                                                numCol + 1)) / 2
                            cy = (2 * app.margin + height *(2 * 
                                                numRow + 1)) / 2
                            # 400 is the size of the image
                            size = width / 300 
                            image = app.players[app.player]
                            player = app.scaleImage(image, size)
                            canvas.create_image(cx, cy, 
                                    image=ImageTk.PhotoImage(player))
                else:
                    if (numRow == len(layer) // 2 and 
                        numCol == len(layer[0]) // 2):
                        if app.player == 6:
                            canvas.create_oval(
                                app.margin + width * numCol,
                                app.margin + height * numRow,
                                app.margin + width * (numCol + 1),
                                app.margin + height * (numRow + 1),
                                fill = "red")
                        else:
                            cx = (2 * app.margin + width *(2 * 
                                                numCol + 1)) / 2
                            cy = (2 * app.margin + height *(2 * 
                                                numRow + 1)) / 2
                            # 400 is the size of the image
                            size = width / 300 
                            image = app.players[app.player]
                            player = app.scaleImage(image, size)
                            canvas.create_image(cx, cy, 
                                    image=ImageTk.PhotoImage(player))
                # draws the sign
                cx = (2*app.margin + width * (2 * numCol + 1)) / 2
                cy = (2*app.margin + height * (2 * numRow + 1)) / 2
                if len(layer[numRow][numCol]) == 2:
                    if layer[numRow][numCol][1] == "+":
                        canvas.create_text(cx, cy,
                        text = "+", font = "Ariel 12 bold")
                    elif layer[numRow][numCol][1] == "-":
                        canvas.create_text(cx, cy,
                        text = "-", font = "Ariel 12 bold")
                    else:
                        canvas.create_text(cx, cy,
                        text = "=", font = "Ariel 12 bold")


# includes signs to signify to go up or down
def layer3D_includeSign(app, layer):
    newLayer = copy.deepcopy(layer)
    for numRow in range(len(layer)):
        for numCol in range(len(layer[0])):
            down = False
            up = False
            if (app.board3L[app.pHeight3L][numRow][numCol] == 0):
                if (app.board3L[app.pHeight3L - 1][numRow][numCol] == 0
                    or app.board3L[app.pHeight3L - 1][numRow][numCol] == "e"):
                    down = True
                if (app.board3L[app.pHeight3L + 1][numRow][numCol] == 0
                    or app.board3L[app.pHeight3L + 1][numRow][numCol] == "e"):
                    up = True
            if down == True and up == True:
                newLayer[numRow][numCol] = str(layer[numRow][numCol]) + "x"
            elif down == True:
                newLayer[numRow][numCol] = str(layer[numRow][numCol]) + "-"
            elif up == True:
                newLayer[numRow][numCol] = str(layer[numRow][numCol]) + "+"
    return newLayer
            
              
# includes the path of solution in the board
def layer3D_includeSolution(app):
    copyBoard = copy.deepcopy(app.board3L)
    for numh in range(len(copyBoard)):
        for numRow in range(len(copyBoard)):
            for numCol in range(len(copyBoard)):
                if (numh, numRow, numCol) in app.visited3L:
                    copyBoard[numh][numRow][numCol] = "b"
    return copyBoard

def layer3D_findSolution(app):
    layer3D_solutionHelper(app, 1, 1, 1)

# helper function to return the list of solution
# modified based on the 112 notes
def layer3D_solutionHelper(app, height, row, col):
    if (height, row, col) in app.visited3L:
        return False
    if (height == len(app.board3L) - 2 and row == len(app.board3L) - 2 
                                and col == len(app.board3L) - 2):
        return True
    app.visited3L.add((height, row, col))
    for dheight, drow, dcol in [(1, 0, 0), (0, 1, 0), (0, -1, 0), 
                                (-1, 0, 0), (0, 0, 1), (0, 0, -1)]:
        # if the next position is a path (0) on the board
        if (app.board3L[height + dheight][row + drow][col + dcol] == 0 or 
            app.board3L[height + dheight][row + drow][col + dcol] == 'e'):
            if (layer3D_solutionHelper(app, height + dheight, 
                                row + drow, col + dcol) == True):
                return True
            # backtrack if there is not solution in this path
    app.visited3L.remove((height, row, col))
    return None

# returns the size * size surrounding of the board, keeping the player 
#                           in the center at all times
# if it is out of the board, it is represented by a 0
def layer3D_partOfBoard(app, board):
    newBoard = []
    for i in range(app.size):
        newBoard.append([0] * app.size)
    i = 0
    for row in range(app.pRow3L - app.size//2, 
                    app.pRow3L + app.size//2 + 1):
        j = 0
        for col in range(app.pCol3L - app.size//2, 
                    app.pCol3L + app.size//2 + 1):
            if (row >= 0 and row < len(board) and 
                col >= 0 and col < len(board)):
                newBoard[i][j] = board[row][col]
            j += 1
        i += 1
    return newBoard

def getBoard(app, board):
    return board[app.pHeight3L]

def layer3D_generateMaze(app):
    app.generateMazeButton3L.pressed = False
    if len(app.input3L.text) == 0:
        app.testMaze3L = threeDMaze(app.prevSize3L, 
                                    app.prevSize3L, app.prevSize3L, 100)
    elif int(app.input3L.text) >= 35 or int(app.input3L.text) <= 1:
        app.error3L = True
        return
    else:
        app.testMaze3L = threeDMaze(int(app.input3L.text), 
                    int(app.input3L.text), int(app.input3L.text), 100)
        app.prevSize3L = int(app.input3L.text)
    app.input3L.text = ""
    app.testMaze3L.generate3DMaze()
    app.board3L = app.testMaze3L.board
    # setting the finishing position
    app.board3L[len(app.board3L)-2][len(app.board3L[0])-2][len(
                                            app.board3L[0][0])-2] = 'e'
    # the board with player
    app.boardP3L = copy.deepcopy(app.board3L)
    app.pCol3L = 1
    app.pRow3L = 1
    app.pHeight3L = 1 
    app.finish3L = False
    app.visited3L = set()
    app.drawSolution3L = False
    layer3D_findSolution(app)
    app.error3L = False
    app.prevSize3L = 5
    app.startTime3L = time.time()
    app.currTime3L = 0
    app.moveTime3L = False

def layer3D_reset(app):
    app.testMaze3L = threeDMaze(app.prevSize3D,
                             app.prevSize3D, app.prevSize3D, 100)
    app.testMaze3L.generate3DMaze()
    app.board3L = app.testMaze3L.board
    # setting the finishing position
    app.board3L[len(app.board3L)-2][len(
                    app.board3L[0])-2][len(app.board3L[0][0])-2] = 'e'
    # the board with player
    app.boardP3L = copy.deepcopy(app.board3L)
    app.pCol3L = 1
    app.pRow3L = 1
    app.pHeight3L = 1 
    app.finish3L = False
    app.visited3L = set()
    app.drawSolution3L = False
    layer3D_findSolution(app)
    app.error3L = False
    app.prevSize3L = 5
    app.startTime3L = time.time()
    app.currTime3L = 0
    app.moveTime3L = False

# called every run
# checks if the player reached the end or not
def layer3D_timerFired(app):
    app.timePassed += 1
    layer3D_reachedEnd(app)
    # if at end, stop moving
    if app.finish3L == True:
        app.moveTime3L = False
    app.timePassed += 1
    if app.moveTime3L == False:
        app.currTime3L = app.currTime3L
    else:
        app.currTime3L = int(time.time() - app.startTime3L)
    
    # Check if the buttons are pressed
    if app.generateMazeButton3L.pressed == True:
        app.generateMazeButton3L.pressed = False
        layer3D_generateMaze(app)
    if app.input3L.pressed == True:
        app.input3L.pressed = False
        app.input3L.type = True
    if app.changePlayer.pressed == True:
        app.changePlayer.pressed = False
        twoD_playerIncrease(app)
    if app.finish3L == True:
        if app.endRetry.pressed == True:
            app.endRetry.pressed = False
            layer3D_reset(app)
        if app.endBack.pressed == True:
            app.endBack.pressed = False
            app.mode = "start"

# does action based on the key that is pressed
def layer3D_keyPressed(app, event):
    if (app.input3L.type and event.key.isdigit() 
                                and len(event.key) == 1):
        if len(app.input3L.text) >= 3:
            app.input3L.text = app.input3L.text[1:]
        app.input3L.text += event.key
    elif event.key == "Enter":
        threeD_generateMaze(app)
    elif event.key == "Backspace":
        app.input3L.text = app.input3L.text[:-1]

    # for changing modes
    elif event.key == "b":
        app.mode = "start"
    elif event.key == "r":
        layer3D_reset(app)
    elif event.key == "s":
        app.drawSolution3L = not app.drawSolution3L
    elif event.key == "f":
        app.enlarge3L = not app.enlarge3L
    elif event.key == "c":
        app.error3L = False
    elif event.key == "h":
        app.mode = "help3L"
    elif event.key == "a":
        threeD_playerIncrease(app)
    elif event.key == "minus":
        if app.size < 25:
            app.size += 2
    elif event.key == "equal":
        if app.size > 1:
            app.size -= 2

    # keys for player movement
    notMove = False
    if event.key == "Right":
        layer3D_movePlayer(app, 0, 1, 0)
    elif event.key == "Left":
        layer3D_movePlayer(app, 0, -1, 0)
    elif event.key == "Up":
        layer3D_movePlayer(app, -1, 0, 0)
    elif event.key == "Down":
        layer3D_movePlayer(app, 1, 0, 0)
    elif event.key == "z":
        layer3D_movePlayer(app, 0, 0, 1)
    elif event.key == "x":
        layer3D_movePlayer(app, 0, 0, -1)
    else:
        notMove = True
    
    # start the timer if the key pressed is up down left or right
    if notMove == False:
        if app.moveTime3L == False:
            app.moveTime3L = True
            app.startTime3L = time.time()

# move the position of the player
def layer3D_movePlayer(app, drow, dcol, dheight):
    currPos = app.board3L[app.pHeight3L + dheight][app.pRow3L 
                                + drow][app.pCol3L + dcol]
    if isinstance(currPos, int):
        if currPos == 0:
            app.pCol3L += dcol
            app.pRow3L += drow
            app.pHeight3L += dheight
    elif currPos[0] == "0" or currPos[0] == "e":
        app.pCol3L += dcol
        app.pRow3L += drow
        app.pHeight3L += dheight

# calls when the mouse if pressed
def layer3D_mousePressed(app, event):
    # depending of which button is clicked on, do a certain action
    for buttons in app.button3L:
        if buttons.inRectangle(event.x, event.y):
            buttons.pressed = True
    if app.finish3L == True:
        if app.endRetry.inRectangle(event.x, event.y):
            app.endRetry.pressed = True
        elif app.endBack.inRectangle(event.x, event.y):
            app.endBack.pressed = True

# draw time
def layer3D_drawTime(app, canvas):
    canvas.create_text(app.width * 3 / 11, app.height * 0.5 / 11,
                text = f"time: {app.currTime3L}", font = "Ariel 20")

# switch player character
def layer3D_playerIncrease(app):
    app.player += 1
    if app.player > 6:
        app.player = 0


# checks if p in on the end by 
def layer3D_reachedEnd(app):
    if (app.pHeight3L == (len(app.board3L) - 2) and
        app.pRow3L == (len(app.board3L[0]) - 2) and
        app.pCol3L == (len(app.board3L[0][0]) - 2)):
        app.finish3L = True
    else:
        app.finish3L = False

# draws an error box if the maze that is being generated is too large or small
def layer3D_drawError(app, canvas):
    canvas.create_rectangle(app.width * 3 / 11, app.height * 4 / 11,
                app.width * 8 / 11, app.height * 7 / 11, fill = "white",
                outline = "black", width = app.width / 100)
    canvas.create_text(app.width * 5.5 / 11, app.height * 5 / 11,
                text = "Error with generating maze", 
                                    font = "Ariel 16 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.5 / 11,
                text = "Please make sure the number is ", 
                                    font = "Ariel 14 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.9 / 11,
                text = "within 1 - 35", font = "Ariel 14 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 6.3 / 11,
                text = "press c to exit", font = "Ariel 14 bold")

# draws the end screen that pops up after the player had reached the end
def layer3L_drawEnd(app, canvas):
    canvas.create_rectangle(app.width * 3 / 11, app.height * 4 / 11,
                app.width * 8 / 11, app.height * 7 / 11, fill = "white",
                outline = "black", width = app.width / 100)
    canvas.create_text(app.width * 5.5 / 11, app.height * 4.75 / 11,
                text = "Congradulations", font = "Ariel 24 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.25 / 11,
                text = f"time: {app.currTime3L}", font = "Ariel 16 bold")
    app.endRetry.drawButton(app, canvas)
    app.endBack.drawButton(app, canvas)

# draws an error box if the maze that is being generated is too large or small
def layer3L_drawError(app, canvas):
    canvas.create_rectangle(app.width * 3 / 11, app.height * 4 / 11,
                app.width * 8 / 11, app.height * 7 / 11, fill = "white",
                outline = "black", width = app.width / 100)
    canvas.create_text(app.width * 5.5 / 11, app.height * 5 / 11,
                text = "Error with generating maze", font = "Ariel 16 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.5 / 11,
                text = "Please make sure the number is ", font = "Ariel 14 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.9 / 11,
                text = "within 1 - 35", font = "Ariel 14 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 6.3 / 11,
                text = "press c to exit", font = "Ariel 14 bold")