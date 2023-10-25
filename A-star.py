#!usr/bin/python3
#Sheeven Jean
#CSCI 4350
#Proj1

import sys, random, copy, heapq, time
start_time = time.time()
nodeid = 0

#Node class
class node():
    def __init__(self, current_state, n, d):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.board = current_state
        self.prev = None
        self.depth = d
        self.fn = Heuristic(self.board.tiles, n) + self.depth
    def __str__(self):
        return 'Node: id=%d '%(self.id) + PrintMatrix(self.board.tiles)

#class for the different states of the board
class state():
    def __init__(self, matrix, x, y):
        self.xpos = x
        self.ypos = y
        self.tiles = matrix
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def copy(self):
        s = copy.deepcopy(self)
        return s
    
#class for the frontier
class PriorityQueue():
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.fn, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)
    
def main():
    #arguments check
    if (len(sys.argv) != 2):
        print()
        print("Usage: %s [Heuristic]" %(sys.argv[0]))
        print()
        sys.exit(1)    
    #variable declarations
    goal = [[0,1,2],[3,4,5],[6,7,8]]
    matrix = [[0 for x in range(3)] for y in range(3)]
    n= int(sys.argv[1])
    x=0
    y=0
    row=0
    for line in sys.stdin:
        col=0
        for i in line.split():
            matrix[row][col] = int(i)
            if(matrix[row][col] == 0):
                x = row
                y = col
            col+=1
        row+=1
        if(row>=3):
            break;
    #Initial Search Tree
    initial = state(matrix, x, y)
    root = node(initial, n, 1)
    frontier = PriorityQueue()
    frontier.push(root)
    lst = []
    #A-star
    visited =  0
    #loop
    while(not frontier.isEmpty()):
        curr = frontier.pop()
        visited+=1
        if(curr.board.tiles == goal):
            break
        lst.append(curr.board.tiles)
        #expand potential children
        upstate = curr.board.up()
        downstate = curr.board.down()
        leftstate = curr.board.left()
        rightstate = curr.board.right()
        if(upstate and upstate.tiles not in lst):
            moveup = node(upstate, n, curr.depth+1)
            moveup.prev = curr
            frontier.push(moveup)
        if(downstate and downstate.tiles not in lst):
            movedown = node(downstate, n, curr.depth+1)
            movedown.prev = curr
            frontier.push(movedown)
        if(leftstate and leftstate.tiles not in lst):
            moveleft = node(leftstate, n, curr.depth+1)
            moveleft.prev = curr
            frontier.push(moveleft)
        if(rightstate and rightstate.tiles not in lst):
            moveright = node (rightstate, n, curr.depth+1)
            moveright.prev = curr
            frontier.push(moveright)
    
    #Data
    print("V = ", visited)
    print("N = ", expanded := frontier.length() + len(lst))
    print("d = ", d := curr.depth)
    print("b = ", b := visited **(1./d))
    out = []
    while(curr != None):
        out.append(curr.board.tiles)
        curr = curr.prev
    for x in range(d-1, -1, -1):
        PrintMatrix(out[x])
        print()

#Print the current board
def PrintMatrix(matrix):
    for x in matrix:
        for y in x:
            print(y, end=" ")
        print()

#determine which heuristic to use
def Heuristic(matrix, n):
    if(n ==0):
        return 0
    if(n == 1):
        return NumTiles(matrix)
    elif(n == 2):
        return Distance(matrix)
    elif(n == 3):
        return MyHeuristic(matrix)
        #return NumTiles(matrix) + Distance(matrix)
 
#Calculate the amount of misplaced tiles in each row and column
def MyHeuristic(matrix):
    r=0
    num=0
    for x in matrix:
        c=0
        for y in x:
            if(y==1 and ((r==1 and c==1) or (r==0 and c==2))):
                if(r > 0 and matrix[r-1][c]==4):
                    num+=2
                elif(matrix[r][c-1]==2):
                    num+=2
            elif(y==2 and (r==1 and c==2)):
                if(matrix[r-1][c]==5):
                    num+=2
            elif(y==3 and ((r==2 and c==0) or (r==1 and c==1))):
                if(matrix[r-1][c]==6):
                    num+=2
                elif(c > 0 and matrix[r][c-1]==4):
                    num+=2
            elif(y==4 and (r==2 and c==1)):
                if(matrix[r-1][c] == 7):
                    num+=2
            elif(y==5 and ((r==2 and c==2) or (r==1 and c==1))):
                if(matrix[r-1][c] == 8):
                    num+=2
                elif( c==1 and matrix[r][c+1] == 4):
                    num+=2
            elif(y==6 and (r==1 and c==1)):
                if(matrix[r][c-1] == 7):
                    num+=2
            elif(y==7 and (r==2 and c==2)):
                if(matrix[r][c-1]==8):
                    num+=2
            c+=1
        r+=1
    return (num + Distance(matrix))
#calculate the number of misplace tiles on the board
def NumTiles(matrix):
    r=0
    num=0
    for x in matrix:
        c=0
        for y in x:
            if(y==1 and (r!=0 or c!=1)):
                num+=1
            elif(y==2 and (r!=0 or c!=2)):
                num+=1
            elif(y==3 and (r!=1 or c!=0)):
                num+=1
            elif(y==4 and (r!=1 or c!=1)):
                num+=1
            elif(y==5 and (r!=1 or c!=2)):
                num+=1
            elif(y==6 and (r!=2 or c!=0)):
                num+=1
            elif(y==7 and (r!=2 or c!=1)):
                num+=1
            elif(y==8 and (r!=2 or c!=2)):
                num+=1
            c+=1
        r+=1
    return num

#calculate the Manhattan distance
def Distance(matrix):
    d = 0
    for i in range(3):
        for j in range(3):
            if(matrix[i][j]==1):
                y = j - 1
                d+= abs(y) + i
            elif(matrix[i][j]==2):
                y = j - 2
                d+= abs(y) + i
            elif(matrix[i][j]==3):
                x= i - 1
                d+= abs(x) + j
            elif(matrix[i][j]==4):
                x= i - 1
                y= j - 1
                d+= abs(x) + abs(y)
            elif(matrix[i][j]==5):
                x= i-1
                y = j -2
                d+= abs(x) + abs(y)
            elif(matrix[i][j]==6):
                x = i-2
                d+= abs(x) + j
            elif(matrix[i][j]==7):
                x = i-2
                y = j-1
                d+= abs(x) + abs(y)
            elif(matrix[i][j]==8):
                x= i-2
                y= j-2
                d+= abs(x) + abs(y)
    return d

main()
print("--- %s seconds ---" % (time.time() - start_time))
