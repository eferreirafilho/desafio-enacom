import unittest
from otimizacao_investimentos import InvestmentOptimizer
import os
import pandas as pd

class TestInvestmentOptimizer(unittest.TestCase):
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

        self.optimizer = InvestmentOptimizer(self.test_file, available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1])
        self.optimizer.define_problem()
        self.optimizer.solve()
        self.optimizer.get_results()

    def tearDown(self):
        os.remove(self.test_file)

    def test_define_problem(self):
        self.assertIsNotNone(self.optimizer.prob)

    def test_solve(self):
        self.assertEqual(self.optimizer.prob.status, 1)  # 1 is the status code for "Optimal"

    def test_get_results(self):
        expected_roi = 2220000.0
        expected_spent = 2380000
        expected_available_minus_spent = 20000
        expected_status = 'Optimal'
        self.assertEqual(self.optimizer.total_roi, expected_roi)
        self.assertEqual(self.optimizer.total_spent, expected_spent)
        self.assertEqual(self.optimizer.available_minus_spent, expected_available_minus_spent)
        self.assertEqual(self.optimizer.status, expected_status)  # Now this should work


if __name__ == '__main__':
    unittest.main()
