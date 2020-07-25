import random #module that generates random values

def generate():
    grid = [[0 for x in range(9)] for y in range(9)]  #generates 2D array with
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

def solve(grid):
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
