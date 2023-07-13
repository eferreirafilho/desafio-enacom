import unittest
from unittest.mock import patch
import pandas as pd
from otimizacao_investimentos import InvestmentOptimizer

class TestInvestmentOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = InvestmentOptimizer('data.csv', available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1], maximum_medium_investment = 100)
    
    def test_init(self):
        self.assertEqual(self.optimizer.available_capital, 2400000)
        self.assertEqual(self.optimizer.cost_limit, [1200000, 1500000, 900000])
        self.assertEqual(self.optimizer.minimum_per_category, [2, 2, 1])
        self.assertEqual(self.optimizer.maximum_medium_investment, 100)
        
    def test_define_problem(self):
        self.optimizer.define_problem()
        self.assertIsNotNone(self.optimizer.prob)

    def test_solve(self):
        self.optimizer.define_problem()
        self.optimizer.solve()
        self.assertEqual(self.optimizer.prob.status, 1)
        
    def test_get_results(self):
        self.optimizer.define_problem()
        self.optimizer.solve()
        self.optimizer.get_results()
        self.assertEqual(self.optimizer.prob.objective.value(), 2220000.0)  # Expected ROI, replace 300 with actual expected ROI

    @patch("pandas.read_csv")
    def test_empty_data(self, mock_csv):
        mock_csv.return_value = pd.DataFrame(columns=['Investment', 'Cost', 'Return', 'Risk'])
        optimizer = InvestmentOptimizer('data.csv', available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1], maximum_medium_investment = 100)
        with self.assertRaises(Exception):
            optimizer.define_problem()
    
    @patch("pandas.read_csv")
    def test_negative_values(self, mock_csv):
        mock_csv.return_value = pd.DataFrame({
            'Investment': ['Inv1', 'Inv2', 'Inv3'],
            'Cost': [-100, 200, 300],
            'Return': [200, -400, 600],
            'Risk': [0, 1, 2]
        })
        optimizer = InvestmentOptimizer('data.csv', available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1], maximum_medium_investment = 100)
        with self.assertRaises(Exception):
            optimizer.define_problem()

    @patch("pandas.read_csv")
    def test_non_numeric_values(self, mock_csv):
        mock_csv.return_value = pd.DataFrame({
            'Investment': ['Inv1', 'Inv2', 'Inv3'],
            'Cost': ['abc', 200, 300],
            'Return': [200, 'xyz', 600],
            'Risk': [0, 1, 2]
        })
        optimizer = InvestmentOptimizer('data.csv', available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1], maximum_medium_investment = 100)
        with self.assertRaises(Exception):
            optimizer.define_problem()

    @patch("pandas.read_csv")
    def test_insufficient_investments(self, mock_csv):
        mock_csv.return_value = pd.DataFrame({
            'Investment': ['Inv1', 'Inv2', 'Inv3'],
            'Cost': [100, 200, 300],
            'Return': [200, 400, 600],
            'Risk': [0, 0, 0]  # All investments are low risk
        })
        optimizer = InvestmentOptimizer('data.csv', available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1], maximum_medium_investment = 100)
        with self.assertRaises(Exception):
            optimizer.define_problem()

if __name__ == '__main__':
    unittest.main()
