import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt  # Add this line to import matplotlib

# Read data from CSV
data = pd.read_csv('fake_data.csv', sep=';', header=None, names=['Investment', 'Cost', 'Return', 'Risk'])

# Data
n = len(data)  # number of investment options
C = data['Cost'].values  # investment costs
R = data['Return'].values  # ROIs

# Risk category
L = [1 if r == 0 else 0 for r in data['Risk'].values]  # Low risk investments
M = [1 if r == 1 else 0 for r in data['Risk'].values]  # Medium risk investments
H = [1 if r == 2 else 0 for r in data['Risk'].values]  # High risk investments

available_capital = 2400000  # Available capital (modify this according to your scenario)

cost_limit = [1200000, 1500000, 900000] # Low, Medium, High
minimum_per_category = [2, 2, 1]

# define the problem as an optimization problem
creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # maximization problem
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# decision variables 
toolbox.register("attr_bool", np.random.choice, [0, 1])

# structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# evaluation function
def evaluate(individual):
    total_cost = np.dot(individual, C)
    total_roi = np.dot(individual, R)
    total_low_risk = np.dot(individual, L)
    total_med_risk = np.dot(individual, M)
    total_high_risk = np.dot(individual, H)
    total_low_risk_cost = np.dot(individual, C * L)
    total_med_risk_cost = np.dot(individual, C * M)
    total_high_risk_cost = np.dot(individual, C * H)
    
    if total_cost > available_capital:
        return -1,  # invalid solution
    if total_low_risk < minimum_per_category[0] or total_med_risk < minimum_per_category[1] or total_high_risk < minimum_per_category[2]:
        return -1,  # invalid solution
    if total_low_risk_cost > cost_limit[0] or total_med_risk_cost > cost_limit[1] or total_high_risk_cost > cost_limit[2]:
        return -1,  # invalid solution
    return total_roi,

# operator definitions
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Genetic Algorithm execution
def main():
    pop = toolbox.population(n=1000)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=200, stats=stats, halloffame=hof, verbose=True)

    return pop, log, hof
if __name__ == "__main__":
    pop, log, hof = main()

    # Best solutions with maximum fitness (total ROI)
    best_solutions = [ind for ind in hof if ind.fitness.values[0] == hof[0].fitness.values[0]]

    # Calculate total spent, total return, and categorize the investments for each best solution
    for solution in best_solutions:
        total_spent = 0
        total_return = 0
        investments = {"Low Risk": [], "Medium Risk": [], "High Risk": []}
        risk_dict = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}

        for i in range(n):
            if solution[i] == 1:
                investment_info = data.iloc[i]
                risk_category = risk_dict[investment_info['Risk']]
                print(f"Investment {i + 1}  - Cost: {investment_info['Cost']}, Return: {investment_info['Return']}, Risk: {risk_category}")

                total_spent += investment_info['Cost']
                total_return += investment_info['Return']

                if L[i] == 1:
                    investments["Low Risk"].append(investment_info['Investment'])
                elif M[i] == 1:
                    investments["Medium Risk"].append(investment_info['Investment'])
                elif H[i] == 1:
                    investments["High Risk"].append(investment_info['Investment'])

        print(f"\nInvestments by risk category:")
        for category, investments in investments.items():
            print(f"{category}: {investments}")

        print(f"\nTotal ROI = {total_return}")
        print(f"Total Spent = {total_spent}")
        print(f"Available - Spent = {available_capital - total_spent}")
        print("--------------------")
