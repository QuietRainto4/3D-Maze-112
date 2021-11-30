# the main file for all the different screens
# includes all variables used throughout the entire game

from cmu_112_graphics import*
from MazeClass import*
from Show2DMaze import*
from show3DMaze import*
from StartingPage import*
from HelpPage import*
from Help3DPage import*
from Help3LPage import*
from Help2DPage import*
from Layer3D import*


def appStarted(app):
    
    app.mode = "start"
    app.timePassed = 0
    app.margin = 70

    app.player = 6
    # list of players
    app.players = []
    # Pictures by Johanna Park from 112 hackathon
    app.pink = app.loadImage('PinkPlayer.png')
    app.blue = app.loadImage('BluePlayer.png')
    app.purple = app.loadImage('PurplePlayer.png')
    app.white = app.loadImage('WhitePlayer.png')
    app.green = app.loadImage('GreenPlayer.png')
    app.yellow = app.loadImage('YellowPlayer.png')
    app.players.append(app.pink)
    app.players.append(app.blue)
    app.players.append(app.purple)
    app.players.append(app.green)
    app.players.append(app.yellow)
    app.players.append(app.white)

    # the values for 2D maze
    app.testMaze2D = Maze(25, 25, 100)
    app.colWidth2D = (app.width - 2 * app.margin) / (len(app.testMaze2D.board[0]))
    app.rowWidth2D = (app.height - 2 * app.margin) / (len(app.testMaze2D.board))
    app.testMaze2D.generateMaze()
    app.board2D = app.testMaze2D.board
    app.copyBoard = []
    app.pCol2D = 1
    app.pRow2D = 1
    app.finish2D = False
    app.drawSolution2D = False
    app.error2D = False
    app.enlarge = False
    app.size = 9
    app.visited2D = set()
    app.startTime2D = time.time()
    app.currTime2D = 0
    app.moveTime2D = False
    twoD_findSolution(app)
    app.prevSize2D = 25
    app.changePlayer = MyButton(app.width * 4.75/11, app.height * 0.25/11, 
                        app.width * 6.8/11, app.height * 0.75/11, "Player(a)", 
                        16)
    app.generateMazeButton2D = MyButton(app.width * 7/11, app.height * 0.25/11, 
                            app.width * 8.8/11, app.height * 0.75/11, "Generate", 
                            16)
    app.input2D = CommandBar(app.width * 9/11, app.height * 0.25/11, 
                            app.width * 10/11, app.height * 0.75/11, 16)
    app.button2D  = []
    app.button2D.append(app.changePlayer)
    app.button2D.append(app.generateMazeButton2D)
    app.button2D.append(app.input2D)

    app.endRetry = MyButton(app.width * 4/11, app.height * 5.5/11, 
                        app.width * 7/11, app.height * 5.9/11, "Retry(r)", 
                        14)
    app.endBack = MyButton(app.width * 4/11, app.height * 6/11, 
                        app.width * 7/11, app.height * 6.4/11, "Back(b)", 
                        14)
    

    # the values for the 3D maze
    app.testMaze3D = threeDMaze(5, 5, 5, 100)
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
    threeD_findSolution(app)
    app.error3D = False
    app.prevSize3D = 5
    app.startTime3D = time.time()
    app.currTime3D = 0
    app.moveTime3D = False
    app.generateMazeButton3D = MyButton(app.width * 7/11, app.height * 0.25/11, 
                            app.width * 8.8/11, app.height * 0.75/11, "Generate", 
                            16)
    app.input3D = CommandBar(app.width * 9/11, app.height * 0.25/11, 
                            app.width * 10/11, app.height * 0.75/11, 16)
    app.plusCharacter = irrButton(app.width * 6.5/11, app.height * 2/11, 
                            app.width * 7/11, app.height * 2.5/11, 1)
    app.decreaseCharacter = irrButton(app.width * 9/11, app.height * 2/11, 
                            app.width * 9.5/11, app.height * 2.5/11, 0)
    app.zButton = OnOffButton(app.width * 7/11, app.height * 3.75/11, 
                            app.width * 8/11, app.height * 4.25/11, "Z Switch", 
                            12, 0.1, True)
    app.xButton = OnOffButton(app.width * 7/11, app.height * 4.5/11, 
                            app.width * 8/11, app.height * 5/11, "X Switch", 
                            12, 0.1, True)
    app.yButton = OnOffButton(app.width * 9/11, app.height * 4.5/11, 
                            app.width * 10/11, app.height * 5/11, "Y Switch", 
                            12, 0.1, True)

    # the images for the buttons
    # https://www.vectorstock.com/royalty-free-vector/on-and-off-icon-editable-switch-button-sign-vector-28695671
    app.onButton = app.loadImage('On Button.png')
    app.offButton = app.loadImage('Off Button.png')

    app.button3D = []
    app.button3D.append(app.generateMazeButton3D)
    app.button3D.append(app.input3D)
    app.button3D.append(app.zButton)
    app.button3D.append(app.xButton)
    app.button3D.append(app.yButton)
    app.button3D.append(app.plusCharacter)
    app.button3D.append(app.decreaseCharacter)

    # https://www.vvidget.com/manuals/GraphIDE/Data3DGraphics/Graph/index.html
    app.graph = app.loadImage('3D Graph.png')
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
    button1 = MyButton(app.width * 3/11, app.height * 4/11,
                        app.width * 8/11, app.height * 5/11,
                        "2D Maze", 36)
    button2 = MyButton(app.width * 3/11, app.height * 5.5/11,
                        app.width * 8/11, app.height * 6.5/11,
                        "3D Maze", 36)
    button3 = MyButton(app.width * 3/11, app.height * 7/11,
                        app.width * 8/11, app.height * 8/11,
                        "3D Layer", 36)
    button4 = MyButton(app.width * 3/11, app.height * 8.5/11,
                        app.width * 8/11, app.height * 9.5/11,
                        "Help", 36)
    app.startButtons = []
    app.startButtons.append(button1)
    app.startButtons.append(button2)
    app.startButtons.append(button3)
    app.startButtons.append(button4)


    # a third mode where the player can only see the horizontal layer
    # it is very similar to the 2D representation
    # therefore will just use a lot of method from 2D
    app.testMaze3L = threeDMaze(5, 5, 5, 100)
    app.testMaze3L.generate3DMaze()
    app.board3L = app.testMaze3L.board
    # setting the finishing position
    app.board3L[len(app.board3L)-2][len(app.board3L[0])-2][len(app.board3L[0][0])-2] = 'e'
    # the board with player
    app.boardP3L = copy.deepcopy(app.board3L)
    # print3dList(app.board3D)
    app.size3L = 9
    app.pCol3L = 1
    app.pRow3L = 1
    app.pHeight3L = 1 
    app.finish3L = False
    app.visited3L = set()
    app.drawSolution3L = False
    layer3D_findSolution(app)
    app.error3L = False
    app.enlarge3L = False
    app.prevSize3L = 5
    app.startTime3L = time.time()
    app.currTime3L = 0
    app.moveTime3L = False
    app.generateMazeButton3L = MyButton(app.width * 7/11, app.height * 0.25/11, 
                            app.width * 8.8/11, app.height * 0.75/11, "Generate", 
                            16)
    app.changePlayer = MyButton(app.width * 4.75/11, app.height * 0.25/11, 
                        app.width * 6.8/11, app.height * 0.75/11, "Player(a)", 
                        16)
    app.input3L = CommandBar(app.width * 9/11, app.height * 0.25/11, 
                            app.width * 10/11, app.height * 0.75/11, 16)
    app.button3L = []
    app.button3L.append(app.generateMazeButton3L)
    app.button3L.append(app.input3L)
    app.button3L.append(app.changePlayer)

runApp(width=800, height=800)

