from cmu_112_graphics import*
from MazeClass import*
import copy 

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

def appStarted(app):
    app.testMaze = threeDMaze(5, 5, 5, 100)
    app.testMaze.generate3DMaze()
    app.board = app.testMaze.board
    # setting the finishing position
    app.board[len(app.board)-2][len(app.board[0])-2][len(app.board[0][0])-2] = 'e'
    # the board with player
    app.boardP = copy.deepcopy(app.board)
    print3dList(app.board)
    app.pCol = 1
    app.pRow = 1
    app.pHeight = 1 
    app.finish = False
    # the corners of the maze
    # I divided the window into 11 * 11 boxes
    app.zx1 = app.width * 1 / 11
    app.zx2 = app.width * 5 / 11
    app.zy1 = app.height * 1 / 11
    app.zy2 = app.width * 5 / 11
    app.xx1 = app.width * 1 / 11
    app.xx2 = app.width * 5 / 11
    app.xy1 = app.height * 6 / 11
    app.xy2 = app.width * 10 / 11
    app.yx1 = app.width * 6 / 11
    app.yx2 = app.width * 10 / 11
    app.yy1 = app.height * 6 / 11
    app.yy2 = app.width * 10 / 11


def drawMaze(app, canvas, board, x1, y1, x2, y2):
    width = x2 - x1
    height = y2 - y1
    colWidth = width / len(board)
    rowWidth  = height / len(board)
    for numRow in range(len(board)):
        for numCol in range(len(board[0])):
            if board[numRow][numCol] == 1:
                canvas.create_rectangle(
                    x1 + colWidth * numCol,
                    y1 + rowWidth * numRow,
                    x1 + colWidth * (numCol + 1),
                    y1 + colWidth * (numRow + 1),
                    fill = "black")
            elif board[numRow][numCol] == 'p':
                if app.finished:
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
                    fill = "pink")

def zSection(app):
    return app.boardP[app.pHeight]

# return the cross section of the board
def xSection(app):
    newBoard = []
    for layer in app.boardP:
        newBoard.insert(0, layer[app.pRow])
    return newBoard

# returns the y cross section of the board from the player's position
def ySection(app):
    newBoard = []
    for layer in app.boardP:
        column = []
        for row in layer:
            column.append(row[app.pCol])
        newBoard.insert(0, column)
    return newBoard

# does action based on the key that is pressed
def keyPressed(app, event):
    if event.key == "Right":
        movePlayer(app, 0, 1, 0)
    elif event.key == "Left":
        movePlayer(app, 0, -1, 0)
    elif event.key == "Up":
        movePlayer(app, -1, 0, 0)
    elif event.key == "Down":
        movePlayer(app, 1, 0, 0)
    elif event.key == "z":
        movePlayer(app, 0, 0, 1)
    elif event.key == "x":
        movePlayer(app, 0, 0, -1)

# move the position of the player
def movePlayer(app, drow, dcol, dheight):
    currPos = app.board[app.pHeight + dheight][app.pRow + drow][app.pCol + dcol]
    if currPos == 0 or currPos == 'e':
        app.pCol += dcol
        app.pRow += drow
        app.pHeight += dheight

# this function is called each run
def timerFired(app):
    reachedEnd(app)
    app.boardP = copy.deepcopy(app.board)
    # print3dList(app.board)
    app.boardP[app.pHeight][app.pRow][app.pCol] = "p"

def redrawAll(app, canvas):
    # set the coordinate to what the person is in as 'p'
    zBoard = zSection(app)
    yBoard = ySection(app)
    xBoard = xSection(app)
    canvas.create_text((app.zx1 + app.zx2) / 2, app.height * 1/22,
                        text = f'z = {app.pHeight}')
    drawMaze(app, canvas, zBoard, app.zx1, app.zy1, 
                app.zx2, app.zy2)
    canvas.create_text((app.yx1 + app.yx2) / 2, app.height * 11/22,
                        text = f'y = {app.pRow}')
    drawMaze(app, canvas, yBoard, app.yx1, app.yy1, 
                app.yx2, app.yy2)
    canvas.create_text((app.xx1 + app.xx2) / 2, app.height * 11/22,
                        text = f'x = {app.pCol}')
    drawMaze(app, canvas, xBoard, app.xx1, app.xy1, 
                app.xx2, app.xy2)
    # return the board to original after

# checks if p in on the end by 
def reachedEnd(app):
    if (app.pHeight == (len(app.board) - 2) and
        app.pRow == (len(app.board[0]) - 2) and
        app.pCol == (len(app.board[0][0]) - 2)):
        app.finished = True
    else:
        app.finished = False
                

runApp(width = 400, height = 400)