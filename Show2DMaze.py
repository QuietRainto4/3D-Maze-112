from cmu_112_graphics import*
from MazeClass import*
from ButtonClass import*
import time

# draws the maze
def twoD_drawMaze(app, canvas):
    for numRow in range(len(app.board2D)):
        for numCol in range(len(app.board2D[0])):
            if app.board2D[numRow][numCol] == 1:
                canvas.create_rectangle(
                    app.margin2D + app.colWidth2D * numCol,
                    app.margin2D + app.rowWidth2D * numRow,
                    app.margin2D + app.colWidth2D * (numCol + 1),
                    app.margin2D + app.colWidth2D * (numRow + 1),
                    fill = "black")

# draws on the canvas
def twoD_redrawAll(app, canvas):
    if app.enlarge == False:
        twoD_drawMaze(app, canvas)
        if app.drawSolution2D == True:
            twoD_drawSolutions(app, canvas)
        twoD_drawGoal(app, canvas)
        twoD_drawPlayer(app, canvas)
    else:
        
        if app.drawSolution2D == True:
            sBoard = twoD_includeSolution(app)
            newBoard = twoD_partOfBoard(app, sBoard)
        else:
            newBoard = twoD_partOfBoard(app, app.board2D)
        twoD_enlargedMaze(app, canvas, newBoard)

    if app.finish2D == True:
        twoD_drawEnd(app, canvas)
    app.input2D.drawButton(app, canvas)
    app.generateMazeButton2D.drawButton(app, canvas)
    if app.timePassed % 10 < 5 and app.input2D.type == True:
        app.input2D.drawInsersionPoint(app, canvas)
    if app.error2D == True:
        twoD_drawError(app, canvas)

def twoD_includeSolution(app):
    copyBoard = copy.deepcopy(app.board2D)
    for numRow in range(len(copyBoard)):
        for numCol in range(len(copyBoard)):
            if (numRow, numCol) in app.visited2D:
                copyBoard[numRow][numCol] = "b"
            if (numRow == len(app.board2D) - 2 and 
                numCol == len(app.board2D) - 2):
                copyBoard[numRow][numCol] = "p"
    return copyBoard
            

# draws the enlarged portion of the maze in app.enlarge == True
# for the solution board, if the point is in the set, then draw it as solution
def twoD_enlargedMaze(app, canvas, newBoard):
    width = (app.width - 2 * app.margin2D) / app.size
    height = (app.height - 2 * app.margin2D) / app.size
    for numRow in range(len(newBoard)):
        for numCol in range(len(newBoard[0])):
            if newBoard[numRow][numCol] == "p":
                canvas.create_rectangle(
                    app.margin2D + width * numCol,
                    app.margin2D + height * numRow,
                    app.margin2D + width * (numCol + 1),
                    app.margin2D + height * (numRow + 1),
                    fill = "pink")
            elif (numRow == len(newBoard) // 2 and 
                numCol == len(newBoard[0]) // 2):
                canvas.create_oval(
                    app.margin2D + width * numCol,
                    app.margin2D + height * numRow,
                    app.margin2D + width * (numCol + 1),
                    app.margin2D + height * (numRow + 1),
                    fill = "red")
            elif newBoard[numRow][numCol] == 1:
                canvas.create_rectangle(
                    app.margin2D + width * numCol,
                    app.margin2D + height * numRow,
                    app.margin2D + width * (numCol + 1),
                    app.margin2D + height * (numRow + 1),
                    fill = "black")
            elif newBoard[numRow][numCol] == "b":
                canvas.create_rectangle(
                    app.margin2D + width * numCol,
                    app.margin2D + height * numRow,
                    app.margin2D + width * (numCol + 1),
                    app.margin2D + height * (numRow + 1),
                    fill = "light blue", outline = "light blue")

# returns the 9 * 9 surrounding of the board, keeping the player in the center at all times
# if it is out of the board, it is represented by a 0
def twoD_partOfBoard(app, board):
    newBoard = []
    for i in range(app.size):
        newBoard.append([0] * app.size)
    # app.pCol2D, app.pRow2D
    i = 0
    for row in range(app.pRow2D - app.size//2, app.pRow2D + app.size//2 + 1):
        j = 0
        for col in range(app.pCol2D - app.size//2, app.pCol2D + app.size//2 + 1):
            if (row >= 0 and row < len(board) and 
                col >= 0 and col < len(board)):
                newBoard[i][j] = board[row][col]
            if (row == len(app.board2D) - 2 and 
                col == len(app.board2D) - 2):
                newBoard[i][j] = "p"
            j += 1
        i += 1
    return newBoard

# detects key presses and moves player depending on it
def twoD_keyPressed(app, event):
    print(event.key)
    if (app.input2D.type and event.key.isdigit() and len(event.key) == 1):
        if len(app.input2D.text) >= 3:
            app.input2D.text = app.input2D.text[1:]
        app.input2D.text += event.key
    elif event.key == "Enter":
        twoD_generateMaze(app)
    elif event.key == "Backspace":
        app.input2D.text = app.input2D.text[:-1]
    elif event.key == "Right":
        twoD_movePlayer(app, 0, 1)
    elif event.key == "Left":
        twoD_movePlayer(app, 0, -1)
    elif event.key == "Up":
        twoD_movePlayer(app, -1, 0)
    elif event.key == "Down":
        twoD_movePlayer(app, 1, 0)
    elif event.key == 'r':
        twoD_reset(app)
    elif event.key == 'b':
        app.mode = "start"
    elif event.key == "s":
        app.drawSolution2D = not app.drawSolution2D
    elif event.key == "c":
        app.error2D = not app.error2D
    elif event.key == "h":
        app.mode = "help"
    elif event.key == "f":
        app.enlarge = not app.enlarge
    elif event.key == "minus":
        if app.size < 25:
            app.size += 2
    elif event.key == "equal":
        if app.size > 1:
            app.size -= 2


# resets the board for the player to play again
def twoD_reset(app):
    app.testMaze2D = Maze(app.prevSize2D, app.prevSize2D, 100)
    app.colWidth2D = (app.width - 2 * app.margin2D) / (len(app.testMaze2D.board[0]))
    app.rowWidth2D = (app.height - 2 * app.margin2D) / (len(app.testMaze2D.board))
    app.testMaze2D.generateMaze()
    app.board2D = app.testMaze2D.board
    app.pCol2D = 1
    app.pRow2D = 1
    app.finish2D = False
    app.drawSolution2D = False
    app.visited2D = set()
    twoD_findSolution(app)

# move the player if is possible
def twoD_movePlayer(app, drow, dcol):
    if app.board2D[app.pRow2D + drow][app.pCol2D + dcol] == 0:
        app.pCol2D += dcol
        app.pRow2D += drow

# draws the player as a red not
def twoD_drawPlayer(app, canvas):
    canvas.create_oval(app.margin2D + app.colWidth2D * app.pCol2D,
                    app.margin2D + app.rowWidth2D * app.pRow2D,
                    app.margin2D + app.colWidth2D * (app.pCol2D + 1),
                    app.margin2D + app.colWidth2D * (app.pRow2D + 1),
                    fill = "red")

# draws the end screen that pops up after the player had reached the end
def twoD_drawEnd(app, canvas):
    canvas.create_rectangle(app.width * 3 / 11, app.height * 4 / 11,
                app.width * 8 / 11, app.height * 7 / 11, fill = "white",
                outline = "black", width = app.width / 100)
    canvas.create_text(app.width * 5.5 / 11, app.height * 5 / 11,
                text = "Congradulations", font = "Ariel 24 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.5 / 11,
                text = "Press R to play again", font = "Ariel 16 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.9 / 11,
                text = "Or press B to return to Main Menu", font = "Ariel 16 bold")

# checks if the player reached the end
def twoD_reachedEnd(app):
    if (app.pRow2D == (len(app.board2D) - 2) and
        app.pCol2D == (len(app.board2D[0]) - 2)):
        app.finish2D = True
    else:
        app.finish2D = False

# draws an error box if the maze that is being generated is too large or small
def twoD_drawError(app, canvas):
    canvas.create_rectangle(app.width * 3 / 11, app.height * 4 / 11,
                app.width * 8 / 11, app.height * 7 / 11, fill = "white",
                outline = "black", width = app.width / 100)
    canvas.create_text(app.width * 5.5 / 11, app.height * 5 / 11,
                text = "Error with generating maze", font = "Ariel 16 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.5 / 11,
                text = "Please make sure the number is ", font = "Ariel 14 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.9 / 11,
                text = "within 1 - 100", font = "Ariel 14 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 6.3 / 11,
                text = "press c to exit", font = "Ariel 14 bold")

def twoD_generateMaze(app):
    if len(app.input2D.text) == 0 or int(app.input2D.text) > 100 or int(app.input2D.text) <= 1:
        app.error2D = True
        return
    if len(app.input2D.text) == 0:
            app.testMaze2D = Maze(app.prevSize2D, app.prevSize2D, 100)
    else:
        app.testMaze2D = Maze(int(app.input2D.text), int(app.input2D.text), 100)
        app.prevSize2D = int(app.input2D.text)
    app.input2D.text = ""
    app.colWidth2D = (app.width - 2 * app.margin2D) / (len(app.testMaze2D.board[0]))
    app.rowWidth2D = (app.height - 2 * app.margin2D) / (len(app.testMaze2D.board))
    app.testMaze2D.generateMaze()
    app.board2D = app.testMaze2D.board
    app.pCol2D = 1
    app.pRow2D = 1
    app.finish2D = False
    app.drawSolution2D = False
    app.visited2D = set()
    twoD_findSolution(app)
    app.generateMazeButton2D.pressed = False

# called every run
# checks if the player reached the end or not
def twoD_timerFired(app):
    twoD_reachedEnd(app)
    app.timePassed += 1
    if app.generateMazeButton2D.pressed == True:
        twoD_generateMaze(app)

def twoD_findSolution(app):
    print(twoD_solutionHelper(app, 1, 1))

# helper function to return the list of solution
# modified based on the 112 notes
def twoD_solutionHelper(app, row, col):
    if (row, col) in app.visited2D:
        return False
    app.visited2D.add((row, col))
    if row == (len(app.board2D) - 2) and col == (len(app.board2D[0]) - 2):
        return True
    else:
        for drow, dcol in [(1, 0), (0, 1), (0, -1), (-1, 0)]:
            # if the next position is a path (0) on the board
            if app.board2D[row + drow][col + dcol] == 0:
                if twoD_solutionHelper(app, row + drow, col + dcol) == True:
                    return True
                # backtrack if there is not solution in this path
    app.visited2D.remove((row, col))
    return None

def twoD_drawSolutions(app, canvas):
    for coord in app.visited2D:
        y, x = coord
        canvas.create_rectangle(
                    app.margin2D + app.colWidth2D * x,
                    app.margin2D + app.rowWidth2D * y,
                    app.margin2D + app.colWidth2D * (x + 1),
                    app.margin2D + app.colWidth2D * (y + 1),
                    fill = "light blue", outline = "light blue")

def twoD_drawGoal(app, canvas):
    canvas.create_rectangle(
                    app.margin2D + app.colWidth2D * (len(app.board2D) - 2),
                    app.margin2D + app.rowWidth2D * (len(app.board2D) - 2),
                    app.margin2D + app.colWidth2D * (len(app.board2D) - 1),
                    app.margin2D + app.colWidth2D * (len(app.board2D) - 1),
                    fill = "pink", outline = "pink")

# calls when the mouse if pressed
def twoD_mousePressed(app, event):
    # depending of which button is clicked on, do a certain action
    if app.input2D.inRectangle(event.x, event.y):
        app.input2D.type = not app.input2D.type
    elif app.generateMazeButton2D.inRectangle(event.x, event.y):
        app.generateMazeButton2D.pressed = True
    


