import pygame
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
CELL_SIZE = 25
N_COLS = SCREEN_WIDTH // CELL_SIZE
N_ROWS = SCREEN_HEIGHT // CELL_SIZE

COLORS = {
    "BLACK":  ( 0,   0,   0   ),
    "WHITE":  ( 255, 255, 255 ),
    "RED":    ( 212, 57,  57  ),
    "PURPLE": ( 124, 57, 212  )
}

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Generator")

CLOCK = pygame.time.Clock()
FPS = 60

def index(i, j):
    return i * N_ROWS + j

class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True] # top, right, bottom, left
        self.visited = False

    def show(self):
        x, y = self.i * CELL_SIZE, self.j * CELL_SIZE

        # draw fill color if cell is visited
        if self.visited:
            pygame.draw.rect(SCREEN, COLORS["PURPLE"], (x, y, CELL_SIZE, CELL_SIZE))

        # draw cell walls
        if self.walls[0]:
            pygame.draw.line(SCREEN, COLORS["WHITE"], (x, y), (x + CELL_SIZE, y), 2)
        if self.walls[1]:
            pygame.draw.line(SCREEN, COLORS["WHITE"], (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[2]:
            pygame.draw.line(SCREEN, COLORS["WHITE"], (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls[3]:
            pygame.draw.line(SCREEN, COLORS["WHITE"], (x, y), (x, y + CELL_SIZE), 2)

class MazeGrid:
    def __init__(self):
        self.cells = []
        self.stack = []
        self.finished = False

        # initialize grid of cells
        for i in range(N_COLS):
            for j in range(N_ROWS):
                self.cells.append(Cell(i,j))

        # set top left cell as visited and add to stack
        self.cells[0].visited = True
        self.stack.append(self.cells[0])

    def show(self):
        for cell in self.cells:
            cell.show()

    def update(self):
        self.show()
        if len(self.stack) > 0:
            cell = self.stack.pop()
            nextCell = self.checkCellNeighbors(cell.i, cell.j)
            if nextCell != None:
                self.stack.append(cell)
                self.removeWalls(cell, nextCell)
                nextCell.visited = True
                self.stack.append(nextCell)
            
            # mark the current cell with a red color
            pygame.draw.rect(SCREEN, COLORS["RED"], (cell.i * CELL_SIZE, cell.j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        else:
            self.finished = True
    
    def checkCellNeighbors(self, i, j):
        unvisited = []
        if j - 1 >= 0 and j - 1 < N_ROWS:
            top = self.cells[index(i, j - 1)]
            if not top.visited:
                unvisited.append(top)
        if i + 1 >= 0 and i + 1 < N_COLS:
            right = self.cells[index(i + 1, j)]
            if not right.visited:
                unvisited.append(right)
        if j + 1 >= 0 and j + 1 < N_ROWS:
            bottom = self.cells[index(i, j + 1)]
            if not bottom.visited:
                unvisited.append(bottom)
        if i - 1 >= 0 and i - 1 < N_COLS:
            left = self.cells[index(i - 1, j)]
            if not left.visited:
                unvisited.append(left)
        
        if len(unvisited) > 0:
            return random.choice(unvisited)
        else:
            return None
    
    def removeWalls(self, a, b):
        if a.i - b.i == 1:
            a.walls[3] = False
            b.walls[1] = False
        elif a.i - b.i == -1:
            a.walls[1] = False
            b.walls[3] = False
        if a.j - b.j == 1:
            a.walls[0] = False
            b.walls[2] = False
        elif a.j - b.j == -1:
            a.walls[2] = False
            b.walls[0] = False




if __name__ == "__main__":
    maze = MazeGrid()

    run = True
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
        
        # do maze generation algorithm here
        if not maze.finished:
            maze.update()
        else:
            SCREEN.fill(COLORS["BLACK"])
            maze = MazeGrid()

        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()
