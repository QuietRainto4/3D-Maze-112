from cmu_112_graphics import*

class MyButton(App):
    def __init__(self, x1, y1, x2, y2, text):
        self.corners = (x1, y1, x2, y2)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.text = text
        self.pressed = False
    
    def inRectangle(self, x, y):
        if (x > self.x1 and x < self.x2 and 
            y > self.y1 and y < self.y2):
            return True
        return False
    
    def drawButton(self,canvas, app):
        canvas.create_rectangle(self.corners, fill = "white",
                                width = 5)
    
    
class CommandBar(MyButton):
    def __init__(self, x1, y1, x2, y2):
        super.__init__(x1, y1, x2, y2)
        self.text = ""
        self.type = False

    def keyPressed(self, app, event):
        if (self.type and event.key.isalnum() and len(event.key) == 1):
            self.text += event.key

            
            


    
    
