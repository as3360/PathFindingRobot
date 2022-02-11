import numpy as np
from tkinter import *
import tkinter as tk
import math


class Grid:

    # Initializing
    def __init__(self, cols, rows, x1, y1, x2, y2):
        self.cols = cols
        self.rows = rows
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.root = Tk()
        self.gridCanv = Canvas(self.root, width=3000, height=3000)
        self.vertices = [[0] * (rows + 1) for _ in range(cols + 1)]
        self.cells = []
        self.ended = Vertex(0, 0, 0)

    # def showValues(self, x, y):

    def lineOfSightThetaStar(self, par, ver):
        x0 = int(par.x / 10)
        y0 = int(par.y / 10)
        x1 = int(ver.x / 10)
        y1 = int(ver.y / 10)
        f = 0
        dy = y1 - y0
        dx = x1 - x0
        sy = 1
        sx = 1
        if dy < 0:
            dy = -dy
            sy = -1
        if dx < 0:
            dx = -dx
            sx = -1
        if dx > dy:
            while x0 != x1:
                f += dy
                if f >= dx:
                    checkCellx = int(x0 + ((sx - 1) / 2))
                    checkCelly = int(y0 + ((sy - 1) / 2))
                    if self.inValidVert(checkCellx, checkCelly):
                        return False
                    y0 += sy
                    f -= dx
                if f != 0:
                    checkCellx = int(x0 + ((sx - 1) / 2))
                    checkCelly = int(y0 + ((sy - 1) / 2))
                    if self.inValidVert(checkCellx, checkCelly):
                        return False
                if dy == 0:
                    checkCellx = int(x0 + ((sx - 1) / 2))

                    if self.inValidVert(checkCellx, y0) and self.inValidVert(checkCellx, y0 - 1):
                        return False
                x0 += sx
        else:
            while y0 != y1:
                f += dx
                if f >= dy:
                    checkCellx = int(x0 + ((sx - 1) / 2))
                    checkCelly = int(y0 + ((sy - 1) / 2))
                    if self.inValidVert(checkCellx, checkCelly):
                        return False
                    x0 += sx
                    f -= dy
                if f != 0:
                    checkCellx = int(x0 + ((sx - 1) / 2))
                    checkCelly = int(y0 + ((sy - 1) / 2))
                    if self.inValidVert(checkCellx, checkCelly):
                        return False
                if dy == 0:

                    checkCelly = int(y0 + ((sy - 1) / 2))
                    if self.inValidVert(x0, checkCelly) and self.inValidVert(x0 - 1, checkCelly):
                        return False
                y0 += sy
        return True

    def updateVertThetaStar(self, v1, v2, fringe):
        if self.lineOfSightThetaStar(v1.parentPath, v2):
            pot_g = v1.parentPath.g + self.distance(v2,v1.parentPath)
            if v2.g > pot_g:
                v2.g = pot_g
                if v2.h == 99999999:
                    v2.h = self.thetaStarHeur(v2.x, v2.y)
                    v2.f = self.f(v2)
                    v2.parentPath = v1.parentPath
                    fringe.insert(v2)
                else:
                    v2.f = self.f(v2)
                    v2.parentPath = v1.parentPath
                    fringe.sift_up(v2.heapInd)
        else:
            pot_g = v1.g + self.distance(v2,v1)
            if v2.g > pot_g:
                v2.g = pot_g
                v2.parentPath = v1
                if v2.h == 99999999:
                    v2.h = self.thetaStarHeur(v2.x, v2.y)
                    v2.f = self.f(v2)
                    fringe.insert(v2)
                else:
                    v2.f = self.f(v2)
                    fringe.sift_up(v2.heapInd)

    def inValidVert(self, x, y):
        leftCorner = True
        if (y > 1):
            leftCorner = self.vertices[x - 1][y - 2].cellFill
        if leftCorner == True:
            return False
        return True

    def thetaStarHeur(self, vx, vy):
        return ((vx - self.x2) ** 2 + (vy - self.y2) ** 2) ** (1 / 2)

    def visitorsA_star(self, vert):
        # returns a list of valid vertices to visit with edges from your current vertex for Astar
        res = []
        xx = int(vert.x / 10)
        yy = int(vert.y / 10)
        filled = [1, 1, 1, 1]
        if (xx > 1 and yy > 1):
            filled[0] = self.vertices[xx - 2][yy - 2].cellFill
        if (yy > 1 and xx < self.cols + 1):
            filled[1] = self.vertices[xx - 1][yy - 2].cellFill
        if (xx > 1 and yy < self.rows + 1):
            filled[2] = self.vertices[xx - 2][yy - 1].cellFill
        if (xx < self.cols + 1 and yy < self.rows + 1):
            filled[3] = self.vertices[xx - 1][yy - 1].cellFill

        if (yy > 1 and (filled[0] == 0 or filled[1] == 0)):
            # northern vertex
            temp = self.vertices[xx - 1][yy - 2]
            res.append(temp)
            if (xx < self.cols):
                if (filled[1] == 0):
                    # northeast vertex
                    temp2 = self.vertices[xx][yy - 2]
                    res.append(temp2)
            if (xx > 1):
                if (filled[0] == 0):
                    # northwest vertex
                    temp3 = self.vertices[xx - 2][yy - 2]
                    res.append((temp3))
        if (xx > 1 and (filled[0] == 0 or filled[2] == 0)):
            # west vertex
            temp = self.vertices[xx - 2][yy - 1]
            res.append(temp)
        if (xx <= self.cols and (filled[1] == 0 or filled[3] == 0)):
            # east vertex
            temp = self.vertices[xx][yy - 1]
            res.append(temp)
            if (yy <= self.rows):
                if (filled[3] == 0):
                    # southeast vertex
                    temp2 = self.vertices[xx][yy]
                    res.append(temp2)
        if (yy <= self.rows and (filled[2] == 0 or filled[3] == 0)):
            # south vertex
            temp = self.vertices[xx - 1][yy]
            res.append(temp)
            if (xx > 1):
                if (filled[2] == 0):
                    # southwest vertex
                    temp2 = self.vertices[xx - 2][yy]
                    res.append(temp2)

        return res

    def getReady(self):
        vs = self.vertices[int(self.x1 / 10 - 1)][int(self.y1 / 10 - 1)]
        vg = self.vertices[int(self.x2 / 10 - 1)][int(self.y2 / 10 - 1)]
        validPath = self.bfs(vs, vg)
        if validPath:
            return True
        else:
            print("No path is possible")
            return False

    def bfs(self, start, goal):
        queue = []
        for v in self.visitorsA_star(start):
            queue.append(v)
        visited = {start}
        while len(queue) > 0:
            temp = queue.pop()
            if temp.x == goal.x and temp.y == goal.y:
                return True
            for v in self.visitorsA_star(temp):
                if (v in visited):
                    pass
                else:
                    visited.add(v)
                    queue.append(v)
        return False

    def updateVertexAStar(self, s, sPrime, fringe):
        potential_g = self.g(s, sPrime)
        if potential_g < s.g:
            s.g = potential_g
            if (s.h == 99999999):
                s.h = self.aStarHeur(s.x, s.y)
                s.f = self.f(s)
                s.parentPath = sPrime
                fringe.insert(s)
            else:
                s.f = self.f(s)
                s.parentPath = sPrime
                fringe.sift_up(s.heapInd)

    def visAStar(self, ver):
        while (ver.parentPath != ver):
            self.addLine(ver, ver.parentPath)
            ver = ver.parentPath

    def visThetaStar(self, ver):
        while (ver.parentPath != ver):
            self.addLine(ver, ver.parentPath)
            ver = ver.parentPath

    def thetaStar(self):
        # Start vertex
        vs = self.vertices[int(self.x1 / 10) - 1][int(self.y1 / 10) - 1]
        # Goal Vertex
        vg = self.vertices[int(self.x2 / 10) - 1][int(self.y2 / 10) - 1]

        vs.g = 0
        vs.parentPath = vs
        vs.h = self.thetaStarHeur(vs.x, vs.y)
        vs.f = self.f(vs)

        VertHeap = VertMinHeap()
        VertHeap.insert(vs)
        # Jon look at the line below
        cl = {0}
        while VertHeap.isNotEmpty():
            s = VertHeap.popMin()
            if s.x == vg.x and s.y == vg.y:
                return s
            cl.add(s)
            neighbors = self.visitorsA_star(s)
            for v in neighbors:
                if (v in cl):
                    pass
                else:
                    self.updateVertThetaStar(s, v, VertHeap)
        return None

    def runThetaStar(self):
        result = self.thetaStar()
        if result == None:
            print("No path found :( ur gonna have to hop some filled cells")
        else:
            self.visThetaStar(result)

    def aStar(self):
        # Start vertex
        vs = self.vertices[int(self.x1 / 10) - 1][int(self.y1 / 10) - 1]
        # Goal Vertex
        vg = self.vertices[int(self.x2 / 10) - 1][int(self.y2 / 10) - 1]

        # Actual A* Algorithm
        vs.g = 0
        vs.parentPath = vs
        vs.h = self.aStarHeur(vs.x, vs.y)
        vs.f = self.f(vs)

        VertHeap = VertMinHeap()
        VertHeap.insert(vs)
        # Jon look at the line below
        cl = {0}
        while VertHeap.isNotEmpty():
            s = VertHeap.popMin()
            if s.x == vg.x and s.y == vg.y:
                return s
            cl.add(s)
            neighbors = self.visitorsA_star(s)
            for v in neighbors:
                if (v in cl):
                    pass
                else:
                    self.updateVertexAStar(v, s, VertHeap)
        return None

    def runAStar(self):
        result = self.aStar()
        if result == None:
            print("No path found :( ur gonna have to hop some filled cells")
        else:
            self.visAStar(result)

    def aStarHeur(self, vx, vy):
        return (np.sqrt(2) - 1) * min(abs(vx - self.x2), abs(vy - self.y2)) + max(abs(vx - self.x2), abs(vy - self.y2))

    def makeCell(self, v1x, v1y, fill):
        temp = Cell(v1x, v1y, fill)
        self.cells.append(temp)

    def g(self, vChild, vParent):
        return vParent.g + self.distance(vParent, vChild)

    def f(self, vert):
        return vert.g + vert.h

    # Makes a singular vertex
    def makeVertices(self, x, y, fill):
        temp = Vertex(x, y, fill)
        self.vertices[int(x / 10) - 1][int(y / 10) - 1] = temp

    # Distance between two vertices
    def distance(self, v1, v2):
        return np.sqrt((v2.y - v1.y) ** 2 + (v2.x - v1.x) ** 2)

    def prep(self):
        self.gridCanv.pack()

    # Plot each individual cell
    def plot_cell(self, cell):
        x0 = cell.v1.x
        y0 = cell.v1.y

        x1 = cell.v4.x

        y1 = cell.v4.y

        fillMark = '#fff'
        if (cell.isFilled):
            fillMark = '#000000'

        self.gridCanv.create_rectangle(x0, y0, x1, y1, fill=fillMark)
        self.root.update()

    # Detecting the start vertex
    def emphasizeStart(self, x, y):
        self.gridCanv.create_oval(x - 6, y - 6, x + 6, y + 6, fill='green')

    # Detecting the goal vertex
    def emphasizeGoal(self, x, y):
        self.gridCanv.create_oval(x - 6, y - 6, x + 6, y + 6, fill='blue')

    # Drawing line in A* Algorithm
    def addLine(self, vert1, vert2):
        x0 = vert1.x
        y0 = vert1.y
        x1 = vert2.x
        y1 = vert2.y

        self.gridCanv.create_line(x0, y0, x1, y1, fill='red', width=2)

    def findVertexVal(self, col, row):
        width = 300
        height = 300

        x = 1125
        y = 450
        self.gridCanv.create_rectangle(x, y, x+width, y+height, fill='#ADD8E6')

        label1 = tk.Label(self.root, text='Find the f,g,h Values!')
        label1.config(font=('helvetica', 14))
        self.gridCanv.create_window(1275, 470, window=label1)

        label2 = tk.Label(self.root, text='Type the Column #')
        label2.config(font=('helvetica', 10))
        self.gridCanv.create_window(1275, 500, window=label2)

        entry1 = tk.Entry(self.root)
        self.gridCanv.create_window(1275, 530, window=entry1)

        label3 = tk.Label(self.root, text='Type the Row #')
        label3.config(font=('helvetica', 10))
        self.gridCanv.create_window(1275, 560, window=label3)

        entry2 = tk.Entry(self.root)
        self.gridCanv.create_window(1275, 590, window=entry2)

        def getSquareRoot():
            x1 = entry1.get()
            y1 = entry2.get()

            x_int = int(x1)
            y_int = int(y1)

            if self.vertices[x_int - 1][y_int - 1].f == 99999999:
                label11 = tk.Label(self.root, text='Vertex was never reached!', font=('helvetica', 10, 'bold'))
                self.gridCanv.create_window(1275, 650, window=label11)
            else:
                label4 = tk.Label(self.root, text='The Values of this Vertex are', font=('helvetica', 10))
                self.gridCanv.create_window(1275, 650, window=label4)

                label5 = tk.Label(self.root, text='f value = ', font=('helvetica', 10, 'bold'))
                self.gridCanv.create_window(1220, 680, window=label5)

                label6 = tk.Label(self.root, text=self.vertices[x_int - 1][y_int - 1].f, font=('helvetica', 10, 'bold'))
                self.gridCanv.create_window(1310, 680, window=label6)

                label7 = tk.Label(self.root, text='g value = ', font=('helvetica', 10, 'bold'))
                self.gridCanv.create_window(1220, 700, window=label7)

                label8 = tk.Label(self.root, text=self.vertices[x_int - 1][y_int - 1].g, font=('helvetica', 10, 'bold'))
                self.gridCanv.create_window(1310, 700, window=label8)

                label9 = tk.Label(self.root, text='h value = ', font=('helvetica', 10, 'bold'))
                self.gridCanv.create_window(1220, 720, window=label9)

                label10 = tk.Label(self.root, text=self.vertices[x_int - 1][y_int - 1].h,
                                   font=('helvetica', 10, 'bold'))
                self.gridCanv.create_window(1310, 720, window=label10)

        button1 = tk.Button(text='Find the Values!', command=getSquareRoot, bg='brown', fg='white',
                            font=('helvetica', 9, 'bold'))
        self.gridCanv.create_window(1275, 620, window=button1)

    def out(self):
        self.root.mainloop()

    def fin(self):
        self.root.update()


# Cell Object
class Cell():
    def __init__(self, v1x, v1y, fill):
        self.v1 = Vertex(v1x, v1y, fill)
        self.isFilled = fill
        self.v2 = Vertex(v1x + 10, v1y, fill)
        self.v3 = Vertex(v1x, v1y + 10, fill)
        self.v4 = Vertex(v1x + 10, v1y + 10, fill)


# Vertex Object
class Vertex:
    def __init__(self, x, y, fill):
        self.x = x
        self.y = y
        self.cellFill = fill
        self.parentPath = None
        self.g = 99999999
        self.h = 99999999
        self.f = 99999999
        self.heapInd = -1


class VertMinHeap:
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0

    def sift_up(self, i):
        while math.floor(i / 2) > 0:
            if self.heap_list[i].f < self.heap_list[int(math.floor(i / 2))].f:
                a = self.heap_list[i].heapInd
                b = self.heap_list[int(math.floor(i / 2))].heapInd
                self.heap_list[i], self.heap_list[int(math.floor(i / 2))] = self.heap_list[int(math.floor(i / 2))], self.heap_list[i]
                self.heap_list[i].heapInd = a
                self.heap_list[int(math.floor(i / 2))].heapInd = b
            i = math.floor(i/2)

    def insert(self, k):
        self.heap_list.append(k)

        self.current_size += 1

        k.heapInd = self.current_size

        self.sift_up(self.current_size)

    def isNotEmpty(self):
        return (self.current_size > 0)

    def sift_down(self, i):
        while (i * 2) <= self.current_size:
            lc = self.low_child(i)
            if self.heap_list[i].f > self.heap_list[lc].f:
                a = self.heap_list[i].heapInd
                b = self.heap_list[lc].heapInd
                self.heap_list[i], self.heap_list[lc] = self.heap_list[lc], self.heap_list[i]
                self.heap_list[i].heapInd = a
                self.heap_list[lc].heapInd = b
            i = lc

    def low_child(self, i):
        if (i * 2) + 1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i * 2].f < self.heap_list[(i * 2) + 1].f:
                return i * 2
            else:
                return (i * 2) + 1

    def popMin(self):
        if len(self.heap_list) == 1:
            return 'Empty heap'

        root = self.heap_list[1]

        self.heap_list[1] = self.heap_list[self.current_size]
        self.heap_list[1].heapInd = 1

        self.heap_list.pop(self.current_size)

        self.current_size -= 1

        self.sift_down(1)

        return root


def main():
    lines = []

    fileName = input("Please input the name of your text file: ")
    file = open(fileName, 'r')

    aort = input("Please write A for A* or T for Theta*: ")

    for line in file:
        lines.append(line)

    start_coord = lines[0].split()
    end_coord = lines[1].split()
    x1temp = int(start_coord[0]) * 10
    y1temp = int(start_coord[1]) * 10
    x2temp = int(end_coord[0]) * 10
    y2temp = int(end_coord[1]) * 10

    row_col = lines[2].split()
    colstemp = int(row_col[0])
    rowstemp = int(row_col[1])

    grid = Grid(colstemp, rowstemp, x1temp, y1temp, x2temp, y2temp)

    for i in range(3, len(lines)):
        use = lines[i].split()
        x = int(use[0]) * 10
        y = int(use[1]) * 10
        fill = int(use[2])
        grid.makeVertices(x, y, fill)

    lc = grid.cols
    lr = grid.rows

    for i in range(1, int(lr) + 2):
        grid.makeVertices(10 * lc + 10, i * 10, 0)

    for i in range(1, int(lc) + 2):
        grid.makeVertices(i * 10, 10 * lr + 10, 0)

    for v in grid.vertices:
        for ver in v:
            if (ver.x <= grid.cols * 10 and ver.y <= grid.rows * 10):
                grid.makeCell(ver.x, ver.y, ver.cellFill)

    for c in grid.cells:
        grid.plot_cell(c)

    grid.emphasizeGoal(grid.x2, grid.y2)
    grid.emphasizeStart(grid.x1, grid.y1)
    go = grid.getReady()
    grid.findVertexVal(colstemp, rowstemp)

    if aort == 'A':
        if(go):
            grid.runAStar()
        else:
            label3 = tk.Label(grid.gridCanv, text='No Path Found!', font=('helvetica', 30))
            grid.gridCanv.create_window(500, 700, window=label3)

    if aort == 'T':
        if(go):
            grid.runThetaStar()
        else:
            label3 = tk.Label(grid.gridCanv, text='No Path Found!', font=('helvetica', 30))
            grid.gridCanv.create_window(500, 700, window=label3)


    tx = " "

    if aort != 'T' and aort != 'A':
        tx = 'Invalid Input!'
    label3 = tk.Label(grid.gridCanv, text=tx, font=('helvetica', 30))
    grid.gridCanv.create_window(500, 700, window=label3)


    grid.prep()
    grid.out()


main()
