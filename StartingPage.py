# the file that draws the starting page

from cmu_112_graphics import*
import math
from ButtonClass import*

def start_redrawAll(app, canvas):
    start_drawMaze(app, canvas)
    canvas.create_image(app.width / 2, app.height * 2/11, 
                        image=ImageTk.PhotoImage(app.title))
    # draws the three boxes for differnt games
    for buttons in app.startButtons:
        buttons.drawButton(app, canvas)
    
def start_drawMaze(app, canvas):
    for numRow in range(len(app.boardBack)):
        for numCol in range(len(app.boardBack[0])):
            if app.boardBack[numRow][numCol] == 1:
                x1 = app.colWidthBack * numCol
                y1 = app.rowWidthBack * numRow
                x2 = app.colWidthBack * (numCol + 1)
                y2 = app.colWidthBack * (numRow + 1)
                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill = "light grey", outline = "light grey")

def start_mousePressed(app, event):
    for buttons in app.startButtons:
        if buttons.inRectangle(event.x, event.y):
            buttons.pressed = True

def start_timerFired(app):
    app.theta += math.pi / 1000
    if app.startButtons[0].pressed == True:
        app.mode = 'twoD'
        app.startButtons[0].pressed = False
    elif app.startButtons[1].pressed == True:
        app.mode = 'threeD'
        app.startButtons[1].pressed = False
    elif app.startButtons[2].pressed == True:
        app.mode = 'layer3D'
        app.startButtons[2].pressed = False
    elif app.startButtons[3].pressed == True:
        app.mode = 'help'
        app.startButtons[3].pressed = False



