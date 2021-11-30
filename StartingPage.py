from cmu_112_graphics import*
import math
from ButtonClass import*

# make 3D maze that you can see and drag
# include help funciton and instructions
def start_redrawAll(app, canvas):
    start_drawMaze(app, canvas)
    canvas.create_image(app.width / 2, app.height * 3/11, 
                        image=ImageTk.PhotoImage(app.title))
    # draws the three boxes for differnt games
    for buttons in app.startButtons:
        buttons.drawButton(app, canvas)
    # canvas.create_rectangle(app.width * 3/11, app.height * 5/11,
    #                         app.width * 8/11, app.height * 6/11,
    #                         fill = "white", width = 5)
    # canvas.create_rectangle(app.width * 3/11, app.height * 6.5/11,
    #                         app.width * 8/11, app.height * 7.5/11,
    #                         fill = "white", width = 5)
    # canvas.create_rectangle(app.width * 3/11, app.height * 8/11,
    #                         app.width * 8/11, app.height * 9/11,
    #                         fill = "white", width = 5)
    
def start_drawMaze(app, canvas):
    for numRow in range(len(app.boardBack)):
        for numCol in range(len(app.boardBack[0])):
            if app.boardBack[numRow][numCol] == 1:
                x1 = app.colWidthBack * numCol
                y1 = app.rowWidthBack * numRow
                x2 = app.colWidthBack * (numCol + 1)
                y2 = app.colWidthBack * (numRow + 1)

                # rotateMatrix = numpy.array([[math.cos(app.theta), -math.sin(app.theta)],
                #                              [math.sin(app.theta), math.cos(app.theta)]])
                # firstPoint = numpy.array([[x1], [y1]])
                # secondPoint = numpy.array([[x2], [y2]])
                # newfPoint = numpy.matmul(rotateMatrix, firstPoint)
                # newsPoint = numpy.matmul(rotateMatrix, secondPoint)
                # newX1 = newfPoint[0, 0]
                # newY1 = newfPoint[1, 0]
                # newX2 = newsPoint[0, 0]
                # newY2 = newsPoint[1, 0]

                # r1, theta1 = cartasianToPolar(app, x1, y1)
                # r2, theta2 = cartasianToPolar(app, x2, y2)
                # x1, y1 = polarToCartasian(app, r1, theta1)
                # x2, y2 = polarToCartasian(app, r2, theta2)

                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill = "light grey", outline = "light grey")

def start_mousePressed(app, event):
    for buttons in app.startButtons:
        if buttons.inRectangle(event.x, event.y):
            buttons.pressed = True

def cartasianToPolar(app, x, y):
    centerX = app.width / 2
    centerY = app.height / 2
    r = distance(centerX, centerY, x, y)
    theta = math.atan((centerY - y)/(centerX - x))
    if (centerX - x) < 0:
        theta = theta + math.pi
    return r, theta
    
def polarToCartasian(app, r, theta):
    x = r * math.cos(theta + app.theta)
    y = r * math.sin(theta + app.theta)
    return (x, y)


def distance(centerX, centerY, x, y):
    return ((centerX - x) ** 2 + (centerY - y) ** 2) ** 0.5


def start_timerFired(app):
    app.theta += math.pi / 1000
    if app.startButtons[0].pressed == True:
        app.mode = 'twoD'
        app.startButtons[0].pressed = False
    elif app.startButtons[1].pressed == True:
        app.mode = 'threeD'
        app.startButtons[1].pressed = False
    elif app.startButtons[2].pressed == True:
        app.mode = 'help'
        app.startButtons[2].pressed = False



