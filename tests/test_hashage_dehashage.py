# This will work if ran from the root folder ensae-prog24
import sys
from math import factorial
import unittest
sys.path.append("swap_puzzle/")
from grid import Grid


class Test_HashDehash(unittest.TestCase):
    def test_hash_dehash(self):
        """We test all the hash and dehash for a grid with 2 lines and 3 columns"""
        G = Grid(2, 3)
        for i in range(1, factorial(6)+1):
            self.assertEqual(hash(Grid(2, 3, G.dehash(i))), i)


if __name__ == '__main__':
    unittest.main()
