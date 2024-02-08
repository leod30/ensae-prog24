from grid import Grid
from solver import Solver

#Question 3 : naive solver
solver=Solver()
grid = Grid(2, 3, [[5, 3, 6], [2, 1, 4]])
solver.naive_solver(grid)





#solver.get_solution(grid)   #The solution is the same length here, but in general its length is <= to the naive one and is optimal


def get_swap(grid1,grid2):
    # Question 7
    """
    Here, the grids are lists of lists
    This function get the swap (i,j),(k,l) that permits
    to go from grid1 to grid2, assuming that the swap
    is possible
    """
    for i in range(len(grid1)):
        for j in range(len(grid1[0])):
            gridtest = [[j for j in grid1[i]] for i in range(len(grid1))]  #A copy of grid 1 that we test all swaps on and stop when grid2 == gridtest
            if i+1 < len(grid1):  # We do all the possible moves, if they dont go outside the dimensions of the grid
                c1, c2 = grid1[i][j], grid1[i+1][j]
                gridtest[i][j] = c2
                gridtest[i+1][j] = c1
                if gridtest == grid2:
                    return ((i,j),(i+1,j))

            gridtest = [[j for j in grid1[i]] for i in range(len(grid1))]  #A copy of grid 1 that we test all swaps on and stop when grid2 == gridtest
            if j+1 < len(grid1[0]):  # We do all the possible moves, if they dont go outside the dimensions of the grid
                c1, c2 = grid1[i][j], grid1[i][j+1]
                gridtest[i][j] = c2
                gridtest[i][j+1] = c1
                if gridtest == grid2:
                    return ((i,j),(i,j+1))
#Question 7 : number of nodes : (mn)!, number of edges :