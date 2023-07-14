import unittest
from otimizacao_investimentos_genetic_algorithm import GeneticAlgorithmOptimizer
import os
import pandas as pd

class TestGeneticAlgorithmOptimizer(unittest.TestCase):
    def setUp(self):
        # Write test data into a csv file
        self.test_file = "test_data.csv"
        self.test_data = """1;470000;410000;0
                            2;400000;330000;0
                            3;170000;140000;1
                            4;270000;250000;1
                            5;340000;320000;1
                            6;230000;320000;1
                            7;50000;90000;1
                            8;440000;190000;2
                            9;320000;120000;2
                            10;800000;450000;2
                            11;120000;80000;0
                            12;150000;120000;0
                            13;300000;380000;1"""
        with open(self.test_file, 'w') as f:
            f.write(self.test_data)

        self.optimizer = GeneticAlgorithmOptimizer(self.test_file, available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1])
        self.optimizer.define_problem()
        self.optimizer.solve()
        self.optimizer.get_results()

    def tearDown(self):
        os.remove(self.test_file)

    def test_invalid_input_file(self):
        with self.assertRaises(ValueError):
            optimizer = GeneticAlgorithmOptimizer("", available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1])

    def test_file_not_found(self):
        with self.assertRaises(ValueError):
            optimizer = GeneticAlgorithmOptimizer("non_existent.csv", available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1])

    def test_empty_data_file(self):
        with open('empty.csv', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            optimizer = GeneticAlgorithmOptimizer('empty.csv', available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1])
        os.remove('empty.csv')

    def test_invalid_available_capital(self):
        with self.assertRaises(ValueError):
            optimizer = GeneticAlgorithmOptimizer(self.test_file, available_capital = -2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1])

if __name__ == '__main__':
    unittest.main()
