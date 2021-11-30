from cmu_112_graphics import*

def help2D_redrawAll(app, canvas):
    canvas.create_text(app.width * 5.5/11, app.height * 1/11,
                        text = "Help", font = "Ariel 36")
    help2D_drawInstructions(app, canvas)

def help2D_drawInstructions(app, canvas):
    instructions = '''
    2D maze game
    This is a more simple verson of the maze for you to practice on before trying the 
    more difficut 3D maze. The goal is to arrive at the pink square in bottm right 
    corner. The red dot represents where you are currently and you can move the red 
    dot using the arrow keys. You can generate a maze of any resonable size by typing 
    the size of the maze that you want to generate into input box at the top right 
    corner of the screen. If you only want to see a section of the maze, you can press
    f to go into the enlarged mode and f as well to leave the enlarged mode.

    some keys for the game
    r - resets the game for the player to play again
    b - goes back to the main screen
    c - closes the error window
    arrow keys - go left, right, up, down in the maze
    z - go up vertically in the 3d maze
    x - go down verticaly in the 3d maze
    h - opens up the help page
    f - enlarges the maze
    cmd + - will increase the size of the maze in the 
            enlarged mode
    cmd - - will decrease the size of the maze in the 
            enlarged mode
    a - changes the player's image

    Have fun playing! :)
    '''
    canvas.create_text(app.width * 5.5/11, app.height * 5.5/11,
                        text = instructions, font = "Ariel 14")

def help2D_keyPressed(app, event):
    if event.key == "b":
        app.mode = "twoD"


    