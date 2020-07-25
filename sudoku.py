import random
import pygame
import copy

pygame.init()

margin = 100

rowg = False
colg = False

screen =  pygame.display.set_mode((800,800))
pygame.display.set_caption("Sudoku")
running = True

icon = pygame.image.load('imgs/logo.png')
pygame.display.set_icon(icon)

font = pygame.font.SysFont("comicsansms", 35)

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

def random_generate():
    grid = [[0 for x in range(9)] for y in range(9)]
    row = random.randrange(9)
    col = random.randrange(9)
    num = random.randrange(1,10)
    for i in range(20): 
        while not validify(grid,num, (row,col)) or grid[row][col] != 0:
            row = random.randrange(9)
            col = random.randrange(9)
            num = random.randrange(1,10)
        grid[row][col] = num
    return grid

def print_out(grid):
    for i in range(len(grid)): 
        for j in range(len(grid[0])):
            if j%3 ==  0 and j != 0: 
                print("| ", end="")

            if i%3 == 0 and i != 0 and j == 0:
                print("---------------------")

            print(grid[i][j],end=" ")

            if j == len(grid[0])-1:
                print('')

def find_empty(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                return (i, j)
    return False


def validify(grid, num, loc):
    for i in range(len(grid[0])):
        if num == grid[loc[0]][i]:
            return False
    for i in range(len(grid[0])):
        if num == grid[i][loc[1]]:
            return False 
    for i in range((loc[0]//3)*3,(loc[0]//3)*3 +3):
        for j in range((loc[1]//3)*3,(loc[1]//3)*3+3):
            if num == grid[i][j]:
                return False
    return True

def recurse(grid):
    # doesnt find anything
    if not find_empty(grid):
        return True #if solution is done 
    else:
        position = find_empty(grid)#finds empty position (row, col)
        for i in range(1,10): #goes through combination of 9
            if validify(grid, i, position): #if the comgrid follows the rule in the empty location
                grid[position[0]][position[1]] = i  #new location becomes the number
                if recurse(grid): #recurses through function (will return True if combo is done)
                    return True #if solution is done
                grid[position[0]][position[1]] = 0
    return False #ends if no possible combination

class EmptyBox:
    margin = 100
    def __init__(self, row, col, num):
        self.num = num
        self.location = ((row+margin)*(800+(margin//2)*9) + (800-margin*2)//18, (col+margin)*(800+(margin//2)*9) + (800-margin*2)//18)

    def placement(self):
        newnum = font.render("10", True, (0, 0, 0))
        newnumRect = newnum.get_rect()
        newnumRect.center = (incr_x, incr_y)
        screen.blit(newnum, newnumRect)

class Num:
    def __init__(self, row, col, num):

    def addNumber(self, selection):
        self.selection = selection
        if self.selection:

class grid:
    def __init__(self, margin, num_grid, direct, size):
        self.margin = margin
        self.margin = num_grid 
        self.direct = direct
        self.size = size
    
    def createSpacing(self):
        
        

board= random_generate()
new = copy.deepcopy(board)

while not recurse(new): 
    board = random_generate()
    new = copy.deepcopy(board)    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if getLocation(pygame.mouse.get_pos(),board) != False:
               rowg, colg = getLocation(pygame.mouse.get_pos(),board)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                input_info(board,rowg,colg,"1")
                print(rowg,colg)
            elif event.key == pygame.K_2:
                input_info(board,rowg,colg,"2")
            elif event.key == pygame.K_3:
                input_info(board,rowg,colg,"3")
            elif event.key == pygame.K_4:
                input_info(board,rowg,colg,"4")
            elif event.key == pygame.K_5:
                input_info(board,rowg,colg,"5")
            elif event.key == pygame.K_6:
                input_info(board,rowg,colg,"6")
            elif event.key == pygame.K_7:
                input_info(board,rowg,colg,"7")
            elif event.key == pygame.K_8:
                input_info(board,rowg,colg,"8")
            elif event.key == pygame.K_9:
                input_info(board,rowg,colg,"9")

    screen.fill((255,255,255))
    drawGrid(board)