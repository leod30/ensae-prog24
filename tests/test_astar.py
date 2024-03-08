# This will work if ran from the root folder ensae-prog24
import unittest
import sys
sys.path.append("swap_puzzle/")
from graph import Graph


class Test_BFS(unittest.TestCase):
    def test_bfs_grid_file_2(self):
        """this function gets the graph in graph.in and tests if the astar function works
        with the graph.path.out, by testing astar(src,dst) (with src and dst the first 2
        numbers of each line in graph1.in) and then compares it to the list at the end
        of the line"""

        G = Graph.graph_from_file("input/graph2.in")
        # Open the file in read mode
        with open("input/graph2.path.out", "r") as file:
            tuple_list = []  # list of the src and dst in graph2.path.out (index i = line i)
            path_list = []  # list of paths in the file graph2.path.out (index i = line i)

            # Read each line of the file : very specific (and not really understandable)
            for line in file:
                elements = line.split(" ")  # splits the elements in each line separated by a space
                if elements[-1] == "None\n":
                    elements[-1] = "None"
                else:
                    last_number = (elements.pop())[:-2]  # removes the "\n" at the end of each line
                    elements.append(last_number)
                    elements.append("]")  # puts back the "]"
                    elements.pop(2)  # case where there is 3 numbers and 1 list

                # Convert the first two numbers of the file as integers
                num1 = eval(elements.pop(0))
                num2 = eval(elements.pop(0))

                list = "".join(elements)
                path = eval(list)  # python understands its a list, or a None object
                tuple_nums = (num1, num2)

                tuple_list.append(tuple_nums)
                path_list.append(path)

        for i in range(len(path_list)):
            path_astar = G.a_star(tuple_list[i][0], tuple_list[i][-1])
            self.assertEqual(path_astar, path_list[i])

        return path_astar


if __name__ == '__main__':
    unittest.main()
