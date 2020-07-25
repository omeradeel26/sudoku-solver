import random #module that generates random values
import copy

def generate():
    grid = [[0 for x in range(9)] for y in range(9)]  #generates 2D array with empty values
    row = random.randrange(9) #generates random row index value between 0 and 8
    col = random.randrange(9) #generates random column index value between 0 and 8
    num = random.randrange(1,10) #generates random number to be placed in board between 0 and 9

    for i in range(20): #generates 20 numbers to base board... increment number to increase difficulty
        while not validify(grid, num, (row,col)) or grid[row][col] != 0: #new numbers generated fill an empty spot and fit sudoku rules
            row = random.randrange(9) #loops to create new values if reqs not met
            col = random.randrange(9)
            num = random.randrange(1,10)
        grid[row][col] = num #if reqs met, values are loaded to the board
    
    COPY = copy.deepcopy(grid)
    if not solve(COPY):
        grid = generate()

    return grid #return new board

def find_empty(grid): #find empty positions in board
    for i in range(len(grid)): #loops through row of board
        for j in range(len(grid[0])): #loops through columns
            if grid[i][j] == 0: #if empty spot found at index 
                return (i, j) #indexes returned (row, col)
    return False #no empty positions left

def validify(grid, num, loc): #function ensures SUDOKU rules are followed
    for i in range(len(grid[0])): #loops through row
        if num == grid[loc[0]][i]: 
            return False
    for i in range(len(grid[0])): #loops through column
        if num == grid[i][loc[1]]:
            return False 
    for i in range((loc[0]//3)*3,(loc[0]//3)*3 +3): #loops through grid
        for j in range((loc[1]//3)*3,(loc[1]//3)*3+3):
            if num == grid[i][j]:
                return False
    return True

def solve(grid): #function to solve the entire grid
    # doesnt find anything
    if not find_empty(grid):
        return True #if solution is done 
    else:
        position = find_empty(grid)#finds empty position (row, col)
        for i in range(1,10): #goes through combination of 9
            if validify(grid, i, position): #if the comgrid follows the rule in the empty location
                grid[position[0]][position[1]] = i  #new location becomes the number
                if solve(grid): #recurses through function (will return True if combo is done)
                    return True #if solution is done
                grid[position[0]][position[1]] = 0
    return False #ends if no possible combination