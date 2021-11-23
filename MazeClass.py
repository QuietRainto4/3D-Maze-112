import random, math
from cmu_112_graphics import*

# from 112 notes
def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

def print2dList(L):
    print(repr2dList(L))

def print3dList(L):
    for layer in L:
        print2dList(layer)

class Maze(object):
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.board = []
        for i in range(row * 2 + 1):
            self.board.append([0] * (col * 2 + 1))
        self.size = size
        self.map = {}
        self.allSets = []
        self.pointsToPath = {}
        self.numRow = 0
        self.insertWalls()
        # print2dList(self.board)
        self.convertToBoard()
    
    # Eller's method
    # https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm

    # a funciton to test all function in the maze
    def testGenerateMaze(self):
        self.firstRow()
        # print(self.allSets)
        self.joinAdjacentCells()
        # print(self.allSets)
        # print(self.map)
        self.increaseVertically()
        # print(self.allSets)
        # print(self.map)
        # each time after a row in finished, add to the map
        # the map maps a coordinate to all adjacent cells
        self.mapToBoard()
        # print2dList(self.board)
        self.addNewSets()
        # print(self.map)
        self.joinAdjacentCells()
        self.increaseVertically()
        self.addNewSets()
        self.joinAdjacentCells()
        self.increaseVertically()
        self.addNewSets()
        self.joinAdjacentCells()
        self.increaseVertically()
        self.addNewSets()
        self.lastRow()
        self.mapToBoard()
        # print2dList(self.board)
    
    # actually generate a maze
    def generateMaze(self):
        self.firstRow()
        # minus 1 because the first row is already made
        # and the last row is joined seperately
        for i in range(self.col - 1):
            self.joinAdjacentCells()
            self.increaseVertically()
            self.addNewSets()
        self.lastRow()
        self.mapToBoard()
        # print2dList(self.board)
    # at 11/15/2021 12:58 (now 59), I finished generating a layer of maze
    
    # insert walls of 1 in between the zeros
    # the one's are walls and the 0 are paths
    def insertWalls(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if i % 2 == 0:
                    self.board[i][j] = 1
                else:
                    if j % 2 == 0:
                        self.board[i][j] = 1

    # maps each possible point to the path that it actually is on the board
    def convertToBoard(self):
        for i in range(self.row):
            for j in range(self.col):
                self.pointsToPath[(i, j)] = (i * 2 + 1, j * 2 + 1)
        # print(self.pointsToPath)

    # converts the dictionary path to the board
    # makes the coordinates in between two points that are connected 0
    def mapToBoard(self):
        for coord in self.map:
            y1, x1 = coord
            for connected in self.map[coord]:
                y2, x2 = connected
                drow = y2 - y1
                dcol = x2 - x1
                newY, newX = self.pointsToPath[(y1, x1)]
                if drow > 0:
                    self.board[newY + 1][newX] = 0
                elif drow < 0:
                    self.board[newY - 1][newX] = 0
                if dcol > 0:
                    self.board[newY][newX + 1] = 0
                elif dcol < 0:
                    self.board[newY][newX - 1] = 0

    # initialize each column in row to be in their own set
    # put set in dictionary or list?
    def firstRow(self):
        for numCol in range(self.col):
            newSet = set()
            newSet.add((0, numCol))
            self.allSets.append(newSet)      
            # add the coordinate to the map
            self.map[(0, numCol)] = set()      

    # randomly join adjacent cells if they are not in the same set
    def joinAdjacentCells(self):
        for numCol in range(self.col - 1):
            shouldCombine = (
                random.randint(1, 2) <= 1)
            # from the future, why did I use b?
            b1 = (self.numRow, numCol)
            b2 = (self.numRow, numCol + 1)
            if shouldCombine and (not self.inSameSet(b1, b2)):
                # print(self.numRow, "combined")
                self.mergeSets(b1, b2)
        # print(self.map)
    
    # to merge a two sets horizontally
    def mergeSets(self, b1, b2):
        s1 = self.findSet(b1)
        s2 = self.findSet(b2)
        ns = self.combineSets(s1, s2)
        self.allSets.remove(s1)
        self.allSets.remove(s2)
        self.allSets.append(ns)
        # add to dictionary if they merged
        self.map[b1].add(b2)
        self.map[b2].add(b1)

    # find the set that the coordinate is in
    def findSet(self, coordinate):
        for theSets in self.allSets:
            if coordinate in theSets:
                return theSets

    # combines two sets
    def combineSets(self, s1, s2):
        for num in s2:
            s1.add(num)
        return s1

    # check if they are in the same set
    def inSameSet(self, s1, s2):
        for theSets in self.allSets:
            if s1 in theSets:
                if s2 in theSets:
                    return True
                return False

    # randomly add vertial coordinates to the new set
    def increaseVertically(self):
        for theSets in self.allSets:
            storage = set()
            count = 0
            # print("theSets:" + str(theSets))
            newPoints = self.numPointsNewRow(theSets)
            # print("newPoints: " + str(newPoints))
            for coordinates in theSets:
                y, x = coordinates
                # only loop through the coordinates that is in the same number of row
                if y == self.numRow:
                    shouldIncrease = random.randint(1, 3) <= 2
                    # if it is on the last point in the set and havent 
                    # increased yet, force it to increase
                    # if count == newPoints - 1:
                    #     shouldIncrease = True
                    if shouldIncrease:
                        y1, x1 = coordinates
                        newCoord = (y1 + 1, x1)
                        # first store all new sets to append later together
                        storage.add(newCoord)
                        # add to the dictionary
                        self.map[newCoord] = set()
                        self.map[coordinates].add(newCoord)
                        self.map[newCoord].add(coordinates)
                        #print(str(self.numRow) + " increased")
                    else:
                        count += 1
            # after looping through all the nodes in the set, 
            # find the node that has the least number of connections 
            # and increase that node vertically
            # 412-530-4700
            # print(self.map)
            # print(theSets)
            # print(f'numRow : {self.numRow}, count: {count}, newPoints: {newPoints}')
            # print(self.leastAdjacentNode(theSets))

            if count == newPoints:
                currCord = self.leastAdjacentNode(theSets)
                y1, x1 = currCord
                newCoord = (y1 + 1, x1)
                # first store all new sets to append later together
                storage.add(newCoord)
                # add to the dictionary
                self.map[newCoord] = set()
                self.map[currCord].add(newCoord)
                self.map[newCoord].add(currCord)
            

            theSets = self.combineSets(theSets, storage)
        # increase the row that we are on after increasing vertically
        self.numRow += 1

    # make the rest of the coordinates their own set
    # if they are not in a set already
    def addNewSets(self):
        for x in range(self.row):
            newSet = set()
            if (self.numRow, x) not in self.map:
                newSet.add((self.numRow, x))
                self.allSets.append(newSet)
                self.map[(self.numRow, x)] = set()
    
    # gets the number of points in the new row
    def numPointsNewRow(self, theSets):
        count = 0
        for coord in theSets:
            y, x = coord
            if self.numRow == y:
                count += 1
        return count

    # problem now
    # some lines simply will not increase vertically
    # should find the path that has the least adjacent nodes and force it to increase


    # returns the node in a set that has the least adjacent paths connected to it
    def leastAdjacentNode(self, theSet):
        bestNode = None
        bestConnections = 10
        for nodes in theSet:
            connections = len(self.map[nodes])
            y, x = nodes
            if y == self.numRow:
                if bestNode == None or connections < bestConnections:
                    bestNode = nodes
                    bestConnections = connections
        return bestNode

    # if reach the last row, join all remaining cells that does not share a set
    # by looping through all the points in the last row,
    # checks if they are in the same set, if not, combine them and make them connected
    def lastRow(self):
        for i in range(self.col - 1):
            n1 = (self.numRow, i)
            n2 = (self.numRow, i + 1)
            if not self.inSameSet(n1, n2):
                self.mergeSets(n1, n2)
    
    

# testMaze = Maze(10, 10, 100)
# testMaze.generateMaze()


# new problem to test the 3D maze
# how will I even know if the make is working
# should first make a backtracking to find the solution?
# otherwise can maybe try with a tini tiny maze, like 3 x 3 or 4 x 4

# the next line was the 250th code when I typed it, though now it is not
# the 250th line code reached on 11/15/2021, 12:45 AM CELEBRATION!
# though many ahem, majority of the lines are comments and spaces
# btw, adding random comments in the code is fun, and it makes it seem 
# like I did so much, when I did not


# note for 3D
# for board[k][j][i], k is the number of layer, j is the number of row
# i is the number of elements in the row
class threeDMaze(Maze):
    def __init__(self, row, col, height, size):
        self.row = row
        self.col = col
        self.height = height
        self.board = []
        for i in range(self.height * 2 + 1):
            store = []
            for j in range(self.row * 2 + 1):
                store.append([0] * (self.col * 2 + 1))
            self.board.append(store)
        self.size = size
        self.map = {}
        self.allSets = []
        self.pointsToPath = {}
        self.currHeight = 0
        self.insertWalls()
        # print3dList(self.board)
        self.convertToBoard()
    
    # function to test the functions in 3D maze
    def testGenerate3DMaze(self):
        self.firstStep()
        self.joinAdjacentCells()
        self.increaseVertically()
        self.mapToBoard()
        # print3dList(self.board)
        #self.convertToBoard()
    
    def generate3DMaze(self):
        self.firstStep()
        # minus 1 because the first row is already made
        # and the last row is joined seperately
        for i in range(self.height - 1):
            self.joinAdjacentCells()
            self.increaseVertically()
            self.addNewSets()
            self.removeRows()
        self.lastStep()
        self.mapToBoard()
        # print3dList(self.board)

    
    # create walls in between each coordinate in the board
    def insertWalls(self):
        for k in range(len(self.board)):
            for j in range(len(self.board[0])):
                for i in range(len(self.board[0][0])):
                    if k % 2 == 0:
                        self.board[i][j][k] = 1
                    else:
                        if j % 2 == 0:
                            self.board[i][j][k] = 1
                        else:
                            if i % 2 == 0:
                                self.board[i][j][k] = 1
    
    # for a coordinate, convert to the actual coordinate in 3D
    # k = height, j = row, i = col
    def convertToBoard(self):
        for k in range(self.height):
            for j in range(self.row):
                for i in range(self.col):
                    self.pointsToPath[(k, j, i)] = (
                                k * 2 + 1, j * 2 + 1, i * 2 + 1)
        # print(self.pointsToPath)

    # converts the dictionary path to the board
    # makes the coordinates in between two points that are connected 0
    def mapToBoard(self):
        for coord in self.map:
            z1, y1, x1 = coord
            for connected in self.map[coord]:
                # print(self.map)
                # print(connected)
                z2, y2, x2 = connected
                drow = y2 - y1
                dcol = x2 - x1
                dheight = z2 - z1
                newZ, newY, newX = self.pointsToPath[(z1, y1, x1)]
                if drow > 0:
                    self.board[newZ][newY + 1][newX] = 0
                elif drow < 0:
                    self.board[newZ][newY - 1][newX] = 0
                if dcol > 0:
                    self.board[newZ][newY][newX + 1] = 0
                elif dcol < 0:
                    self.board[newZ][newY][newX - 1] = 0
                if dheight > 0:
                    self.board[newZ + 1][newY][newX] = 0
                elif dheight < 0:
                    self.board[newZ - 1][newY][newX] = 0
    
    # makes each coordinate in the board a set of itself
    def firstStep(self):
        for numRow in range(self.row):
            for numCol in range(self.col):
                newSet = set()
                newSet.add((0, numRow, numCol))
                self.allSets.append(newSet)      
                # add the coordinate to the map
                self.map[(0, numRow, numCol)] = set() 
    
    # randomly joins adjacent cells on the first layer on the board
    # needs to join randomally in all four directions on the layer
    def joinAdjacentCells(self):
        for numRow in range(self.row):
            for numCol in range(self.col):
                for moves in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    drow, dcol = moves
                    shouldCombine = random.randint(1, 4) <= 1
                    newRow = numRow + drow
                    newCol = numCol + dcol
                    if (newRow >= 0 and newRow < self.row and
                        newCol >= 0 and newCol < self.row):
                        b1 = (self.currHeight, numRow, numCol)
                        b2 = (self.currHeight, newRow, newCol)
                        if shouldCombine and (not self.inSameSet(b1, b2)):
                            # print(self.numRow, "combined")
                            self.mergeSets(b1, b2)
        # print(self.map)
    
    # randomly add vertial coordinates to the new set
    def increaseVertically(self):
        for theSets in self.allSets:
            storage = set()
            count = 0
            # print("theSets:" + str(theSets))
            newPoints = self.numPointsNewRow(theSets)
            # print("newPoints: " + str(newPoints))
            for coordinates in theSets:
                z, y, x = coordinates
                # only loop through the coordinates that is in the same number of row
                if z == self.currHeight:
                    shouldIncrease = random.randint(1, 4) <= 1
                    # if it is on the last point in the set and havent 
                    # increased yet, force it to increase
                    # if count == newPoints - 1:
                    #     shouldIncrease = True
                    if shouldIncrease:
                        z1, y1, x1 = coordinates
                        newCoord = (z1 + 1, y1, x1)
                        # first store all new sets to append later together
                        storage.add(newCoord)
                        # add to the dictionary
                        self.map[newCoord] = set()
                        self.map[coordinates].add(newCoord)
                        self.map[newCoord].add(coordinates)
                        #print(str(self.numRow) + " increased")
                    else:
                        count += 1
            # after looping through all the nodes in the set, 
            # find the node that has the least number of connections 
            # and increase that node vertically
            if count == newPoints:
                currCord = self.leastAdjacentNode(theSets)
                z1, y1, x1 = currCord
                newCoord = (z1 + 1, y1, x1)
                # first store all new sets to append later together
                storage.add(newCoord)
                # add to the dictionary
                self.map[newCoord] = set()
                self.map[currCord].add(newCoord)
                self.map[newCoord].add(currCord)
            theSets = self.combineSets(theSets, storage)
        # increase the height that we are on after increasing vertically
        self.currHeight += 1

        # returns the node in a set that has the least adjacent paths connected to it
    def leastAdjacentNode(self, theSet):
        bestNode = None
        # 6 is the hightest number of possible connections for a node
        bestConnections = 6
        for nodes in theSet:
            connections = len(self.map[nodes])
            z, y, x = nodes
            if z == self.currHeight:
                if bestNode == None or connections < bestConnections:
                    bestNode = nodes
                    bestConnections = connections
        return bestNode
    
    # gets the number of points in the new row
    def numPointsNewRow(self, theSets):
        count = 0
        for coord in theSets:
            z, y, x = coord
            if self.currHeight == z:
                count += 1
        return count
    
    # if reach the last layer, join all remaining cells that does not share a set
    # def lastStep(self):
    #     for numRow in range(self.row):
    #         for numCol in range(self.col):
    #             for moves in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    #                 drow, dcol = moves
    #                 newRow = numRow + drow
    #                 newCol = numCol + dcol
    #                 if (newRow >= 0 and newRow < self.row and
    #                     newCol >= 0 and newCol < self.row):
    #                     n1 = (self.currHeight, numRow, numCol)
    #                     n2 = (self.currHeight, newRow, newCol)
    #                     if not self.inSameSet(n1, n2):
    #                         self.mergeSets(n1, n2)

    def lastStep(self):
        store = []
        for numRow in range(self.row):
            for numCol in range(self.col):
                store.append((numRow, numCol))
        for num in range(len(store)):
            randomCoord = random.randint(0, len(store) - 1)
            currRow, currCol = store[randomCoord]
            for moves in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                drow, dcol = moves
                newRow = currRow + drow
                newCol = currCol + dcol
                if (newRow >= 0 and newRow < self.row and
                    newCol >= 0 and newCol < self.row):
                    n1 = (self.currHeight, currRow, currCol)
                    n2 = (self.currHeight, newRow, newCol)
                    if not self.inSameSet(n1, n2):
                        self.mergeSets(n1, n2)
            store.pop(randomCoord)
    
    # make the rest of the coordinates their own set
    # if they are not in a set already
    def addNewSets(self):
        for numRow in range(self.row):
            for numCol in range(self.col):
                newSet = set()
                if (self.currHeight, numRow, numCol) not in self.map:
                    newSet.add((self.currHeight, numRow, numCol))
                    self.allSets.append(newSet)
                    self.map[(self.currHeight, numRow, numCol)] = set()
                    
    # removes coordinates for rows after used
    def removeRows(self):
        for theSets in self.allSets:
            store = []
            for coord in theSets:
                z, y, x, = coord
                if z == self.currHeight - 1:
                    store.append(coord)
            for elem in store:
                theSets.remove(elem)

test3DMaze = threeDMaze(2, 2, 2, 100)
test3DMaze.generate3DMaze()