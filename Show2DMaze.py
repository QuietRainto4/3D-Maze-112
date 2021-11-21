from cmu_112_graphics import*
from MazeClass import*

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

def twoD_redrawAll(app, canvas):
    twoD_drawMaze(app, canvas)
    twoD_drawPlayer(app, canvas)
    if app.finish2D == True:
        twoD_drawEnd(app, canvas)

def twoD_keyPressed(app, event):
    if event.key == "Right":
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

def twoD_reset(app):
    app.testMaze2D = Maze(10, 10, 100)
    app.colWidth2D = (app.width - 2 * app.margin2D) / (len(app.testMaze2D.board[0]))
    app.rowWidth2D = (app.height - 2 * app.margin2D) / (len(app.testMaze2D.board))
    app.testMaze2D.generateMaze()
    app.board2D = app.testMaze2D.board
    app.pCol2D = 1
    app.pRow2D = 1
    app.finish2D = False

def twoD_movePlayer(app, drow, dcol):
    if app.board2D[app.pRow2D + drow][app.pCol2D + dcol] == 0:
        app.pCol2D += dcol
        app.pRow2D += drow

def twoD_drawPlayer(app, canvas):
    canvas.create_oval(app.margin2D + app.colWidth2D * app.pCol2D,
                    app.margin2D + app.rowWidth2D * app.pRow2D,
                    app.margin2D + app.colWidth2D * (app.pCol2D + 1),
                    app.margin2D + app.colWidth2D * (app.pRow2D + 1),
                    fill = "red")

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

def twoD_reachedEnd(app):
    if (app.pRow2D == (len(app.board2D) - 2) and
        app.pCol2D == (len(app.board2D[0]) - 2)):
        app.finish2D = True
    else:
        app.finish2D = False

def twoD_timerFired(app):
    twoD_reachedEnd(app)