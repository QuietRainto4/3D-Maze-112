from cmu_112_graphics import*
from MazeClass import*
from ButtonClass import*
import copy 
import time

# from 112 notes
def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def print2dList(L):
    print(repr2dList(L))

def print3dList(L):
    for layer in L:
        print2dList(layer)

# draws the maze based on the board that it was in
def threeD_drawMaze(app, canvas, board, x1, y1, x2, y2):
    for numRow in range(len(board)):
        for numCol in range(len(board[0])):
            if isinstance(board[numRow][numCol], tuple):
                for elem in board[numRow][numCol]:
                    threeD_drawBox(app, canvas, board, elem, 
                                x1, y1, x2, y2, numRow, numCol)
            else:
                threeD_drawBox(app, canvas, board, board[numRow][numCol], 
                                x1, y1, x2, y2, numRow, numCol)

def threeD_drawBox(app, canvas, board, code, x1, y1, x2, y2, numRow, numCol):
    width = x2 - x1
    height = y2 - y1
    colWidth = width / len(board)
    rowWidth  = height / len(board)
    if code == 1:
        canvas.create_rectangle(
                x1 + colWidth * numCol,
                y1 + rowWidth * numRow,
                x1 + colWidth * (numCol + 1),
                y1 + colWidth * (numRow + 1),
                fill = "black")
    elif code == 'p':
        if app.finish3D:
            canvas.create_rectangle(
                x1 + colWidth * numCol,
                y1 + rowWidth * numRow,
                x1 + colWidth * (numCol + 1),
                y1 + colWidth * (numRow + 1),
                fill = "pink")
        canvas.create_oval(
            x1 + colWidth * numCol,
            y1 + rowWidth * numRow,
            x1 + colWidth * (numCol + 1),
            y1 + colWidth * (numRow + 1),
            fill = "red")
    elif board[numRow][numCol] == 'e':
        canvas.create_rectangle(
            x1 + colWidth * numCol,
            y1 + rowWidth * numRow,
            x1 + colWidth * (numCol + 1),
            y1 + colWidth * (numRow + 1),
            fill = "pink", outline = "pink")
    elif board[numRow][numCol] == 'ans':
        canvas.create_rectangle(
            x1 + colWidth * numCol,
            y1 + rowWidth * numRow,
            x1 + colWidth * (numCol + 1),
            y1 + colWidth * (numRow + 1),
            fill = "light blue", outline = "light blue")

# returns the horizontal cross-section of the board
def threeD_zSection(app):
    return app.boardP3D[app.pHeight3D]

# return the cross section of the board
def threeD_xSection(app):
    newBoard = []
    for layer in app.boardP3D:
        newBoard.insert(0, layer[app.pRow3D])
    return newBoard

# returns the y cross section of the board from the player's position
def threeD_ySection(app):
    newBoard = []
    for layer in app.boardP3D:
        column = []
        for row in layer:
            column.append(row[app.pCol3D])
        newBoard.insert(0, column)
    return newBoard

def threeD_mousePressed(app, event):
    # depending of which button is clicked on, do a certain action
    if app.input3D.inRectangle(event.x, event.y):
        app.input3D.type = not app.input3D.type
    elif app.generateMazeButton3D.inRectangle(event.x, event.y):
        app.generateMazeButton3D.pressed = True
    elif app.changePlayer.inRectangle(event.x, event.y):
        app.changePlayer.pressed = True

    if app.finish3D == True:
        if app.endRetry.inRectangle(event.x, event.y):
            app.endRetry.pressed = True
        elif app.endBack.inRectangle(event.x, event.y):
            app.endBack.pressed = True

# does action based on the key that is pressed
def threeD_keyPressed(app, event):
    print(event.key)
    if (app.input3D.type and event.key.isdigit() and len(event.key) == 1):
        if len(app.input3D.text) >= 3:
            app.input3D.text = app.input3D.text[1:]
        app.input3D.text += event.key
    elif event.key == "Enter":
        threeD_generateMaze(app)
    elif event.key == "Backspace":
        app.input3D.text = app.input3D.text[:-1]

    # for changing modes
    elif event.key == "b":
        app.mode = "start"
    elif event.key == "r":
        threeD_reset(app)
    elif event.key == "s":
        app.drawSolution3D = not app.drawSolution3D
    elif event.key == "c":
        app.error3D = False
    elif event.key == "h":
        app.mode = "help"
    elif event.key == "a":
        threeD_playerIncrease(app)

    # keys for player movement
    notMove = False
    if event.key == "Right":
        threeD_movePlayer(app, 0, 1, 0)
    elif event.key == "Left":
        threeD_movePlayer(app, 0, -1, 0)
    elif event.key == "Up":
        threeD_movePlayer(app, -1, 0, 0)
    elif event.key == "Down":
        threeD_movePlayer(app, 1, 0, 0)
    elif event.key == "z":
        threeD_movePlayer(app, 0, 0, 1)
    elif event.key == "x":
        threeD_movePlayer(app, 0, 0, -1)
    else:
        notMove = True
    
    # start the timer if the key pressed is up down left or right
    if notMove == False:
        if app.moveTime3D == False:
            app.moveTime3D = True
            app.startTime3D = time.time()

# resets the value and generate another maze for the player to play
def threeD_reset(app):
    # the values for the 3D maze
    app.testMaze3D = threeDMaze(app.prevSize3D, app.prevSize3D, app.prevSize3D, 100)
    app.testMaze3D.generate3DMaze()
    app.board3D = app.testMaze3D.board
    # setting the finishing position
    app.board3D[len(app.board3D)-2][len(app.board3D[0])-2][len(app.board3D[0][0])-2] = 'e'
    # the board with player
    app.boardP3D = copy.deepcopy(app.board3D)
    app.pCol3D = 1
    app.pRow3D = 1
    app.pHeight3D = 1 
    app.finish3D = False
    app.visited3D = set()
    app.drawSolution3D = False
    threeD_findSolution(app)
    app.startTime3D = time.time()
    app.currTime3D = 0
    app.moveTime3D = False

# when the generate button is pressed 
def threeD_generateMaze(app):
    app.generateMazeButton3D.pressed = False
    if int(app.input3D.text) > 35 or int(app.input3D.text) <= 1:
        app.error3D = True
        return
    if len(app.input3D.text) == 0:
            app.testMaze3D = threeDMaze(app.prevSize3D, app.prevSize3D, app.prevSize3D, 100)
    else:
        app.testMaze3D = threeDMaze(int(app.input3D.text), int(app.input3D.text),
                                         int(app.input3D.text), 100)
        app.prevSize3D = int(app.input3D.text)
    app.input3D.text = ""
    app.testMaze3D.generate3DMaze()    
    app.board3D = app.testMaze3D.board
    # setting the finishing position
    app.board3D[len(app.board3D)-2][len(app.board3D[0])-2][len(app.board3D[0][0])-2] = 'e'
    # the board with player
    app.boardP3D = copy.deepcopy(app.board3D)
    # print3dList(app.board3D)
    app.pCol3D = 1
    app.pRow3D = 1
    app.pHeight3D = 1 
    app.finish3D = False
    app.visited3D = set()
    app.drawSolution3D = False
    app.error3D = False
    threeD_findSolution(app)
    app.startTime3D = time.time()
    app.currTime3D = 0
    app.moveTime3D = False

# move the position of the player
def threeD_movePlayer(app, drow, dcol, dheight):
    currPos = app.board3D[app.pHeight3D + dheight][app.pRow3D + drow][app.pCol3D + dcol]
    if currPos == 0 or currPos == 'e':
        app.pCol3D += dcol
        app.pRow3D += drow
        app.pHeight3D += dheight

# this function is called each run
def threeD_timerFired(app):
    app.timePassed += 1
    threeD_reachedEnd(app)
    app.boardP3D = copy.deepcopy(app.board3D)
    # print3dList(app.board)
    app.boardP3D[app.pHeight3D][app.pRow3D][app.pCol3D] = "p"
    if app.drawSolution3D == True:
        threeD_includeSolution(app)
        # Check if the buttons are pressed

    if app.generateMazeButton3D.pressed == True:
        app.generateMazeButton3D.pressed = False
        threeD_generateMaze(app)
    if app.finish3D == True:
        if app.endRetry.pressed == True:
            app.endRetry.pressed = False
            print("it is pressed")
            threeD_reset(app)
        if app.endBack.pressed == True:
            app.endBack.pressed = False
            app.mode = "start"
    
    # if at end, stop moving
    if app.finish3D == True:
        app.moveTime3D = False
    app.timePassed += 1
    if app.moveTime3D == False:
        app.currTime3D = app.currTime3D
    else:
        app.currTime3D = int(time.time() - app.startTime3D)


def threeD_redrawAll(app, canvas):
    # set the coordinate to what the person is in as 'p'
    zBoard = threeD_zSection(app)
    yBoard = threeD_ySection(app)
    xBoard = threeD_xSection(app)
    canvas.create_image(app.width * 8/11, app.height * 3/11, 
                        image=ImageTk.PhotoImage(app.graph))
    canvas.create_text((app.zx1 + app.zx2) / 2, app.height * 1/22,
                        text = f'z = {app.pHeight3D}', font = "ariel 16")
    threeD_drawMaze(app, canvas, zBoard, app.zx1, app.zy1, 
                app.zx2, app.zy2)
    canvas.create_text((app.yx1 + app.yx2) / 2, app.height * 11/22,
                        text = f'y = {app.pRow3D}', font = "ariel 16")
    threeD_drawMaze(app, canvas, yBoard, app.yx1, app.yy1, 
                app.yx2, app.yy2)
    canvas.create_text((app.xx1 + app.xx2) / 2, app.height * 11/22,
                        text = f'x = {app.pCol3D}', font = "ariel 16")
    threeD_drawMaze(app, canvas, xBoard, app.xx1, app.xy1, 
                app.xx2, app.xy2)
    # draws the buttons
    for button in app.button3D:
        button.drawButton(app, canvas)
    threeD_drawTime(app, canvas)

    # return the board to original after
    if app.finish3D:
        threeD_drawEnd(app, canvas)
    app.input3D.drawButton(app, canvas)
    app.generateMazeButton3D.drawButton(app, canvas)
    if app.timePassed % 10 < 5 and app.input3D.type == True:
        app.input3D.drawInsersionPoint(app, canvas)
    if app.error3D == True:
        threeD_drawError(app, canvas)
    
    

# checks if p in on the end by 
def threeD_reachedEnd(app):
    if (app.pHeight3D == (len(app.board3D) - 2) and
        app.pRow3D == (len(app.board3D[0]) - 2) and
        app.pCol3D == (len(app.board3D[0][0]) - 2)):
        app.finish3D = True
    else:
        app.finish3D = False

# draws the end screen when the player reached to the end
def threeD_drawEnd(app, canvas):
    canvas.create_rectangle(app.width * 3 / 11, app.height * 4 / 11,
                app.width * 8 / 11, app.height * 7 / 11, fill = "white",
                outline = "black", width = app.width / 100)
    canvas.create_text(app.width * 5.5 / 11, app.height * 4.75 / 11,
                text = "Congradulations", font = "Ariel 24 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.25 / 11,
                text = f"time: {app.currTime3D}", font = "Ariel 16 bold")
    app.endRetry.drawButton(app, canvas)
    app.endBack.drawButton(app, canvas)

def threeD_findSolution(app):
    threeD_solutionHelper(app, 1, 1, 1)

# helper function to return the list of solution
# modified based on the 112 notes
def threeD_solutionHelper(app, height, row, col):
    if (height, row, col) in app.visited3D:
        return False
    if height == len(app.board3D) - 2 and row == len(app.board3D) - 2 and col == len(app.board3D) - 2:
        return True
    app.visited3D.add((height, row, col))
    for dheight, drow, dcol in [(1, 0, 0), (0, 1, 0), (0, -1, 0), 
                                (-1, 0, 0), (0, 0, 1), (0, 0, -1)]:
        # if the next position is a path (0) on the board
        if (app.board3D[height + dheight][row + drow][col + dcol] == 0 or 
            app.board3D[height + dheight][row + drow][col + dcol] == 'e'):
            if (threeD_solutionHelper(app, height + dheight, 
                                row + drow, col + dcol) == True):
                return True
            # backtrack if there is not solution in this path
    app.visited3D.remove((height, row, col))
    return None

# includes the solution to the board
def threeD_includeSolution(app):
    for (height, row, col) in app.visited3D:
        if app.boardP3D[height][row][col] == "p":
            app.boardP3D[height][row][col] = ("p", "ans")
        else:
            app.boardP3D[height][row][col] = "ans"

# draws the end screen that pops up after the player had reached the end
# draws an error box if the maze that is being generated is too large or small
def threeD_drawError(app, canvas):
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

# draw time
def threeD_drawTime(app, canvas):
    canvas.create_text(app.width * 5 / 11, app.height * 0.5 / 11,
                text = f"time: {app.currTime3D}", font = "Ariel 20")

# switch player character
def threeD_playerIncrease(app):
    app.player += 1
    if app.player > 6:
        app.player = 0