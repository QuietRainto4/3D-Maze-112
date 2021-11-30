from cmu_112_graphics import*
from MazeClass import*
from ButtonClass import*
import time

# draws the maze
def drawMaze(app, canvas, board):
    for numRow in range(len(board)):
        for numCol in range(len(board)):
            if board[numRow][numCol] == 1:
                canvas.create_rectangle(
                    app.margin + app.colWidth2D * numCol,
                    app.margin + app.rowWidth2D * numRow,
                    app.margin + app.colWidth2D * (numCol + 1),
                    app.margin + app.colWidth2D * (numRow + 1),
                    fill = "black")

# draws on the canvas
def twoD_redrawAll(app, canvas):
    twoD_drawTime(app, canvas)
    if app.enlarge == False:
        drawMaze(app, canvas, app.board2D)
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

    # if the player has reached the end, draw the end screen
    if app.finish2D == True:
        twoD_drawEnd(app, canvas)
    # draws the buttons
    for button in app.button2D:
        button.drawButton(app, canvas)
    # for the flickering bar
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
# for the solution board, if the point is in the set
# then draw it as solution
def twoD_enlargedMaze(app, canvas, newBoard):
    width = (app.width - 2 * app.margin) / app.size
    height = (app.height - 2 * app.margin) / app.size
    for numRow in range(len(newBoard)):
        for numCol in range(len(newBoard[0])):
            if newBoard[numRow][numCol] == "p":
                canvas.create_rectangle(
                    app.margin + width * numCol,
                    app.margin + height * numRow,
                    app.margin + width * (numCol + 1),
                    app.margin + height * (numRow + 1),
                    fill = "pink")
            elif newBoard[numRow][numCol] == 1:
                canvas.create_rectangle(
                    app.margin + width * numCol,
                    app.margin + height * numRow,
                    app.margin + width * (numCol + 1),
                    app.margin + height * (numRow + 1),
                    fill = "black")
            elif newBoard[numRow][numCol] == "b":
                canvas.create_rectangle(
                    app.margin + width * numCol,
                    app.margin + height * numRow,
                    app.margin + width * (numCol + 1),
                    app.margin + height * (numRow + 1),
                    fill = "light blue", outline = "light blue")
            
            if (numRow == len(newBoard) // 2 and 
                    numCol == len(newBoard[0]) // 2):
                if app.player == 6:
                    canvas.create_oval(
                        app.margin + width * numCol,
                        app.margin + height * numRow,
                        app.margin + width * (numCol + 1),
                        app.margin + height * (numRow + 1),
                        fill = "red")
                else:
                    cx = (2 * app.margin + width *(2 * numCol + 1)) / 2
                    cy = (2 * app.margin + height *(2 * numRow + 1)) / 2
                    # 400 is the size of the image
                    size = width / 300 
                    image = app.players[app.player]
                    player = app.scaleImage(image, size)
                    canvas.create_image(cx, cy, 
                                    image=ImageTk.PhotoImage(player))

# returns the 9 * 9 surrounding of the board, keeping the player 
#                           in the center at all times
# if it is out of the board, it is represented by a 0
def twoD_partOfBoard(app, board):
    newBoard = []
    for i in range(app.size):
        newBoard.append([0] * app.size)
    i = 0
    for row in range(app.pRow2D - app.size//2, 
                    app.pRow2D + app.size//2 + 1):
        j = 0
        for col in range(app.pCol2D - app.size//2, 
                    app.pCol2D + app.size//2 + 1):
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
    if (app.input2D.type and event.key.isdigit() and len(event.key) == 1):
        if len(app.input2D.text) >= 3:
            app.input2D.text = app.input2D.text[1:]
        app.input2D.text += event.key
    elif event.key == "Enter":
        twoD_generateMaze(app)
    elif event.key == "Backspace":
        app.input2D.text = app.input2D.text[:-1]
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
    elif event.key == "a":
        twoD_playerIncrease(app)
    elif event.key == "minus":
        if app.size < 25:
            app.size += 2
    elif event.key == "equal":
        if app.size > 1:
            app.size -= 2

    notMove = False
    # when the player reaches the end, stop any action
    if app.finish2D == True:
        return 
    elif event.key == "Right":
        twoD_movePlayer(app, 0, 1)
    elif event.key == "Left":
        twoD_movePlayer(app, 0, -1)
    elif event.key == "Up":
        twoD_movePlayer(app, -1, 0)
    elif event.key == "Down":
        twoD_movePlayer(app, 1, 0)
    else:
        notMove = True
    # start the timer if the key pressed is up down left or right
    if notMove == False:
        if app.moveTime2D == False:
            app.moveTime2D = True
            app.startTime2D = time.time()


# resets the board for the player to play again
def twoD_reset(app):
    app.testMaze2D = Maze(app.prevSize2D, app.prevSize2D, 100)
    app.colWidth2D = (app.width - 2 * app.margin) / (len(app.testMaze2D.board[0]))
    app.rowWidth2D = (app.height - 2 * app.margin) / (len(app.testMaze2D.board))
    app.testMaze2D.generateMaze()
    app.board2D = app.testMaze2D.board
    app.pCol2D = 1
    app.pRow2D = 1
    app.finish2D = False
    app.drawSolution2D = False
    app.visited2D = set()
    twoD_findSolution(app)
    app.startTime2D = time.time()
    app.currTime2D = 0
    app.moveTime2D = False

# move the player if is possible
def twoD_movePlayer(app, drow, dcol):
    if app.board2D[app.pRow2D + drow][app.pCol2D + dcol] == 0:
        app.pCol2D += dcol
        app.pRow2D += drow

# draws the player as a red not
def twoD_drawPlayer(app, canvas):
    if app.player == 6:
        canvas.create_oval(app.margin + app.colWidth2D * app.pCol2D,
                        app.margin + app.rowWidth2D * app.pRow2D,
                        app.margin + app.colWidth2D * (app.pCol2D + 1),
                        app.margin + app.colWidth2D * (app.pRow2D + 1),
                        fill = "red")
    else:
        cx = (2 * app.margin + app.colWidth2D *(2 * app.pCol2D + 1)) / 2
        cy = (2 * app.margin + app.rowWidth2D *(2 * app.pRow2D + 1)) / 2
        # 400 is the size of the image
        size = app.colWidth2D / 300 
        image = app.players[app.player]
        player = app.scaleImage(image, size)
        canvas.create_image(cx, cy, 
                        image=ImageTk.PhotoImage(player))

# draws the end screen that pops up after the player had reached the end
def twoD_drawEnd(app, canvas):
    canvas.create_rectangle(app.width * 3 / 11, app.height * 4 / 11,
                app.width * 8 / 11, app.height * 7 / 11, fill = "white",
                outline = "black", width = app.width / 100)
    canvas.create_text(app.width * 5.5 / 11, app.height * 4.75 / 11,
                text = "Congradulations", font = "Ariel 24 bold")
    canvas.create_text(app.width * 5.5 / 11, app.height * 5.25 / 11,
                text = f"time: {app.currTime2D}", font = "Ariel 16 bold")
    app.endRetry.drawButton(app, canvas)
    app.endBack.drawButton(app, canvas)

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

# When enter is pressed or when the generate button is pressed
# generate a new maze
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
    app.colWidth2D = (app.width - 2 * app.margin) / (len(app.testMaze2D.board[0]))
    app.rowWidth2D = (app.height - 2 * app.margin) / (len(app.testMaze2D.board))
    app.testMaze2D.generateMaze()
    app.board2D = app.testMaze2D.board
    app.pCol2D = 1
    app.pRow2D = 1
    app.finish2D = False
    app.drawSolution2D = False
    app.visited2D = set()
    twoD_findSolution(app)
    app.generateMazeButton2D.pressed = False
    app.startTime2D = time.time()
    app.currTime2D = 0
    app.moveTime2D = False
    
# called every run
# checks if the player reached the end or not
def twoD_timerFired(app):
    twoD_reachedEnd(app)
    # if at end, stop moving
    if app.finish2D == True:
        app.moveTime2D = False
    app.timePassed += 1
    if app.moveTime2D == False:
        app.currTime2D = app.currTime2D
    else:
        app.currTime2D = int(time.time() - app.startTime2D)
    
    # Check if the buttons are pressed
    if app.generateMazeButton2D.pressed == True:
        app.generateMazeButton2D.pressed = False
        twoD_generateMaze(app)
    if app.changePlayer.pressed == True:
        app.changePlayer.pressed = False
        twoD_playerIncrease(app)
    if app.finish2D == True:
        if app.endRetry.pressed == True:
            app.endRetry.pressed = False
            twoD_reset(app)
        if app.endBack.pressed == True:
            app.endBack.pressed = False
            app.mode = "start"

def twoD_findSolution(app):
    twoD_solutionHelper(app, 1, 1)

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
                    app.margin + app.colWidth2D * x,
                    app.margin + app.rowWidth2D * y,
                    app.margin + app.colWidth2D * (x + 1),
                    app.margin + app.colWidth2D * (y + 1),
                    fill = "light blue", outline = "light blue")

def twoD_drawGoal(app, canvas):
    canvas.create_rectangle(
                    app.margin + app.colWidth2D * (len(app.board2D) - 2),
                    app.margin + app.rowWidth2D * (len(app.board2D) - 2),
                    app.margin + app.colWidth2D * (len(app.board2D) - 1),
                    app.margin + app.colWidth2D * (len(app.board2D) - 1),
                    fill = "pink", outline = "pink")

# calls when the mouse if pressed
def twoD_mousePressed(app, event):
    # depending of which button is clicked on, do a certain action
    for buttons in app.button2D:
        if buttons.inRectangle(event.x, event.y):
            buttons.pressed = True

    if app.finish2D == True:
        if app.endRetry.inRectangle(event.x, event.y):
            app.endRetry.pressed = True
        elif app.endBack.inRectangle(event.x, event.y):
            app.endBack.pressed = True
    
# draw time
def twoD_drawTime(app, canvas):
    canvas.create_text(app.width * 3 / 11, app.height * 0.5 / 11,
                text = f"time: {app.currTime2D}", font = "Ariel 20")

# switch player character
def twoD_playerIncrease(app):
    app.player += 1
    if app.player > 6:
        app.player = 0