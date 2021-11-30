# the help page with instructions for the 3D game

from cmu_112_graphics import*

def help3D_redrawAll(app, canvas):
    canvas.create_text(app.width * 5.5/11, app.height * 1/11,
                        text = "3D Help", font = "Ariel 36")
    help3D_drawInstructions(app, canvas)
    canvas.create_image(570, 330, 
                        image=ImageTk.PhotoImage(app.graph))
                        
def help3D_drawInstructions(app, canvas):
    instructions = '''
    3D maze game
    The goal is to arrive at the pink                          A graph showing the planes
    square in the top layer. The red                                  in the 3D maze
    dot represents where you are currently      
    and you can move the red dot using the
    arrow keys or by using the z and x key, 
    where the z key is for moving vertically
    up and the x key is for moving vertically 
    down. When you reach the end you will 
    have the option to replay. You can
    generate a maze of any reasonable size 
    by typing the size of the maze that you 
    want to generate into input box at the 
    top right corner of the screen.

    some keys for the 3D game
    r - resets the game for the player to play again
    b - goes back to the previous page
    c - closes the error window
    arrow keys - go left, right, up, down in the maze
    z - go up vertically in the 3d maze
    x - go down verticaly in the 3d maze
    h - opens up the help page
    a - changes the player's image

    Have fun playing! :)
    '''

    canvas.create_text(app.width * 4.8/11, app.height * 5.5/11,
                        text = instructions, font = "Ariel 14")

def help3D_keyPressed(app, event):
    if event.key == "b":
        app.mode = "threeD"


    