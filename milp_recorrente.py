import pandas as pd
from pulp import *
import os

# Read data from CSV
data = pd.read_csv('data.csv', sep=';', header=None, names=['Investment', 'Cost', 'Return', 'Risk'])

# Data
number_of_investment_options = len(data)  # number of investment options
investment_costs = data['Cost'].values
return_of_investments = data['Return'].values

# Risk category
L = [1 if r == 0 else 0 for r in data['Risk'].values]  # Low risk investments
M = [1 if r == 1 else 0 for r in data['Risk'].values]  # Medium risk investments
H = [1 if r == 2 else 0 for r in data['Risk'].values]  # High risk investments

available_capital = 2400000  # Available capital (modify this according to your scenario)


cost_limit = [1200000, 1500000, 900000] # Low, Medium, High
# cost_limit = [x * 1.1 for x in cost_limit]
minimum_per_category = [2, 2, 1]

# Define the problem
prob = LpProblem("Investment_Optimization", LpMaximize)

# Variables
x = LpVariable.dicts("Investment", range(number_of_investment_options), cat='Binary')

# Objective function
prob += lpSum([x[i] * return_of_investments[i] for i in range(number_of_investment_options)])

# Constraints
prob += lpSum([x[i] * investment_costs[i] for i in range(number_of_investment_options)]) <= available_capital, "Investment_Limit"
prob += lpSum([x[i] * L[i] for i in range(number_of_investment_options)]) >= minimum_per_category[0], "Low_Risk_Min"
prob += lpSum([x[i] * M[i] for i in range(number_of_investment_options)]) >= minimum_per_category[1], "Medium_Risk_Min"
prob += lpSum([x[i] * H[i] for i in range(number_of_investment_options)]) >= minimum_per_category[2], "High_Risk_Min"
prob += lpSum([x[i] * investment_costs[i] * L[i] for i in range(number_of_investment_options)]) <= cost_limit[0], "Low_Risk_Max"
prob += lpSum([x[i] * investment_costs[i] * M[i] for i in range(number_of_investment_options)]) <= cost_limit[1], "Medium_Risk_Max"
prob += lpSum([x[i] * investment_costs[i] * H[i] for i in range(number_of_investment_options)]) <= cost_limit[2], "High_Risk_Max"

previous_solutions = []

# Check if previous solutions file exists and load the previous solutions
if os.path.exists('previous_solutions.csv'):
    previous_solutions = pd.read_csv('previous_solutions.csv')['solution'].values.tolist()

for solution in previous_solutions:
    # Convert the solution from string to list of int
    solution = [int(val) for val in solution.split(',')]
    
    # Add constraint to exclude previous solution
    prob += lpSum([x[i] if solution[i] == 0 else 1-x[i] for i in range(number_of_investment_options)]) >= 1


MAX_NUMBER_OF_SOLUTIONS = 10
solution_number = 0

while solution_number < MAX_NUMBER_OF_SOLUTIONS:
    prob.solve(pulp.PULP_CBC_CMD(msg=True, warmStart=True))

    # If no solution found, break the loop
    if prob.status != 1:
        break

    # Create the solution as a list of binary variables
    current_solution = [int(x[i].value()) for i in range(number_of_investment_options)]

    # Add constraint to exclude the current solution in the next iteration
    prob += lpSum([x[i] if current_solution[i] == 0 else 1-x[i] for i in range(number_of_investment_options)]) >= 1

    print(current_solution)

    # Update the previous solutions list
    previous_solutions.append(','.join(map(str, current_solution)))

    total_spent = sum([current_solution[i] * investment_costs[i] for i in range(number_of_investment_options)])

    # Save the result to a csv file
    result = pd.DataFrame({
        'solution': [','.join(map(str, current_solution))],
        'total_roi': [prob.objective.value()],
        'total_spent': [total_spent],
        'ratio_roi_spent': [prob.objective.value()/total_spent]
    })

    if not os.path.isfile('previous_solutions.csv'):
        result.to_csv('previous_solutions.csv', index=False)
    else:  # else it exists so append without writing the header
        result.to_csv('previous_solutions.csv', mode='a', header=False, index=False)
        
    solution_number +=1
