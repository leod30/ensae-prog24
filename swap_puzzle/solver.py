from grid import Grid
from grid import get_swap
from graph import Graph
from math import factorial
import heapq

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
                i1, j1 = self.get_coord(number, grid)
                sequence = self.get_seq((i1, j1), (i, j))
                grid.swap_seq(sequence)
                swaps += len(sequence)
                for swap in sequence:
                    solution.append(swap)
                number += 1
        return (solution, len(solution))

    def get_solution(self, grid):
        # Question 7 part 2 with the bfs and all the graph created
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        graph = grid.create_graph()     # We get the graph corresponding
        if (hash(grid)) == 1:
            return "Already solved"
        path = graph.bfs(hash(grid), 1)      # we get the path and the len of it by bfs
        # Then, we need to obtain which swap gives us the transformation from one grid to another
        # We implemented this function as get_swap in the grid.py file
        path = [get_swap(grid.dehash(path[i]),grid.dehash(path[i+1])) for i in range(len(path)-1)]
        return path
    
    def better_get_solution(self, grid):
        # Question 8 with the creation of the part needed of the graph
        """
        Solves the grid and returns the sequence of swaps at the format 
        [((i1, j1), (i2, j2)), ((i1', j1'), (i2', j2')), ...]. 
        """
        # We do the bfs directly here, but we create the nodes and edges when needed
        if (hash(grid)) == 1:
            return "Already solved"
        
        graph = Graph(nodes=[i for i in range(1, factorial(grid.m*grid.n)+1)])
        src = hash(grid)
        dst = 1
        queue = [src]
        marked = [src]
        prev = [None for i in range(factorial(grid.m*grid.n))] #list of the parents, in the same order as the nodes
        while len(queue) != 0 and dst not in queue :
            current = queue.pop(0)
            
            # Here we will need the neighbors of current, so we create them
            neighbors = Grid(grid.m,grid.n, grid.dehash(current)).generate_neighbors()

            
            for neighbor in neighbors:
                graph.add_edge(current, hash(neighbor))

            # Now we continue the bfs, because the edges needed have been created
            for neighbor in graph.graph[current]:
                if neighbor not in marked:
                    queue.append(neighbor)
                    marked.append(neighbor)
                    prev[neighbor-1]=current
        
        path=[dst]
        while src not in path:
            path.append(prev[path[-1]-1])
        path.reverse()

        # Then, we need to obtain which swap gives us the transformation from one grid to another
        # We implemented this function as get_swap in the grid.py file
        path = [get_swap(grid.dehash(path[i]),grid.dehash(path[i+1])) for i in range(len(path)-1)]
        return path

    def a_star(self, grid):
        """A-star algorithm with the distance of Manhattan as an evaluation of the distance to the goal
        
        ---------
        Parameters:
            grid : the grid that we want to solve"""
        grid.g_score = 0  # The grid from where we start
        # Initialize the priority queue
        open_list = [(grid.Manhattan_distance(), grid)]  # heapq works with list of tuples (heuristic, element)
        closed_set = set()  # Already visited
        while open_list:
            print(len(open_list))
            # Extract the state with the smallest heuristic from the priority queue
            
            current_heuristic, current_state = heapq.heappop(open_list)
            # Check if the current state is the goal state
            if current_state.state == Grid(grid.m, grid.n).state :

                # Reconstruct the path from the goal state to the start state
                path = []
                while current_state is not None:
                    path.append(current_state)
                    current_state = current_state.parent
                # Return the path in reverse order since it was constructed from goal to start
                path.reverse()
                path = [get_swap(path[i].state,path[i+1].state) for i in range(len(path)-1)]
                return path
                

            # Add the current state to the closed set
            closed_set.add(current_state)

            # Generate neighbors of the current state
            neighbors = current_state.generate_neighbors()

            for neighbor in neighbors:
                # Check if the neighbor is already in the closed set
                if neighbor in closed_set:
                    continue

                # Calculate the path cost to the neighbor
                tentative_g_score = current_state.g_score + 1

                # Check if the neighbor is already in the open_list
                better_option_found = True
                for i, (h, n) in enumerate(open_list):
                    if neighbor.state == n.state:
                        # If the neighbor is already in the open_list and the new cost is lower, update its information
                        if tentative_g_score+neighbor.Manhattan_distance() < h:
                            del open_list[i]
                        else:
                            better_option_found = False
                        break
                
                if better_option_found:
                    neighbor.g_score = tentative_g_score
                    neighbor.parent = current_state

                    # Calculate the heuristic for the neighbor
                    neighbor_heuristic = neighbor.Manhattan_distance()

                    # Add the neighbor to the priority queue
                    heapq.heappush(open_list, (tentative_g_score + neighbor_heuristic, neighbor))

        # If no path found, return None
        return None