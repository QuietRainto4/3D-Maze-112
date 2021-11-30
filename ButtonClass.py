from cmu_112_graphics import*

# the button classes for all the different types of button used
# the OnOffButton and the CommandBar button 
# and the irrButton class inherits from the 
# My Button Class

class MyButton(App):
    def __init__(self, x1, y1, x2, y2, text, textSize):
        self.corners = (x1, y1, x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.text = text
        self.textSize = textSize
        self.pressed = False
    
    # checks of the x, y coordinate is in the button
    def inRectangle(self, x, y):
        if (x > self.x1 and x < self.x2 and 
            y > self.y1 and y < self.y2):
            return True
        return False
    
    # draws the button as a rectangle with the text inside
    def drawButton(self, app, canvas):
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        lineSize = int(min(cx, cy)) / 100
        canvas.create_rectangle(self.corners, fill = "white",
                                width = lineSize)
        canvas.create_text(cx, cy, text = self.text, 
                            font = f"Ariel {self.textSize}")

# a special button where the user can type inside it
class CommandBar(MyButton):
    def __init__(self, x1, y1, x2, y2, textSize):
        super().__init__(x1, y1, x2, y2, "", textSize)
        self.type = False

    # draws the insersion point when the user is typing
    def drawInsersionPoint(self, app, canvas):
        xPoint = (self.x2 - self.x1) * 3 / 4 + self.x1
        canvas.create_rectangle(xPoint, self.y1 + 5, xPoint + 1, 
                                self.y2 - 5, fill = "black", width = 0)

# a special button where the on/off state will be held and shown
class OnOffButton(MyButton):
    def __init__(self, x1, y1, x2, y2, text, textSize, size, state):
        super().__init__(x1, y1, x2, y2, text, textSize)
        self.state = state
        self.size = size
    
    # draws the button with text for the OnOff Button
    def drawButton(self, app, canvas):
        onButton = app.scaleImage(app.onButton, self.size)
        offButton = app.scaleImage(app.offButton, self.size)
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        if self.state == True:
            canvas.create_image(cx, cy, 
                        image=ImageTk.PhotoImage(onButton))
        else:
            canvas.create_image(cx, cy, 
                        image=ImageTk.PhotoImage(offButton))
        canvas.create_text(cx - 68, cy, text = self.text, 
                            font = f"Ariel {self.textSize}")

# the class for drawing the triangular shapes
class irrButton(MyButton):
    def __init__(self, x1, y1, x2, y2, direction):
        super().__init__(x1, y1, x2, y2, "", 0)
        self.direction = direction
    def drawButton(self, app, canvas):
        if self.direction == 1:
            canvas.create_polygon(self.x1, self.y1, self.x1, self.y2, self.x2, 
                                        (self.y1 + self.y2)/2, fill = "gold",
                                        outline = "black")
        else:
            canvas.create_polygon(self.x2, self.y1, self.x2, self.y2, self.x1, 
                                        (self.y1 + self.y2)/2, fill = "gold",
                                        outline = "black")

            


    
    
