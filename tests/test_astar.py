# This will work if ran from the root folder ensae-prog24
import unittest
import sys
sys.path.append("swap_puzzle/")
from graph import Graph
from grid import Grid
from solver import Solver
import heuristics


solver = Solver()


class Test_ASTAR(unittest.TestCase):
    def test_astar(self):

        G = Grid(3, 3, [[5, 3, 6], [2, 1, 4], [8, 7, 9]])
        
        path_astar = solver.a_star(G, heuristics.hash)

        self.assertEqual(path_astar, [((0, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 0), (0, 1)), ((0, 2), (1, 2)), ((1, 1), (1, 2)), ((0, 2), (1, 2)), ((1, 1), (1, 2)), ((1, 0), (1, 1)), ((2, 0), (2, 1))])
        # We compare it to the path found with the bfs


if __name__ == '__main__':
    unittest.main()
