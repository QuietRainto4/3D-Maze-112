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

def threeD_drawMaze(app, canvas, board, x1, y1, x2, y2):
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

# does action based on the key that is pressed
def threeD_keyPressed(app, event):
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
    # for chaning modes
    if event.key == "2":
        app.mode = "twoD"

# move the position of the player
def threeD_movePlayer(app, drow, dcol, dheight):
    currPos = app.board3D[app.pHeight3D + dheight][app.pRow3D + drow][app.pCol3D + dcol]
    if currPos == 0 or currPos == 'e':
        app.pCol3D += dcol
        app.pRow3D += drow
        app.pHeight3D += dheight

# this function is called each run
def threeD_timerFired(app):
    threeD_reachedEnd(app)
    app.boardP3D = copy.deepcopy(app.board3D)
    # print3dList(app.board)
    app.boardP3D[app.pHeight3D][app.pRow3D][app.pCol3D] = "p"

def threeD_redrawAll(app, canvas):
    # set the coordinate to what the person is in as 'p'
    zBoard = threeD_zSection(app)
    yBoard = threeD_ySection(app)
    xBoard = threeD_xSection(app)
    canvas.create_text((app.zx1 + app.zx2) / 2, app.height * 1/22,
                        text = f'z = {app.pHeight3D}')
    threeD_drawMaze(app, canvas, zBoard, app.zx1, app.zy1, 
                app.zx2, app.zy2)
    canvas.create_text((app.yx1 + app.yx2) / 2, app.height * 11/22,
                        text = f'y = {app.pRow3D}')
    threeD_drawMaze(app, canvas, yBoard, app.yx1, app.yy1, 
                app.yx2, app.yy2)
    canvas.create_text((app.xx1 + app.xx2) / 2, app.height * 11/22,
                        text = f'x = {app.pCol3D}')
    threeD_drawMaze(app, canvas, xBoard, app.xx1, app.xy1, 
                app.xx2, app.xy2)
    # return the board to original after

# checks if p in on the end by 
def threeD_reachedEnd(app):
    if (app.pHeight3D == (len(app.board3D) - 2) and
        app.pRow3D == (len(app.board3D[0]) - 2) and
        app.pCol3D == (len(app.board3D[0][0]) - 2)):
        app.finished = True
    else:
        app.finished = False
                
