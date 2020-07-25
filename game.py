import pygame as p #import pygame... allows us to create GUI
import copy #import copy... allows for hardcopying variables
from solver import solve, generate #import solve function and generating board function

WIDTH = HEIGHT = 800 #set height and width 
MARGIN = 100 #margin around board

ROWS = 9 #num of rows
COLS = 9 #num of columns

SQ_WIDTH = (WIDTH - MARGIN*2)//ROWS #WIDTH of one square 
SQ_HEIGTH = (WIDTH - MARGIN*2)//ROWS #Height of one squre

SCREEN =  p.display.set_mode((WIDTH,HEIGHT))
ICON = p.image.load('imgs/logo.png')

p.display.set_caption("Sudoku")
p.display.set_icon(ICON)

FONT = pygame.font.SysFont("calibri", 35)

running = True

class game:
    def __init__(self):
        pass

p.init()

allnum = ["1","2","3","4","5","6","7","8","9"]

def getLocation(loc, grid):
    if loc[0] > margin and loc[0] < 800-margin and loc[1] > margin and loc[1] < 800-margin:
        col = (loc[0]-margin)//((800-(margin*2))//9)
        row = (loc[1]-margin)//((800-(margin*2))//9)
        if grid[row][col] == 0:
            return row, col
        return False
    return False

def drawGrid(grid):
    incr = margin

    for i in range(4):
       pygame.draw.line(screen, (0,0,0),(margin,incr),(800-margin,incr), 3)
       pygame.draw.line(screen, (0,0,0), (incr,margin),(incr,800-margin), 3)
       incr += (800-margin*2)//3
    
    incr = margin

    for i in range(1,7):
        if i == 3 or i==5:
            incr += ((800-margin*2)//9)*2
        else: 
            incr += (800-margin*2)//9
        pygame.draw.line(screen, (0,0,0),(margin,incr),(800-margin,incr))
        pygame.draw.line(screen, (0,0,0),(incr,margin),(incr,800-margin))

    incr_x = margin + (800-margin*2)//18
    incr_y = margin + (800-margin*2)//18

    for i in range (len(grid)):
        for j in range (len(grid[0])):
            if grid[i][j] != 0:
                text = font.render(str(board[i][j]), True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (incr_x, incr_y)
                screen.blit(text, textRect)
            incr_x += (800-margin*2)//9
        incr_x = margin + (800-margin*2)//18
        incr_y += (800-margin*2)//9
    incr_y = margin + (800-margin*2)//18   

class EmptyBox:
    def __init__(self, row, col, num):
        self.num = ''
        self.location = (margin + (row*((800-margin*2)//9)) + (800-margin*2)//18, margin + (col*((800-margin*2)//9)) + (800-margin*2)//18)
        self.active = True

    def placement(self, num):
        if self.active and num in allnum:
            print(self.location[0],(self.location[1]))
            self.num = num
            text = font.render(num, True, (0, 0, 0))
            screen.blit(text,(self.location[0],self.location[1]))
        else: 
            active = False

board = generate()
new = copy.deepcopy(board)

while not solve(new): 
    board = generate()
    new = copy.deepcopy(board)  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if getLocation(pygame.mouse.get_pos(),board) != False:
               rowg, colg = getLocation(pygame.mouse.get_pos(),board)
               filled = EmptyBox(rowg, colg, board[rowg][colg])  
        if event.type == pygame.KEYDOWN:
            if event.key == 'K_BACKSPACE':
                filled.num = ''
            else:
               filled.placement(event.unicode)

    screen.fill((255,255,255))
    drawGrid(board)
    pygame.display.flip()