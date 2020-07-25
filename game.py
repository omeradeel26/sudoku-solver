import pygame as p #import pygame... allows us to create GUI
import copy #import copy... allows for hardcopying variables
from solver import solve, generate #import solve function and generating board function

SIZE = 800 #set height and width 
MARGIN = 75 #margin around board

SQUARES = 9 #num of squares per side
SECTION = SQUARES//3 #num of sections per side

SECTION_SIZE = (SIZE - MARGIN * 2)/ SECTION #WIDTH of one section
SQ_SIZE = (SIZE - MARGIN*2)/ SQUARES #WIDTH of one square 

NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
COLOUR = (0,0,0)

CLOCK = p.time.Clock() #set framerate
p.init() #initilizes GUI

SCREEN =  p.display.set_mode((SIZE, SIZE)) #initializes screen
ICON = p.image.load('imgs/logo.png') #loads logo for game

p.display.set_caption("Sudoku") #sets screen title 
p.display.set_icon(ICON) #sets logo for game

FONTSIZE = int((SIZE - MARGIN*2) *0.06)
FONT = p.font.SysFont("calibri", FONTSIZE) #imports font & fontsize used for game
 
class GameBoard: #Gameboard class for the board
    def __init__(self): #initializes attributes of board
        self.board = generate() #randomizes board
        self.active = False #whether or not a square is selected (default = NONE)
         
    def DrawBoard(self): #draws out board
        #DRAWING OUTLINE OF SECTIONS
        increment = MARGIN #increment by size of one square each time
        for i in range(SECTION + 1): #times to add a solid border for sections
           p.draw.line(SCREEN, COLOUR, (MARGIN, increment), (SIZE - MARGIN, increment), 3) #draw horizontal line
           p.draw.line(SCREEN, COLOUR, (increment, MARGIN),(increment, SIZE - MARGIN), 3) #draw vertical line
           increment += SECTION_SIZE #increase size of incrememnt each time
        
        #DRAWING OUTLINE FOR SQUARES
        increment = MARGIN #starts off halfway in first square
        for i in range(SQUARES + 1):
            p.draw.line(SCREEN, COLOUR, (MARGIN, increment), (SIZE - MARGIN, increment)) #draw horizontal line
            p.draw.line(SCREEN, COLOUR, (increment, MARGIN),(increment, SIZE - MARGIN)) #draw vertical line
            increment += SQ_SIZE #increase size of incrememnt each time

        increment_y = increment_x = MARGIN + SQ_SIZE//2 
        
        #DRAWING OUT NUMBERS
        for row in range(len(self.board)): #loops through all rows in board
            for col in range(len(self.board[0])): #loops through all columns in board
                if self.board[row][col] != 0: #if board does not contain 
                    text = FONT.render(str(self.board[row][col]), True, COLOUR)
                    textRect = text.get_rect()
                    textRect.center = (increment_x, increment_y)
                    SCREEN.blit(text, textRect)                
                increment_x += SQ_SIZE
            increment_x = MARGIN + SQ_SIZE//2 
            increment_y += SQ_SIZE
        increment_y = MARGIN + SQ_SIZE//2  

    def FindLocation(self, mouseX, mouseY):
        self.Scol = (mouseY-MARGIN) // int(SQ_SIZE)
        self.Srow = (mouseX-MARGIN) // int(SQ_SIZE)
        self.location = (MARGIN + (self.Srow*int(SQ_SIZE)), MARGIN + (self.Scol*int(SQ_SIZE)))
        if (mouseX > MARGIN) and (mouseX < SIZE - MARGIN) and mouseY > MARGIN and (mouseY < SIZE - MARGIN) and self.board[self.Scol][self.Srow] == 0:
            self.active = True #square is selected
            return self.Srow, self.Scol
        else: 
            del(self.Scol) #removes attributes b/c they are false
            del(self.Srow)
            del(self.location)
            self.active = False #makes sure square is not selected
            return False

    def DrawSelectedBox(self):
        p.draw.rect(SCREEN, COLOUR, (self.location[0], self.location[1], SQ_SIZE, SQ_SIZE))
       # p.draw.rect(SCREEN, COLOUR, [self.location[0], self.location[1], SQ_SIZE, SQ_SIZE])
        
def main():
    running = True #var to control and run Pygame 
    sudoku = GameBoard() #instaciates GameBoard Class to Sudoku... assigns all attributes and methods

    while running: #loop function
        for event in p.event.get(): #gets all events in PyGame
            if event.type == p.QUIT: #if PyGame Window is shut
                running = False    #finish loop
            if event.type == p.MOUSEBUTTONDOWN: #if mouse is pressed record selected box location to sudoku
                mouseX = p.mouse.get_pos()[0] #get mouseX location
                mouseY = p.mouse.get_pos()[1] #get mouseY location
                sudoku.FindLocation(mouseX, mouseY) #find location of selected box 
            if event.type == p.KEYDOWN:
                if sudoku.FindLocation != False:
                    pass
            
            if sudoku.active:
                sudoku.DrawSelectedBox()
                p.display.flip()
                print("hello")
        #     if event.key == 'K_BACKSPACE':
        #         filled.num = ''
        #     else:
            #       filled.placement(event.unicode)
        SCREEN.fill((255,255,255))
        sudoku.DrawBoard()
        p.display.flip()
        #CLOCK.tick(30)

if __name__=="__main__":
    main()