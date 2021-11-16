class Block(object):
    def __init__(self, size):
        self.size = size

class Wall(Block):
    pass

class Path(Block):
    def __init__(self, size, left, right, front, back):
        super.__init__(self, size)
        # self.up = up
        # self.down = down
        self.left = left
        self.right = right
        self.front = front 
        self.back = back

    


    

