board = [[5,3,0,0,7,0,0,0,0],
         [6,0,0,1,9,5,0,0,0],
         [0,9,8,0,0,0,0,6,0],
         [8,0,0,0,6,0,0,0,3],
         [4,0,0,8,0,3,0,0,1],
         [7,0,0,0,2,0,0,0,6],
         [0,6,0,0,0,0,2,8,0],
         [0,0,0,4,1,9,0,0,5],
         [0,0,0,0,8,0,0,7,9]]

def print_out(bo):
    for i in range(len(bo)): 
        for j in range(len(bo[0])):
            if j%3 ==  0 and j != 0: 
                print("| ", end="")

            if i%3 == 0 and i != 0 and j == 0:
                print("---------------------")

            print(bo[i][j],end=" ")

            if j == len(bo[0])-1:
                print('')

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)
    return False


def validify(bo, num, loc):
    for i in range(len(bo[0])):
        if num == bo[loc[0]][i]:
            return False
    for i in range(len(bo[0])):
        if num == bo[i][loc[1]]:
            return False 
    for i in range((loc[0]//3)*3,(loc[0]//3)*3 +3):
        for j in range((loc[1]//3)*3,(loc[1]//3)*3+3):
            if num == bo[i][j]:
                return False
    return True

def recurse(bo):
    # doesnt find anything
    if not find_empty(bo):
        return True #if solution is done 
    else:
        position = find_empty(bo)#finds empty position (row, col)
        for i in range(1,10): #goes through combination of 9
            if validify(bo, i, position): #if the combo follows the rule in the empty location
                bo[position[0]][position[1]] = i  #new location becomes the number
                if recurse(bo): #recurses through function (will return True if combo is done)
                    return True #if solution is done
                bo[position[0]][position[1]] = 0
    return False #ends if no possible combination


if recurse(board):
    print_out(board)
else:
    print("no viable solution")