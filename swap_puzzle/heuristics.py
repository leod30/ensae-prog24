from math import factorial

def Manhattan_distance_cell_by_cell(grid):
    """This functions calculates the Manhattan distance from the grid in grid.state to the grid 1,...,mn, cell by cell"""
    dist = 0
    for number in range(1,grid.m*grid.n+1): # We add all the distances of all the numbers
        # We find the coordinates of number in the grid.state grid
        for i in range(grid.m):
            if number in grid.state[i]:
                line1 = i
        for j in range(grid.n):
            if number == grid.state[line1][j]:
                column1 = j
        
        # We find the desired coordinates of number
        line2, column2 = number // grid.n, number % grid.n
        
        # We add this to the distance
        dist += abs(line1-line2) + abs(column1-column2)
        
    return dist

def Manhattan_distance_max(grid):
    """This functions calculates the Manhattan distance from the grid in grid.state to the grid 1,...,mn, but keeps the max"""
    max = 0
    for number in range(1,grid.m*grid.n+1): # We add all the distances of all the numbers
        # We find the coordinates of number in the grid.state grid
        for i in range(grid.m):
            if number in grid.state[i]:
                line1 = i
        for j in range(grid.n):
            if number == grid.state[line1][j]:
                column1 = j
        
        # We find the desired coordinates of number
        line2, column2 = number // grid.n, number % grid.n
        if max < abs(line1-line2) + abs(column1-column2):
            max = abs(line1-line2) + abs(column1-column2)
        
    return max

def Manhattan_distance(grid):
    """This functions calculates the Manhattan distance from the grid in grid.state to the grid 1,...,mn, with the distance from the norm 1"""
    dist = 0
    index = 1
    for number in range(1,grid.m*grid.n+1): # We add all the distances of all the numbers
        dist += abs(number-index)
        index+=1
        
    return dist

def hash(grid):
    list = []
    for i in range(grid.m): #We transform the grid into a list
        for j in range(grid.n):
            list.append(grid.state[i][j])

    T = [False for i in range(grid.m*grid.n+1)] #List whe T[i] indicates if whether or not i has been assigned
    S = 0   #The hash number that we are going to create
    for i in range(1, grid.m*grid.n+1): #We procede cell by cell
        x = list[i-1]   #We recreate the coefficient multiplied by (mn-i) in the hash, that is (x-1-d) : x-1 because we know that the first (mn-1)! starts by 1 (so it starts by (mn-1)!*0=(mn-1)!*(1-1)). Finally, we remove d, with d the number of numbers < x
        d = 0
        for j in range(1, x):
            if T[j]:
                d += 1
        T[x] = True
        S += (x-1-d)*factorial(grid.m*grid.n-i)
    return S+1
