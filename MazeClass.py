import random

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

    def ellerGenerateMaze(self):
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
        self.mapToBoard()
        print2dList(self.board)
    
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
            shouldCombine = random.randint(1, 2) <= 2
            b1 = (self.numRow, numCol)
            b2 = (self.numRow, numCol + 1)
            if shouldCombine and (not self.inSameSet(b1, b2)):
                print(self.numRow, "combined")
                s1 = self.findSet(b1)
                s2 = self.findSet(b2)
                ns = self.combineSets(s1, s2)
                self.allSets.remove(s1)
                self.allSets.remove(s2)
                self.allSets.append(ns)
                # add to dictionary if they merged
                self.map[b1].add(b2)
                self.map[b2].add(b1)
        print(self.map)
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
        count = 0
        for theSets in self.allSets:
            storage = set()
            for coordinates in theSets:
                shouldIncrease = random.randint(1, 2) == 1
                # if it is on the last point in the set and havent 
                # increased yet, force it to increase
                if count == len(theSets) - 1:
                    shouldIncrease = True
                if len(theSets) == 1 or shouldIncrease:
                    y1, x1 = coordinates
                    newCoord = (y1 + 1, x1)
                    # first store all new sets to append later together
                    storage.add(newCoord)
                    # add to the dictionary
                    self.map[newCoord] = set()
                    self.map[coordinates].add(newCoord)
                    self.map[newCoord].add(coordinates)
                else:
                    count += 1
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

    # if reach the last row, join all remaining cells that does not share a set


testMaze = Maze(5, 5, 100)
testMaze.ellerGenerateMaze()
