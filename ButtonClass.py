from cmu_112_graphics import*

# https://www.vectorstock.com/royalty-free-vector/on-and-off-icon-editable-switch-button-sign-vector-28695671


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
    
    def inRectangle(self, x, y):
        if (x > self.x1 and x < self.x2 and 
            y > self.y1 and y < self.y2):
            return True
        return False
    
    def drawButton(self, app, canvas):
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        lineSize = int(min(cx, cy)) / 100
        canvas.create_rectangle(self.corners, fill = "white",
                                width = lineSize)
        canvas.create_text(cx, cy, text = self.text, 
                            font = f"Ariel {self.textSize}")
    
class CommandBar(MyButton):
    def __init__(self, x1, y1, x2, y2, textSize):
        super().__init__(x1, y1, x2, y2, "", textSize)
        self.type = False

    def drawInsersionPoint(self, app, canvas):
        xPoint = (self.x2 - self.x1) * 3 / 4 + self.x1
        canvas.create_rectangle(xPoint, self.y1 + 5, xPoint + 1, 
                                self.y2 - 5, fill = "black", width = 0)

class OnOffButton(MyButton):
    def __init__(self, x1, y1, x2, y2, state):
        super().__init__(self, x1, y1, x2, y2, "", 0)
        self.state = state
        
    def drawButton(self, app, canvas):
        onButton = app.loadImage('On Button.png')
        offButton = app.loadImage('Off Button.png')
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        if self.state == True:
            canvas.create_image(cx, cy, 
                        image=ImageTk.PhotoImage(onButton))
        else:
            canvas.create_image(cx, cy, 
                        image=ImageTk.PhotoImage(offButton))

            
            


    
    
