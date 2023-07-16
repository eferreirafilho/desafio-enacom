import pandas as pd

# Import the modified InvestmentOptimizer class
from otimizacao_investimentos_prog_linear import InvestmentOptimizer

def get_n_best_solutions(n, data='data.csv', available_capital=2400000, cost_limit=[1200000, 1500000, 900000], minimum_per_category=[2, 2, 1], singleobjective=True):
    optimizer = InvestmentOptimizer(data, available_capital, cost_limit, minimum_per_category, singleobjective)
    optimizer.clear_old_results('multiple_solutions.csv')
    for i in range(n):
        print(f"\nRunning optimization round {i+1}")
        try:
            optimizer.define_problem()
            optimizer.solve()
            solution = optimizer.get_results()  # Get the solution
            optimizer.save_multiple_results(solution, 'multiple_solutions.csv')  # Save the solution to a new CSV file
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_n_best_solutions(5)
