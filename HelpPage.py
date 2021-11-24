from cmu_112_graphics import*

def help_redrawAll(app, canvas):
    canvas.create_text(app.width * 5.5/11, app.height * 1/11,
                        text = "Help", font = "Ariel 36")
    help_drawInstructions(app, canvas)

def help_drawInstructions(app, canvas):
    canvas.create_text(app.width * 5.5/11, app.height * 1/11,
                        text = "Help", font = "Ariel 36")

    instructions = '''
    2D maze game
    This is a more simple verson of the maze for you to practice on before trying the 
    more difficut 3D maze. The goal is to arrive at the pink square in bottm right 
    corner. The red dot represents where you are currently and you can move the red 
    dot using the arrow keys. You can generate a maze of any resonable size by typing 
    the size of the maze that you want to generate into input box at the top right 
    corner of the screen.

    3D maze game
    The goal is to arrive at the pink square in the top layer. The red dot represents 
    where you are currently and you can move the red dot using the arrow keys or by 
    using the z and x key, where the z key is for moving vertically up and the x key is 
    for moving vertically down. When you reach the end you will have the option to replay. 
    You can generate a maze of any reasonable size by typing the size of the maze that you 
    want to generate into input box at the top right corner of the screen.

    some keys for the game
    r - resets the game for the player to play again
    b - goes back to the main screen
    c - closes the error window
    arrow keys - go left, right, up, down in the maze
    z - go up vertically in the 3d maze
    x - go down verticaly in the 3d maze
    h - opens upp the help page

    Have fun playing! :)
    '''

    canvas.create_text(app.width * 5.5/11, app.height * 5.5/11,
                        text = instructions, font = "Ariel 14")

def help_keyPressed(app, event):
    if event.key == "b":
        app.mode = "start"


    