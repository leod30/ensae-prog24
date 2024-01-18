from grid import Grid

class Solver(): 
    """
    A solver class, to be implemented.
    """

    def get_coord(self, number, grid:[Grid]):
        """
        Gets the coordinates (i,j) of number in grid, i being the line and j the column number

        Parameters:
        -----------
        number: int
            This number is between 1 and m*n
        """
        compteur = 0
        for i in range(grid.m):
            if number in grid.state[i]:
                line = i
        for j in range(grid.n):
            if number == grid.state[line][j]:
                column = j
        return (line, column)

    def get_seq(self, start: [tuple[int]], finish: [tuple[int]]):
        """
        Gets the sequence of swaps necessary to get the cell that has the coordinates "start" to "finish"

        Parameters:
        -----------
        start, finish: tuple[int]
            coordinates of the start and finish cells
        """
        print(start, finish)
        i1, j1, i2, j2 = start[0], start[1], finish[0], finish[1]
        swaps_lr = [((i1, j1-((j1-j2>0)-(j1-j2<0))*k),(i1, j1 - ((j1-j2>0)-(j1-j2<0))*(k+1))) for k in range (abs(j1-j2))]
        swaps_up = [((i1-k, j2),(i1-k-1, j2)) for k in range (i1-i2)]
        for swap in swaps_up:
            swaps_lr.append(swap)
        return swaps_lr

    def naive_solver(self, grid):
        """Idea: We proceed cell by cell, starting with the 1st line, then processing its cells from left to right
        and then continue. For each cell, we know what number must arrive in it (variable number). Then we get 
        the coordinates of this number in the grid (get_coord function). Then, we get the sequence of swaps that
        we must make to send the number in the desired cell (get_seq function). Finally, we apply this sequence
        with swap_seq, while incrementing the number of swaps.

        Does it work with every configuration? It seems to.

        Is the length optimal? There is no reason, so no.

        What is the estimated complexity? 	The function get_coord : assuming that « in » is O(1), its complexity is O(max(n,m))
											The function get_seq : its complexity is O(max(n,m))
											Thus, the overall function has a O(n^3+m^3) complexity"""
        solution = []
        n, m = grid.n, grid.m
        swaps = 0
        number = 1
        for i in range(m):
            for j in range(n):
                print(grid)
                i1, j1 = self.get_coord(number, grid)
                sequence = self.get_seq((i1, j1), (i, j))
                grid.swap_seq(sequence)
                swaps += len(sequence)
                for swap in sequence:
                    solution.append(swap)
                number += 1
        print(grid)
        return (solution, len(solution))

    def get_solution(self):
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        # TODO: implement this function (and remove the line "raise NotImplementedError").
        # NOTE: you can add other methods and subclasses as much as necessary. The only thing imposed is the format of the solution returned.
        raise NotImplementedError

solver=Solver()
grid = Grid(2, 3, [[5, 3, 6], [2, 1, 4]])
solver.naive_solver(grid)