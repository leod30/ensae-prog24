import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'

from grid import Grid
from solver import Solver
from graph import Graph
import heuristics

import time

# Question 3 : naive solver
solver = Solver()
"""grid = Grid(2, 3, [[5, 3, 6], [2, 1, 4]])
solver.naive_solver(grid)"""

# Question 4
"""G = Grid(10,10)
G.grid_representation()"""

# Question 5 : we test all the lines, with tests/test_bfs.py, and it do work

# Question 6 :The idea is this:
# We replace the list of lists with a list with all the coefficients and we will assign a number which will be the
# hash by numbering these lists coefficient by coefficient in ascending order. Then we notice, to avoid having to
# store the list of all possible grids, that the (mn-1)! first lists start with 1, then (mn-1)! following by 2 etc.
# Then for the 2nd digit, when we have located the slice corresponding to the first digit, we notice that the
# (mn-2)! first numbers in this range start with the first digit not placed in the list in ascending order, etc.
# This method produces a unique result
# You can see this in the grid class

# Question 7 : number of nodes : (mn)!, number of edges : it seems to be 2(mn)!; thus the complexity of the bfs is O((mn)!), 
# hash and dehash are O((mn)!) (even less but it doesn't change anything)
# create_graph is O((mn)!*mn), so the overall function is O((mn)*mn)
"""grid = Grid(2, 3, [[5, 3, 6], [2, 1, 4]])
print(solver.get_solution(grid))"""   #The solution is the same length here, but in general its length is <= to the naive one and is optimal

# Question 8 : here, we are only going to create the part of the graph that we need, to do it, as we 
# use the bfs, we create the corresponding nodes and edges
"""grid = Grid(2, 3, [[5, 3, 6], [2, 1, 4]])
solver.better_get_solution(grid)"""
# Thus, we conclude that this method is overall more efficient, we can even do it for slightly
# bigger grids in a reasonable amount of time which was impossible with the previous method
# but its complexity depends on the case, and it can be as complex as the previous ones in the worst cases



# A* algorithm : 
# To implement this algorithm, we need a heuristic. Our first idea is the Manhattan distance.
# It consists of saying that the weight of a block and its distance Δx+Δy to its sorted position,
# and that the evaluated distance from the grid is the sum of the weights. However, in the
# following case: [[1, 2, 6], [4, 5, 3]], 1 swap can resolve the grid but its distance of
# Manhattan to the sorted position is 2, we will therefore test heuristics which are multiples
# of this, for example the Manhattan distance divided by 2.

# First, we implement the distance of Manhattan function in the Grid class

# Once this is done, we can code the algorithm (in solver class), but first, we create the g_score and parent
# attribute in the grid class, g_score (which will be the distance from this node to the initial state) with 
# a high value and parent set to None, so we can stop our algorithm when a grid has no parent

# Doing this, we found out that the Manhattan distance, even with some changes was not efficient, and we thought of our hash : this
# could be a great heuristic, so we tested it, and it works very well!

# For example, here, we tested on a 3,3 grid the previous and the Astar algorithm : the previous took 52
# seconds and the Astar only 0.1 second


start_time = time.time()
grid = Grid(3, 3, [[5, 3, 6], [2, 1, 4], [8,7,9]])
solver.a_star(grid, heuristics.hash)
end_time = time.time()

execution_time = end_time - start_time
print("1. Execution time :", execution_time, "seconds")  #This lasts around 0.1 second

#############

start_time = time.time()
grid = Grid(3, 3, [[5, 3, 6], [2, 1, 4], [8,7,9]])
solver.better_get_solution(grid)
end_time = time.time()

execution_time = end_time - start_time
print("2. Execution time :", execution_time, "seconds")  #This lasts around 50 seconds, a lot longer

# Then, we chose to use pygame to create a game, this is done in the "app.py" file. Warning : if you run it on Onyxia or vscode via github, it doesn't have any environment to display it
