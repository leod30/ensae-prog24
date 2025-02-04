import numpy as np
from math import factorial
from graph import Graph
import pygame

"""
This is the grid module. It contains the Grid class and its associated methods.
"""


import random

class Grid():
    """
    A class representing the grid from the swap puzzle. It supports rectangular grids. 

    Attributes: 
    -----------
    m: int
        Number of lines in the grid
    n: int
        Number of columns in the grid
    state: list[list[int]]
        The state of the grid, a list of list such that state[i][j] is the number in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..m and columns are numbered 0..n.
    """

    def __init__(self, m, n, initial_state = []):
        """
        Initializes the grid.

        Parameters: 
        -----------
        m: int
            Number of lines in the grid
        n: int
            Number of columns in the grid
        initial_state: list[list[int]]
            The intiail state of the grid. Default is empty (then the grid is created sorted).
        """
        self.m = m
        self.n = n
        self.coeff = 7 - self.m * self.n / 45
        self.displayx = 1200
        self.displayy = 900
        if not initial_state:
            initial_state = [list(range(i*n+1, (i+1)*n+1)) for i in range(m)]            
        self.state = initial_state

        self.g_score = 100000
        self.parent = None
    
    def __str__(self): 
        """
        Prints the state of the grid as text.
        """
        output = f"The grid is in the following state:\n"
        for i in range(self.m): 
            output += f"{self.state[i]}\n"
        return output
    
    def __eq__(self, grid):
        return self.state == grid.state
    
    def __lt__(self, grid):
        """We compare the grids by their Manhattan's distance,
        which represents if the grid is more or less solved, in
        order to be able to use heap.heappush ( G < H means G is
        better )"""
        return self.Manhattan_distance() <= grid.Manhattan_distance()
    
    def deepcopy(self):
        list = [[cell for cell in line] for line in self.state]
        return Grid(self.m, self.n, list)

    def __repr__(self):
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: m={self.m}, n={self.n}>"

    def is_sorted(self):
        """
        Checks is the current state of the grid is sorte and returns the answer as a boolean.
        """
        return self.state == [list(range(i*self.n+1, (i+1)*self.n+1)) for i in range(self.m)]

    def swap(self, cell1, cell2):
        """
        Implements the swap operation between two cells. Raises an exception if the swap is not allowed.

        Parameters: 
        -----------
        cell1, cell2: tuple[int]
            The two cells to swap. They must be in the format (i, j) where i is the line and j the column number of the cell. 
        """
        if (cell1[0] == cell2[0] and abs(cell1[1] - cell2[1]) == 1) or (cell1[1] == cell2[1] and abs(cell1[0] - cell2[0]) == 1):
            c1, c2 = self.state[cell1[0]][cell1[1]], self.state[cell2[0]][cell2[1]]
            self.state[cell1[0]][cell1[1]] = c2
            self.state[cell2[0]][cell2[1]] = c1
        else :
            raise ValueError("This swap is not allowed.")

    def swap_seq(self, cell_pair_list):
        """
        Executes a sequence of swaps. 

        Parameters: 
        -----------
        cell_pair_list: list[tuple[tuple[int]]]
            List of swaps, each swap being a tuple of two cells (each cell being a tuple of integers). 
            So the format should be [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...].
        """
        for swap in cell_pair_list :
            self.swap(swap[0],swap[1])

    @classmethod
    def grid_from_file(cls, file_name): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.

        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "m n" 
            - next m lines contain n integers that represent the state of the corresponding cell

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            m, n = map(int, file.readline().split())
            initial_state = [[] for i_line in range(m)]
            for i_line in range(m):
                line_state = list(map(int, file.readline().split()))
                if len(line_state) != n: 
                    raise Exception("Format incorrect")
                initial_state[i_line] = line_state
            grid = Grid(m, n, initial_state)
        return grid


    def grid_representation(self, col_bg = "#101820", col_txt = "#FEE715"):
        """
        Creates a grid representation with pygame : we suggest you to run it on vscode
        """
        pygame.init()
        self.screen = pygame.display.set_mode((self.displayx, self.displayy))
        pygame.display.set_caption("GRID REPRESENTATION")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(col_bg)

            for i in range(self.m):
                for j in range(self.n):
                    pygame.draw.rect(surface=self.screen, color=col_txt,
                                     rect=pygame.Rect(self.displayx * (j + 2) / (self.n + 4),
                                                      self.displayy * (i + 2) / (self.m + 4),
                                                      self.displayx / (self.n + 4) + self.coeff,
                                                      self.displayy / (self.m + 4) + self.coeff),
                                     width=int(self.coeff))
                    font = pygame.font.SysFont('verdana bold', int(300 / max(self.m, self.n)))
                    text = font.render(str(self.state[i][j]), True, col_txt)
                    self.screen.blit(text, (self.displayx * (j + 5 / 2) / (self.n + 4) - text.get_rect().width / 2 +
                                             self.coeff / 2,
                                             self.displayy * (i + 5 / 2) / (self.m + 4) - text.get_rect().height / 2 +
                                             self.coeff / 2))

            pygame.display.flip()

        pygame.quit()

    def __hash__(self):
        #Question 6
        """The idea is this:
We replace the list of lists with a list with all the coefficients and we will assign a number which will be the
hash by numbering these lists coefficient by coefficient in ascending order. Then we notice, to avoid having to
store the list of all possible grids, that the (mn-1)! first lists start with 1, then (mn-1)! following by 2 etc.
Then for the 2nd digit, when we have located the slice corresponding to the first digit, we notice that the
(mn-2)! first numbers in this range start with the first digit not placed in the list in ascending order, etc.
This method produces a unique result

        Returns:
            S: int
                A unique integer representing the grid, that is between 0 and (mn-1)!
        """
        list = []
        for i in range(self.m): #We transform the grid into a list
            for j in range(self.n):
                list.append(self.state[i][j])

        T = [False for i in range(self.m*self.n+1)] #List whe T[i] indicates if whether or not i has been assigned
        S = 0   #The hash number that we are going to create
        for i in range(1, self.m*self.n+1): #We procede cell by cell
            x = list[i-1]   #We recreate the coefficient multiplied by (mn-i) in the hash, that is (x-1-d) : x-1 because we know that the first (mn-1)! starts by 1 (so it starts by (mn-1)!*0=(mn-1)!*(1-1)). Finally, we remove d, with d the number of numbers < x
            d = 0
            for j in range(1, x):
                if T[j]:
                    d += 1
            T[x] = True
            S += (x-1-d)*factorial(self.m*self.n-i)
        return S+1

    def dehash(self, hash):
        # Question 6
        """
        Same commentary as hash, but in the other direction

        Args:
            hash (int): the integer representing a grid, that we will decode into a list

        Returns:
            grid (list) : the list mentioned above
        """
        hash -= 1
        list = []
        visited = [False for i in range(self.n*self.m)]
        for k in range(self.n*self.m-1):
            r, d = hash % factorial(self.m*self.n-k-1), hash//factorial(self.n*self.m-k-1)
            x = 1
            while (d+1+len([i for i in visited[:x-1] if i])) != x or visited[x-1] is True:
                x += 1
            list.append(x)
            visited[x-1] = True
            hash = r
        
        # We add the last coefficient
        for k in range(1, self.n*self.m+1):
            if k not in list:
                list.append(k)
        
        # We convert our list into a grid.state
        grid = [[None for j in range(self.n)] for i in range(self.m)]

        for i in range(self.m):
            for j in range(self.n):
                grid[i][j]=list.pop(0)
        return grid
    

    def create_graph(self):
        #Question 7 part 1
        """Creates the graph corresponding to the situation, first, it adds all the nodes, ie all
            the possible grids then it creates the edges by doing all the possible swaps on the 
            grids, and adding their hash to the list of the neighbors of the node

        Returns:
            dict: the graph, represented by its adjacency list
        """
        graph = Graph(nodes=[i for i in range(1, factorial(self.m*self.n)+1)])
        for node in range(1, factorial(self.m*self.n)+1):
            for i in range(self.m):
                for j in range(self.n):
                  if i+1 < self.m:  # We do all the possible moves, if they dont go outside the dimensions of the grid
                    G = Grid(self.m, self.n, self.dehash(node))
                    G.swap((i,j),(i+1,j))
                    graph.add_edge(node, hash(G))

                  if j+1 < self.n:  # We do all the possible moves, if they dont go outside the dimensions of the grid
                    G = Grid(self.m, self.n, self.dehash(node))
                    G.swap((i,j),(i,j+1))
                    graph.add_edge(node, hash(G))

        return graph
    
    def Manhattan_distance(self):
        """This functions calculates the Manhattan distance from the grid in self.state to the grid 1,...,mn, but we no longer use it"""
        dist = 0
        for number in range(1,self.m*self.n+1): # We add all the distances of all the numbers
            # We find the coordinates of number in the self.state grid
            for i in range(self.m):
                if number in self.state[i]:
                    line1 = i
            for j in range(self.n):
                if number == self.state[line1][j]:
                    column1 = j
            
            # We find the desired coordinates of number
            line2, column2 = number // self.n, number % self.n

            # We add this to the distance
            dist += abs(line1-line2) + abs(column1-column2)
        
        return dist
    
    def generate_neighbors(self):
        """
        this function does all the swaps possible from a grid, and returns the list of the neighbors as a list
        """
        neighbors = []
        for i in range(self.m):
            for j in range(self.n):
                if i+1 < self.m:  # We do all the possible moves, if they dont go outside the dimensions of the grid
                    current_state_copy = self.deepcopy()
                    current_state_copy.swap((i,j),(i+1,j))
                    neighbors.append(current_state_copy)

                if j+1 < self.n:  # We do all the possible moves, if they dont go outside the dimensions of the grid
                    current_state_copy = self.deepcopy()
                    current_state_copy.swap((i,j),(i,j+1))
                    neighbors.append(current_state_copy)

            neighbors = list(set(neighbors))
        return neighbors

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
