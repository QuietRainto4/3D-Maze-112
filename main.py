# the main file for all the different screens

from cmu_112_graphics import*
from MazeClass import*
from Show2DMaze import*
from show3DMaze import*
from StartingPage import*
# from ButtonClass import*

def appStarted(app):
    app.mode = "start"

    # the values for 2D maze
    app.testMaze2D = Maze(10, 10, 100)
    app.margin2D = 50
    app.colWidth2D = (app.width - 2 * app.margin2D) / (len(app.testMaze2D.board[0]))
    app.rowWidth2D = (app.height - 2 * app.margin2D) / (len(app.testMaze2D.board))
    app.testMaze2D.generateMaze()
    app.board2D = app.testMaze2D.board
    app.pCol2D = 1
    app.pRow2D = 1
    app.finish2D = False

    # the values for the 3D maze
    app.testMaze3D = threeDMaze(4, 4, 4, 100)
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

    # the values for starting page
    # https://www.dafont.com/maze-line.font
    # maze title picture from here
    app.title = app.loadImage('Maze Title.png')
    app.title = app.scaleImage(app.title, 0.3)
    app.background = Maze(25, 25, 100)
    app.colWidthBack = (app.width) / (len(app.background.board[0]))
    app.rowWidthBack = (app.height) / (len(app.background.board))
    app.background.generateMaze()
    app.boardBack = app.background.board
    app.theta = 0
    button1 = MyButton(app.width * 3/11, app.height * 5/11,
                        app.width * 8/11, app.height * 6/11,
                        text = "2D Maze")
    button2 = MyButton(app.width * 3/11, app.height * 6.5/11,
                        app.width * 8/11, app.height * 7.5/11,
                        text = "3D Maze")
    button3 = MyButton(app.width * 3/11, app.height * 8/11,
                        app.width * 8/11, app.height * 9/11,
                        text = "impossible Maze")
    app.startButtons = []
    app.startButtons.append(button1)
    app.startButtons.append(button2)
    app.startButtons.append(button3)



runApp(width=800, height=800)


# Questions for TP 2
# Import numpy and debug the rotation
# Can store a function inside an object button such that 
# it will execute when pressed


# Todo list
# backtracking algorithm for both mazes and somehow show them
# the input bar + commands needed
# delete boxes after used
