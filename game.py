import pygame as p #import pygame... allows us to create GUI
import copy #import copy... allows for hardcopying variables
from solver import solve, generate, validify, find_empty #import from solver file
import time #creates delay in code at the end

GameScreen = "HOME" #starting screen

SIZE = 700 #set height and width 
MARGIN = 75 #margin around board

mins = 0 #global vars for time so that when Timer function is called var is not reset
seconds = 0  

run = True #controls end screen delay
cont = True #controls whether or not timer is ran

SQUARES = 9 #num of squares per side
SECTION = SQUARES//3 #num of sections per side

SECTION_SIZE = (SIZE - MARGIN * 2)/ SECTION #WIDTH of one section
SQ_SIZE = (SIZE - MARGIN*2)/ SQUARES #WIDTH of one square 

NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] #possible values

COLOUR = (0,0,0) #colour of all borders and lines
SELECT_COL = (255,138,138) #color of selected box 
BUTTON_COL = (144,238, 144) #color of box on home screen (Green)
SBUTTON_COL = (51,165,50) #color of box when hovering on home screen (dark green)
BACKGROUND_COL = (255,255,255) #color of background 

FPS = 30 #framerate
CLOCK = p.time.Clock() #set framerate function

p.init() #initilizes GUI

SCREEN =  p.display.set_mode((SIZE, SIZE)) #initializes screen
ICON = p.image.load('imgs/logo.png') #loads logo for game

p.display.set_caption("Sudoku") #sets screen title 
p.display.set_icon(ICON) #sets logo for game

FONTSIZE = int((SIZE - MARGIN*2) *0.06)
LOWERFONTSIZE = int(FONTSIZE*0.75)

FONT = p.font.SysFont("calibri", FONTSIZE) #imports font & fontsize used for game
LOWERFONT = p.font.SysFont("calibri", LOWERFONTSIZE) #imports font & fontsize used for game
 
class GameBoard: #Gameboard class for the board
    def __init__(self): #initializes attributes of board
        self.board = generate() #randomizes board
        self.mouseactive = False #whether or not a square is selected (default = NONE)
        self.keyactive = False #whether or not a square is selected and key is pressed (default = NONE)
        self.info = '' #content within the square
        self.mistakes = 0 #number of mistakes made while playing
      #  self.run = True #ran when the screen size is changed
         
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

        text = FONT.render("Press spacebar to solve", True, COLOUR) #renders number from array 
        SCREEN.blit(text, (MARGIN, SIZE*0.05))  #draws number in

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
        elif info.key == 13 and self.info in NUMBERS: #if user presses enter and fixes bug where person can press enter before finalizing key
            self.FinalizeKey(info) #check function to see if answer is correct
        else: 
            self.keyactive = False #key is not active at the moment
            self.info = '' #information within key is reset

    def DrawNum(self): #function that draws in number if DetectKeys is true
        text = FONT.render(self.info, True, COLOUR) #renders number from array 
        textRect = text.get_rect() #centers text 
        textRect.center = (self.location[0] + SQ_SIZE//2, self.location[1] + SQ_SIZE//2) #Coordinates for text
        SCREEN.blit(text, textRect)  #draws number in

    def FinalizeKey(self, event): #function that checks whether or not ENTER is pressed and then validfies answer chooses to add to board or not
        new = copy.deepcopy(self.board) #creates dummy array to test whether or not user input can be solved
        new[self.Srow][self.Scol] = int(self.info) #adds user input to dummy array
        if validify(self.board, int(self.info), (self.Srow, self.Scol)) and solve(new): #follows rules of sudoku
            self.board[self.Srow][self.Scol] = int(self.info) #adds the value to the board to be drawn in 
            self.mouseactive = False #resets variables
            self.keyactive = False 
            self.info = ''
        else:
            self.mistakes +=1 #adds number of mistakes
            self.keyactive = False #resets variables
            self.mouseactive = False 
            self.info = ''
    
    def DrawMistakes(self):
        compound = "Mistakes: " + str(self.mistakes) #makes word using # of mistakes attribute
        text = LOWERFONT.render(compound, True, COLOUR) #renders words from array 
        textRect = text.get_rect() #centers text 
        textRect.center = (SIZE//7.5, SIZE - (MARGIN//2)) #Coordinates for text
        SCREEN.blit(text, (MARGIN, SIZE*0.925))  #draws number in

class EndScreen():
    def __init__(self):
        self.sizeX = SIZE*0.4 #dimensions of button
        self.buttonX = SIZE//2 - self.sizeX//2
        self.sizeY = SIZE*0.1
        self.buttonY = SIZE*0.6 - self.sizeY//2 
        self.maintext = p.font.SysFont("Calibri", int(self.sizeX*0.4)) #size of text used
        self.smalltext = p.font.SysFont("Calibri", int(self.sizeX*0.1)) #size of text used
        self.buttontext = p.font.SysFont("Calibri", int(self.sizeX*0.075), 1.5) #size of text used
        self.active = False #whether or not button is hovered
    def DrawOver(self, mistakes):
        #draw title in
        text = self.maintext.render("GAME OVER!", True, COLOUR) #renders words from array 
        textRect = text.get_rect() #centers text 
        textRect.center = (SIZE//2, SIZE*0.35) #Coordinates for text
        SCREEN.blit(text, textRect)  #draws number in

        compound = "You finished with " + str(mistakes) + " mistakes and in the time " + str(mins).zfill(2) + ":" + str(seconds).zfill(2) 
        text = FONT.render(compound, True, COLOUR) #renders words from array 
        textRect = text.get_rect() #centers text 
        textRect.center = (SIZE//2, SIZE//2) #Coordinates for text
        SCREEN.blit(text, textRect)  #draws number in

        self.Button() 

        text = self.buttontext.render("Generate New Board!", True, (255,255,255)) #renders words from array 
        textRect = text.get_rect() #centers text 
        textRect.center = (SIZE//2, SIZE*0.6) #Coordinates for text
        SCREEN.blit(text, textRect)  #draws number in

    def Button(self):
        self.mouseX = p.mouse.get_pos()[0]
        self.mouseY = p.mouse.get_pos()[1]
        if (self.buttonX + self.sizeX) > self.mouseX  > self.buttonX and (self.buttonY + self.sizeY) > self.mouseY  > self.buttonY:
            p.draw.rect(SCREEN, SBUTTON_COL, (self.buttonX, self.buttonY, self.sizeX, self.sizeY))
            self.active = True #button is hovered
        else:
            p.draw.rect(SCREEN, BUTTON_COL, (self.buttonX, self.buttonY, self.sizeX, self.sizeY))   
            self.active = False #button is hovered     

class HomeScreen:
    def __init__(self):
        self.sizeX = SIZE*0.4 #dimensions of button
        self.buttonX = SIZE//2 - self.sizeX//2
        self.sizeY = SIZE*0.1
        self.buttonY = SIZE*0.6 - self.sizeY//2 
        self.maintext = p.font.SysFont("Calibri", int(self.sizeX*0.5)) #size of text used
        self.smalltext = p.font.SysFont("Calibri", int(self.sizeX*0.1)) #size of text used
        self.buttontext = p.font.SysFont("Calibri", int(self.sizeX*0.12), 1.5) #size of text used
        self.active = False #whether or not button is hovered

    def DrawHome(self):
        #draw title in
        text = self.maintext.render("Sudoku", True, COLOUR) #renders words from array 
        textRect = text.get_rect() #centers text 
        textRect.center = (SIZE//2, SIZE*0.45) #Coordinates for text
        SCREEN.blit(text, textRect)  #draws number in

        #draw name in 
        text = self.smalltext.render("Created by Omer Adeel", True, COLOUR) #renders words from array 
        SCREEN.blit(text, (SIZE*0.025, SIZE*0.925))  #draws number in

        #button function
        self.Button() 

        #draw button text 
        text = self.buttontext.render("Generate Board!", True, (255,255,255)) #renders words from array 
        textRect = text.get_rect() #centers text 
        textRect.center = (SIZE//2, SIZE*0.6) #Coordinates for text
        SCREEN.blit(text, textRect)  #draws number in
    
    def Button(self):
        self.mouseX = p.mouse.get_pos()[0]
        self.mouseY = p.mouse.get_pos()[1]
        if (self.buttonX + self.sizeX) > self.mouseX  > self.buttonX and (self.buttonY + self.sizeY) > self.mouseY  > self.buttonY:
            p.draw.rect(SCREEN, SBUTTON_COL, (self.buttonX, self.buttonY, self.sizeX, self.sizeY))
            self.active = True #button is hovered
        else:
            p.draw.rect(SCREEN, BUTTON_COL, (self.buttonX, self.buttonY, self.sizeX, self.sizeY))   
            self.active = False #button is hovered     
def Timer():
    global mins, seconds
    SECOND = int((p.time.get_ticks() - start_ticks)/1000) #running clock of application
    if cont:
        mins = SECOND//60 #minuites
        seconds = SECOND - mins*60 #seconds
        if seconds == 60: #resets seconds to zero
            seconds = 0

        compound =  "Timer: " + str(mins).zfill(2) + ":" + str(seconds).zfill(2)   #format word as a clock
        text = LOWERFONT.render(compound, True, COLOUR) #renders word
        SCREEN.blit(text, (SIZE - MARGIN - SIZE*0.17, SIZE*0.925))  #draws timer in
        
def main(screen): #main function ran directly only from within this executed file
    global run, start_ticks
    running = True #var to control and run Pygame 
    sudoku = GameBoard() #instaciates GameBoard Class to Sudoku... assigns all attributes and methods
    home = HomeScreen() #instaciates home Class to Sudoku... assigns all attributes and methods
    end = EndScreen() #instaciates done Class to Sudoku... assigns all attributes and methods

    while running: #loop function    
        if screen == "END":
            for event in p.event.get(): #gets all events in PyGame
                if event.type == p.QUIT: #if PyGame Window is shut
                    running = False    #finish loop
                if event.type == p.MOUSEBUTTONDOWN:
                    if end.active: 
                        start_ticks += p.time.get_ticks()  
                        sudoku = GameBoard()                  
                        screen = "PLAY"
            if run: #add start function delay to show finished board
                time.sleep(3) #show for 3 seconds 
            SCREEN.fill(BACKGROUND_COL) #fill screen white
            end.DrawOver(sudoku.mistakes)  #text for screen
            run = False #makes sure that function is not ran again

        if screen == "PLAY":
            for event in p.event.get(): #gets all events in PyGame
                if event.type == p.QUIT: #if PyGame Window is shut
                    running = False    #finish loop
                if event.type == p.MOUSEBUTTONDOWN: #if mouse is pressed record selected box location to sudoku
                    mouseX, mouseY = p.mouse.get_pos() #get position of mouse
                    sudoku.FindLocation(mouseX, mouseY) #find location of selected box 
                if event.type == p.KEYDOWN:
                    if sudoku.mouseactive:
                        sudoku.DetectKeys(event)
                    if event.key == p.K_SPACE:
                        solve(sudoku.board) #solve the board                   
                        cont = False #stops the clock
            SCREEN.fill(BACKGROUND_COL) #white background
            Timer() #keeps track of time
            sudoku.DrawBoard() #Draw new board
            sudoku.DrawMistakes() #Draw # of mistakes

            if not find_empty(sudoku.board):
                screen = "END" 
                sudoku.mouseactive = False
                        
            if sudoku.mouseactive: #if the mouse is selected
                sudoku.DrawSelectedBox() #draw red box function

            if sudoku.keyactive: #if the keyboard is active draw the number on screen
                sudoku.DrawNum()  

        if screen == "HOME":
            for event in p.event.get(): #gets all events in PyGame
                if event.type == p.QUIT: #if PyGame Window is shut
                    running = False # break loop
                if event.type == p.MOUSEBUTTONDOWN:
                    if home.active:    
                        cont = True                 
                        start_ticks = p.time.get_ticks() #gets starting ticks unntil next event
                        screen = "PLAY"
            SCREEN.fill(BACKGROUND_COL)
            home.DrawHome()

        p.display.update() #updates screen
        CLOCK.tick(FPS) #framerate of application

if __name__=="__main__": #executes main function if python file is ran directly
    main(GameScreen)