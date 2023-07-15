import unittest
from unittest import mock
from unittest.mock import patch
from otimizacao_investimentos_linear_programming import InvestmentOptimizer
from otimizacao_investimentos_genetic_algorithm import GeneticAlgorithmOptimizer
from optimization_gui import Application  # Assuming app.py is the file containing the code

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = Application()

    @patch('tkinter.messagebox.showerror')
    def test_validate_positive_integer(self, mock_msg):
        self.assertEqual(self.app.validate_positive_integer("5"), 5)
        self.assertIsNone(self.app.validate_positive_integer("-1"))
        self.assertIsNone(self.app.validate_positive_integer("2.5"))
        mock_msg.assert_called()

    @patch('tkinter.messagebox.showerror')
    def test_validate_float(self, mock_msg):
        self.assertEqual(self.app.validate_float("10.5"), 10.5)
        self.assertIsNone(self.app.validate_float("invalid_input"))
        mock_msg.assert_called()

    @patch('tkinter.messagebox.showerror')
    def test_load_data(self, mock_msg):
        self.app.data_cb.set("data.csv")
        self.app.load_data()
        self.assertEqual(self.app.data, "data.csv")

        self.app.data_cb.set("fake_data.csv")
        self.app.load_data()
        self.assertEqual(self.app.data, "fake_data.csv")

        self.app.data_cb.set("invalid_data.csv")
        self.app.load_data()
        mock_msg.assert_called()

    @patch('tkinter.messagebox.showerror')
    def test_solve(self, mock_msg):
        self.app.data = 'data.csv'
        self.app.available_capital_entry.delete(0, 'end')
        self.app.available_capital_entry.insert(0, '2400000')
        self.app.cost_limit_entry.delete(0, 'end')
        self.app.cost_limit_entry.insert(0, '[1200000, 1500000, 900000]')
        self.app.minimum_per_category_entry.delete(0, 'end')
        self.app.minimum_per_category_entry.insert(0, '[2, 2, 1]')
        self.app.solver_cb.set("Linear Programming (Deterministic, Optimal)")
        self.app.solve()
        self.assertIsInstance(self.app.optimizer, InvestmentOptimizer)

        self.app.solver_cb.set("Genetic Algorithm (Stochastic)")
        self.app.solve()
        self.assertIsInstance(self.app.optimizer, GeneticAlgorithmOptimizer)

        self.app.data = None
        self.app.solve()
        mock_msg.assert_called()

if __name__ == "__main__":
    unittest.main()
