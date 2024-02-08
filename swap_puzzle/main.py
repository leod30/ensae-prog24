from grid import Grid
from solver import Solver
from graph import Graph

#Question 3 : naive solver
solver=Solver()
"""grid = Grid(2, 3, [[5, 3, 6], [2, 1, 4]])
solver.naive_solver(grid)"""

#Question 4
"""G = Grid(10,10)
G.grid_representation()"""

#Question 5 : we test all the lines
def test_graph(graph_number):
    """this function gets the graph in graph.in and tests if the bfs function works with the graph.path.out, by testing bfs(src,dst) (with src and dst the first 2 numbers of each line in graph1.in) and then compares it to the list at the end of the line"""
    G = Graph.graph_from_file(f"/home/onyxia/work/ensae-prog24/input/graph"+str(graph_number)+".in")
    # Open the file in read mode
    with open(f"/home/onyxia/work/ensae-prog24/input/graph"+str(graph_number)+".path.out", "r") as file:
        tuple_list = []  # list with tuples of integers, representing the first 2 numbers of each line in the file graph1.path.out
        list_list = []  # list with lists of integers, representing the path in each line in the file graph1.path.out
        
        # Read each line of the file
        for line in file:
            elements = line.split(" ") #splits the elements in each line separed by a space
            if elements[-1] == "None\n":
                elements[-1] = "None"
            else:
                last_number = (elements.pop())[:-2]  # at the end of each line, is a "\n" in order to return to a new line in the file, so we extract the number
                elements.append(last_number)
                elements.append("]")  # puts back the "]"
                num3 = eval(elements.pop(2))  # case where there is 3 numbers and 1 list
            
            # Convertir les trois premiers éléments en nombres entiers
            num1 = eval(elements.pop(0))
            num2 = eval(elements.pop(0))
            
            #removes the \n at the end of each line
            list = "".join(elements)
            path = eval(list) #python understands its a list, or a None object
            tuple_nums = (num1, num2)
            
            tuple_list.append(tuple_nums)
            list_list.append(path)

    function_work = True
    for i in range(len(list_list)):
        path_bfs = G.bfs(tuple_list[i][0], tuple_list[i][-1])
        if path_bfs != list_list[i]:
            function_work = False

    return "It works with graph number "+str(graph_number)+"!" if function_work else "It doesn't work"


"""print(test_graph(1))
print(test_graph(2))"""

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
solver.better_get_solution(grid)"""   #The solution is the same length here, but in general its length is <= to the naive one and is optimal

# Question 8 : we implemented the better_bfs function that stops the bfs when the goal node is reached
# Then, we use the get solve but with the better_bfs, its complexity is slightly better
"""grid = Grid(2, 3, [[5, 3, 6], [2, 1, 4]])
solver.better_get_solution(grid)"""