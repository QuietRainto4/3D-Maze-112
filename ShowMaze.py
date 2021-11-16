from cmu_112_graphics import*
from MazeClass import*

class ShowMaze(App):
    def appStarted(app):
        testMaze = Maze(10, 10, 100)
        app.colWidth = app.width / testMaze.col
        app.rowWidth = app.height / testMaze.row
        app.margin = 50
        testMaze.generateMaze()
        app.board = testMaze.board

    # draws the maze
    def drawMaze(app, canvas, self):
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
        app.drawMaze(app, canvas)

ShowMaze(width = 400, height = 400)

