import pygame
import math
from queue import PriorityQueue, Queue
import random

WIDTH = 1280
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path finding algorthm")

RED = (255, 0,0)
GREEN = (0, 255,0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255, 165, 0)
GREY = (128,128,128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BLACK
        self.neighbors = []
        self.wall_neighbors = []
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == WHITE
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def reset(self):
        self.color = BLACK 
        
    def make_start(self):
        self.color = ORANGE
        
    def make_closed(self):
        self.color = RED
        
    def make_open(self):
        self.color = GREEN
        
    def make_barrier(self):
        self.color = WHITE
        
    def make_end(self):
        self.color = TURQUOISE
        
    def make_path(self):
        self.color = PURPLE
        
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # Check down
            self.neighbors.append(grid[self.row + 1][self.col]) 
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # Check up
            self.neighbors.append(grid[self.row - 1][self.col]) 
            
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # Check left
            self.neighbors.append(grid[self.row][self.col - 1]) 
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # Check right
            self.neighbors.append(grid[self.row][self.col + 1])
        random.shuffle(self.neighbors)
        
    def update_wall_neighbors(self, grid):
        self.wall_neighbors = []
        if self.row < self.total_rows - 2 and not grid[self.row + 2][self.col].is_barrier(): # Check down
            self.wall_neighbors.append((grid[self.row + 1][self.col],grid[self.row + 2][self.col]))
            
        if self.row > 1 and not grid[self.row - 2][self.col].is_barrier(): # Check up
            self.wall_neighbors.append((grid[self.row-1][self.col], grid[self.row - 2][self.col]))
            
        if self.col > 1 and not grid[self.row][self.col - 2].is_barrier(): # Check left
            self.wall_neighbors.append((grid[self.row][self.col - 1],grid[self.row][self.col - 2]))
            
        if self.col < self.total_rows - 2 and not grid[self.row][self.col + 2].is_barrier(): # Check right
            self.wall_neighbors.append((grid[self.row][self.col + 1], grid[self.row][self.col + 2]))
        random.shuffle(self.wall_neighbors)
    
    def __lt__(self, other):
        return False
    

def h(p1, p2):# heuristic function
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

###################################################
# a star algorithm
def astar_algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True # make path
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) 
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    
        draw()
        
        if current != start:
            current.make_closed()
            
    return False

###################################################
# dfs algorithm
def dfs_algorithm(draw, grid, start, end):
    visited = set()
    came_from = {}
    stack = [start]
   
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        
        current = stack.pop()
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        if current not in visited:
            visited.add(current)
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)
                    came_from[neighbor] = current
                        
                    if neighbor != end and neighbor != start:
                        neighbor.make_open()
        draw()
        
        if current != start:
                current.make_closed()
        
    return False

# dfs maze generation
def dfs_maze_generation(draw, grid):
    visited = set()
    stack = [(None,grid[1][1])]
    
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = stack.pop()
        
        if current[1] not in visited:
            visited.add(current[1])
            if current[0] != None:
                current[0].reset()
            
            current[1].update_wall_neighbors(grid)
            for wall, neighbor in current[1].wall_neighbors:
                if neighbor not in visited:
                    stack.append((wall, neighbor))
        draw()

# bfs algorithm
def bfs_algorithm(draw, grid, start, end):
    visited = set()
    came_from = {}
    q = Queue()
    q.put(start)
    
    while not q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
        current = q.get()
        
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        if current not in visited:
            visited.add(current)
            
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    q.put(neighbor)
                    came_from[neighbor] = current
                    
                    if neighbor != end and neighbor != start:
                        neighbor.make_open()
                        
        draw()
        if current !=  start:
            current.make_closed()
        
    return False
###################################################

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
            
    return grid

def draw_grid(win, rows, width):
    gap = width // rows 
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
            
def draw_barrier(grid):
    i = j = 0
    for row in grid:
        if i % 2 == 0:
            for spot in row:
                spot.make_barrier()
        else:
            for spot in row:
                if j % 2 == 0:
                    spot.make_barrier()
                j += 1
        i += 1
            
def draw(win, grid, rows, width):
    win.fill('black')
    
    for row in grid:
        for spot in row:
            spot.draw(win)
            
    #draw_grid(win, rows, width)
    pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 64 # CHANGE THE SIZE OF THE MAP
    grid = make_grid(ROWS, WIDTH)
    
    start = None
    end = None
    
    run = True
    started = False
    
    draw_barrier(grid)
    while run:
            
            draw(WIN, grid, ROWS, WIDTH)
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if started:
                    continue
                    
                if pygame.mouse.get_pressed()[0]: # left mouse
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    #print(row, col)
                    if not spot.is_barrier():
                        if not start and spot != end:
                            start = spot
                            start.make_start()
                        elif not end and spot != start:
                            end = spot
                            end.make_end()
                        elif spot != end and spot != start:
                            spot.make_barrier()
                    
                elif pygame.mouse.get_pressed()[2]: # right mouse
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, width)
                    spot = grid[row][col]
                    
                    spot.reset()
                    if spot == start:
                        start = None
                    elif spot == end:
                        end = None
                    
                keys = pygame.key.get_pressed()
                
                # Press SPACE for maze generation
                if keys[pygame.K_SPACE]:
                    pygame.display.set_caption('Maze generating...')
                    if not start and not end:
                        # for row in grid:
                        #     for spot in row:
                        #         spot.update_wall_neighbors(grid)
                        
                        dfs_maze_generation(lambda: draw(win, grid, ROWS, width),
                                            grid)
                
                # Press B for bfs 
                if keys[pygame.K_b]:
                    pygame.display.set_caption('BFS')
                    if start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                                
                        bfs_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                            
                # Press D for dfs
                elif keys[pygame.K_d]:
                    pygame.display.set_caption('DFS')
                    if start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                                
                        dfs_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                        
                # Press A for a star
                elif keys[pygame.K_a]:
                    pygame.display.set_caption('A*')
                    if start and end:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                                
                        astar_algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                if keys[pygame.K_c]:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    draw_barrier(grid)
                
    pygame.quit()
    
if __name__=='__main__':
    main(WIN, WIDTH)