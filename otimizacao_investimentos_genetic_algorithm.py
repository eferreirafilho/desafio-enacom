import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
import random

class GeneticAlgorithmOptimizer:
    def __init__(self, data, available_capital, cost_limit, minimum_per_category):
        if data is None:
            raise ValueError("No data provided")
        if isinstance(data, str):
            try:
                self.data = pd.read_csv(data, sep=';', header=None, names=['Investment', 'Cost', 'Return', 'Risk'])
            except FileNotFoundError:
                raise ValueError(f"Could not find data file: {data}")
            except Exception as e:
                print(f"Error loading data file: {e}")
                raise
        else:
            raise TypeError("Data should be a file path (str).")
        if self.data.empty:
            raise ValueError("Data file is empty")
        
        if not isinstance(available_capital, (int, float)) or available_capital <= 0:
            raise ValueError("Available capital should be a positive number.")

        self.available_capital = available_capital
        self.cost_limit = cost_limit
        self.minimum_per_category = minimum_per_category
        self.toolbox = base.Toolbox()
        
    def define_problem(self):
        number_of_investment_options = len(self.data)  # number of investment options
        investment_costs = self.data['Cost'].values  # investment costs
        return_of_investments = self.data['Return'].values  # ROIs
        low_risk_category = [1 if r == 0 else 0 for r in self.data['Risk'].values]  # Low risk investments
        medium_risk_category = [1 if r == 1 else 0 for r in self.data['Risk'].values]  # Medium risk investments
        high_risk_category = [1 if r == 2 else 0 for r in self.data['Risk'].values]  # High risk investments

        # define the problem as an optimization problem
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # maximization problem
        creator.create("Individual", list, fitness=creator.FitnessMax)

        # decision variables 
        self.toolbox.register("attr_bool", random.randint, 0, 1)

        # structure initializers
        self.toolbox.register("individual", tools.initRepeat, creator.Individual, self.toolbox.attr_bool, number_of_investment_options)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # evaluation function
        def evaluate(individual):
            total_cost = np.dot(individual, investment_costs)
            total_roi = np.dot(individual, return_of_investments)
            total_low_risk = np.dot(individual, low_risk_category)
            total_med_risk = np.dot(individual, medium_risk_category)
            total_high_risk = np.dot(individual, high_risk_category)
            total_low_risk_cost = np.dot(individual, investment_costs * low_risk_category)
            total_med_risk_cost = np.dot(individual, investment_costs * medium_risk_category)
            total_high_risk_cost = np.dot(individual, investment_costs * high_risk_category)
            
            if total_cost > self.available_capital:
                return -1,  # invalid solution
            if total_low_risk < self.minimum_per_category[0] or total_med_risk < self.minimum_per_category[1] or total_high_risk < self.minimum_per_category[2]:
                return -1,  # invalid solution
            if total_low_risk_cost > self.cost_limit[0] or total_med_risk_cost > self.cost_limit[1] or total_high_risk_cost > self.cost_limit[2]:
                return -1,  # invalid solution
            return total_roi,

        # operator definitions
        self.toolbox.register("evaluate", evaluate)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        
        self.return_of_investments = return_of_investments
        self.investment_costs = investment_costs
        self.low_risk_category = low_risk_category
        self.medium_risk_category = medium_risk_category
        self.high_risk_category = high_risk_category
        self.number_of_investment_options = number_of_investment_options

    def solve(self):
        pop = self.toolbox.population(n=50)
        hof = tools.HallOfFame(1, similar=np.array_equal)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        self.pop, self.log = algorithms.eaSimple(pop, self.toolbox, cxpb=0.5, mutpb=0.2, ngen=20, stats=stats, halloffame=hof, verbose=True)
        self.hof = hof

    def get_results(self):
        valid_solutions = [ind for ind in self.hof if ind.fitness.values[0] != -1]

        if not valid_solutions:
            print("No valid solution found.")
            return None

        best_solution = max(valid_solutions, key=lambda ind: ind.fitness.values[0])

        total_spent = np.dot(best_solution, self.investment_costs)
        total_return = np.dot(best_solution, self.return_of_investments)
        total_low_risk = np.dot(best_solution, self.low_risk_category)
        total_med_risk = np.dot(best_solution, self.medium_risk_category)
        total_high_risk = np.dot(best_solution, self.high_risk_category)

        print(f"\nBest solution:")
        print(f"Total ROI = {total_return}")
        print(f"Total Spent = {total_spent}")
        print(f"Available - Spent = {self.available_capital - total_spent}")
        print(f"Total Low Risk Investments = {total_low_risk}")
        print(f"Total Medium Risk Investments = {total_med_risk}")
        print(f"Total High Risk Investments = {total_high_risk}")
        
        return best_solution

    def save_results(self, solution):
        df = pd.DataFrame([solution])  # Notice the brackets around solution, it makes solution a row instead of a column
        df.to_csv('solutions.csv', index=False, header=False)

if __name__ == "__main__":
    try:
        optimizer = GeneticAlgorithmOptimizer('data.csv', available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1])
        optimizer.define_problem()
        optimizer.solve()
        solution = optimizer.get_results()
        optimizer.save_results(solution)
    except Exception as e:
        print(f"An error occurred: {e}")
