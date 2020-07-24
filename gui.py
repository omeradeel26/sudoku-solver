import pygame
from sudoku import *

pygame.init()

margin = 100
button_states = pygame.mouse.get_pressed()

screen =  pygame.display.set_mode((800,800))
pygame.display.set_caption("Sudoku")
running = True

icon = pygame.image.load('imgs/logo.png')
pygame.display.set_icon(icon)

def getLocation(loc):
    if loc[0] > margin and loc[0] < 800-margin and loc[1] > margin and lov[1] < 800-margin:
        row = (loc[0]-margin)//3
        col = (loc[1]-margin)//3
        return row, col


def drawGrid():
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
  #  for i in range (len(board[0])):
  #      for j in range (len(board)):
  #          text = font.render(board[i][j])
        
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False     
    screen.fill((255,255,255))
    drawGrid()
    if button_states[0] == 1:
        print("hello")
        print(getLocation(pygame.mouse.get_pos()))
