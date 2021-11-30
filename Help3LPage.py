from cmu_112_graphics import*

def help3L_redrawAll(app, canvas):
    canvas.create_text(app.width * 5.5/11, app.height * 1/11,
                        text = "Help 3D Layer", font = "Ariel 36")
    help3L_drawInstructions(app, canvas)

def help3L_drawInstructions(app, canvas):
    instructions = '''
    3D layer maze game
    The goal is to arrive at the pink square in the top layer. The red dot 
    represents where you are currently and you can move the red dot using 
    the arrow keys or by using the z and x key, where the z key is for moving 
    vertically up and the x key is for moving vertically down. When you reach 
    the end you will have the option to replay. You can generate a maze of any 
    reasonable size by typing the size of the maze that you want to generate 
    into input box at the top right corner of the screen. The + sign meant that 
    you can go up from that spot, the - sign means that you can go down from that 
    spot, and the = sign means the you can go both up and down from that spot. 

    some keys for the game
    r - resets the game for the player to play again
    b - goes back to the previous page
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

def help3L_keyPressed(app, event):
    if event.key == "b":
        app.mode = "layer3D"


    