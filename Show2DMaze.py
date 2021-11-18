from cmu_112_graphics import*
from MazeClass import*

def appStarted(app):
    app.testMaze = Maze(25, 25, 100)
    app.margin = 50
    app.colWidth = (app.width - 2 * app.margin) / (len(app.testMaze.board[0]))
    app.rowWidth = (app.height - 2 * app.margin) / (len(app.testMaze.board))
    app.testMaze.generateMaze()
    app.board = app.testMaze.board
    app.pCol = 1
    app.pRow = 1

# draws the maze
def drawMaze(app, canvas):
    for numRow in range(len(app.board)):
        for numCol in range(len(app.board[0])):
            if app.board[numRow][numCol] == 1:
                canvas.create_rectangle(
                    app.margin + app.colWidth * numCol,
                    app.margin + app.rowWidth * numRow,
                    app.margin + app.colWidth * (numCol + 1),
                    app.margin + app.colWidth * (numRow + 1),
                    fill = "black")

def redrawAll(app, canvas):
    drawMaze(app, canvas)
    drawPlayer(app, canvas)

def keyPressed(app, event):
    if event.key == "Right":
        movePlayer(app, 0, 1)
    elif event.key == "Left":
        movePlayer(app, 0, -1)
    elif event.key == "Up":
        movePlayer(app, -1, 0)
    elif event.key == "Down":
        movePlayer(app, 1, 0)

def movePlayer(app, drow, dcol):
    if app.board[app.pRow + drow][app.pCol + dcol] == 0:
        app.pCol += dcol
        app.pRow += drow

def drawPlayer(app, canvas):
    canvas.create_oval(app.margin + app.colWidth * app.pCol,
                    app.margin + app.rowWidth * app.pRow,
                    app.margin + app.colWidth * (app.pCol + 1),
                    app.margin + app.colWidth * (app.pRow + 1),
                    fill = "red")

runApp(width = 800, height = 800)

