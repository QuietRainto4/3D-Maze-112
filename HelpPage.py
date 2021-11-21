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
    This is a more simple verson of the maze for you to practice
    on before trying the more difficut 3D maze. The goal is to 
    arrive at the pink square in bottm right corner. The red dot 
    represents where you are currently and you can move the red 
    dot using the arrow keys. You can generate a maze of any 
    resonable size by typing the size of the maze that you want to 
    generate into input box at the top right corner of the screen.

    Some commands for modifying the maze
    wall off --- Turn the visability of the walls off
    wall on --- Turn the visability of the walls on
    see section --- enlarge the maze so that you will only see part
                    of the maze as you traverse through it
    see entire --- be able to see the entire maze
    gen (size) --- generate a 2D maze of a certain size, the size
                    should be between 2 - 200 for better performance

    3D maze game
    The goal is to arrive at the pink square in the top layer.
    The red dot represents where you are currently and you can 
    move the red dot using the arrow keys or by using the z and 
    x key, where the z key is for moving vertically up and the 
    x key is for moving vertically down. When you reach the end
    you will have the option to replay. You can generate a maze
    of any reasonable size by typing the size of the maze that you 
    want to generate into input box at the top right corner of 
    the screen.

    If you want to increase the difficutly, you can also turn off 
    the walls by typing {vis off}. If you want to turn any views 
    off you can type { x (or y or z) off}. To turn it on, type 
    { x (or y or z) on}

    Have fun playing! :)

    '''



    