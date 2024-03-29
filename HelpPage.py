# the main help page that explains the game

from cmu_112_graphics import*

def help_redrawAll(app, canvas):
    canvas.create_text(app.width * 5.5/11, app.height * 1/11,
                        text = "Help", font = "Ariel 36")
    help_drawInstructions(app, canvas)

def help_drawInstructions(app, canvas):
    instructions = '''
    This is a maze game made by Yu Ching Wu. There are three 
    different modes to play in, the 2D mode, 3D, mode, and 
    3D Layer mode. The 2D mode is the normal maze, 3D mode 
    is a maze where you can also go vertically up and down 
    and the planes are the x, y, z, planes in a 3D graph, the 
    3D layer mode only shows the z plane but has +, -, =, 
    signs to signify whether the player can move up or down
    at that spot. 

    Somtimes, if the maze that is generated is too large, the
    game may be a little slow. Therefore it is best if you
    can pick the best maze size to play with.

    If needed, press h in the different mode to check out
    all the shortcuts avaliable in that particular game.
    Then press b to go back to the game that you are playing

    All the mazes are generated by eller's algorithm
    Have fun playing! :)
    '''
    canvas.create_text(app.width * 5.5/11, app.height * 5.5/11,
                        text = instructions, font = "Ariel 14")

def help_keyPressed(app, event):
    if event.key == "b":
        app.mode = "start"


    