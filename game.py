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

COLOUR = (0,0,0) #colour of all borders and lines
SELECT_COL = (255,138,138) #color of selected box 

FPS = 30 #framerate
CLOCK = p.time.Clock() #set framerate function

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
        self.mouseactive = False #whether or not a square is selected (default = NONE)
        self.keyactive = False #whether or not a square is selected and key is pressed (default = NONE)
        self.info = '' #content within the square
        self.mistakes = 0 #number of mistakes made while playing
         
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

        increment_y = increment_x = MARGIN + SQ_SIZE//2 #starts from middle of first row 
        
        #DRAWING OUT NUMBERS
        for row in range(len(self.board)): #loops through all rows in board
            for col in range(len(self.board[0])): #loops through all columns in board
                if self.board[row][col] != 0: #if board does not contain 
                    text = FONT.render(str(self.board[row][col]), True, COLOUR) #renders number from array 
                    textRect = text.get_rect() #centers text 
                    textRect.center = (increment_x, increment_y)
                    SCREEN.blit(text, textRect)  #draws number in
                increment_x += SQ_SIZE # move over one square each time
            increment_x = MARGIN + SQ_SIZE//2 #set to default
            increment_y += SQ_SIZE #move one square down each row
        increment_y = MARGIN + SQ_SIZE//2  #set to defualt

    def FindLocation(self, mouseX, mouseY): #Find the location of the selected square
        self.Scol = int((mouseX-MARGIN) // SQ_SIZE) #column of selected square
        self.Srow = int((mouseY-MARGIN) // SQ_SIZE) #row of selected square
        self.location = (MARGIN + (self.Scol*int(SQ_SIZE)), MARGIN + (self.Srow*int(SQ_SIZE))) #gets location of square to place back again when square is selected
        if (mouseX > MARGIN) and (mouseX < SIZE - MARGIN) and (mouseY > MARGIN) and (mouseY < SIZE - MARGIN) and self.board[self.Srow][self.Scol] == 0: #makes sure that selected square is empty and within boundaries
            self.info = ''
            self.mouseactive = True #square is selected
        else: 
            del(self.Scol) #removes attributes b/c they are false
            del(self.Srow) 
            del(self.location)
            self.keyactive = False #makes sure that a key can not be placed
            self.mouseactive = False #makes sure square is not selected

    def DrawSelectedBox(self): #draws selected square to board
        p.draw.rect(SCREEN, SELECT_COL, (self.location[0], self.location[1], SQ_SIZE, SQ_SIZE), 4) #draws rectangle in position selected

    def DetectKeys(self, info): #function that detects valid key presses 
        if info.unicode in NUMBERS:  #Checks if user input is between 1 and 9
            self.keyactive =  True #then it will continously print the number in the main loop which is attached to function DrawNum
            self.info = info.unicode #sets info in selected square as follows    
        else: 
            self.keyactive = False #key is not active at the moment
            self.info = '' #information within key is reset

    def DrawNum(self): #function that draws in number if DetectKeys is true
        text = FONT.render(self.info, True, COLOUR) #renders number from array 
        textRect = text.get_rect() #centers text 
        textRect.center = (self.location[0] + SQ_SIZE//2, self.location[1] + SQ_SIZE//2) #Coordinates for text
        SCREEN.blit(text, textRect)  #draws number in

    def FinalizeKey(self, event): #function that checks whether or not ENTER is pressed and then validfies answer chooses to add to board or not
        if self.keyactive: #if 
            new = copy.deepcopy(self.board)
            if solve(new):
                self.board[self.Scol][self.Srow] = self.info
                self.mouseactive = False
                self.keyactive = False 
            else: 
                self.keyactive = False 
                self.info = ''  
        
def main(): #main function ran directly only from within this executed file
    running = True #var to control and run Pygame 
    sudoku = GameBoard() #instaciates GameBoard Class to Sudoku... assigns all attributes and methods

    while running: #loop function
        for event in p.event.get(): #gets all events in PyGame
            if event.type == p.QUIT: #if PyGame Window is shut
                running = False    #finish loop
            if event.type == p.MOUSEBUTTONDOWN: #if mouse is pressed record selected box location to sudoku
                mouseX, mouseY = p.mouse.get_pos() #get position of mouse
                sudoku.FindLocation(mouseX, mouseY) #find location of selected box 
            if event.type == p.KEYDOWN:
                if sudoku.mouseactive:
                    sudoku.DetectKeys(event)
                    
        SCREEN.fill((0,0,0)) # Fill the entire screen with black
        SCREEN.fill((255,255,255))
        sudoku.DrawBoard()
       
        if sudoku.mouseactive:
            sudoku.DrawSelectedBox()

        if sudoku.keyactive:
            sudoku.DrawNum()
    
        p.display.update()
        CLOCK.tick(FPS)

if __name__=="__main__":
    main()