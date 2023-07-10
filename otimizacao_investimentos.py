import pandas as pd
from pulp import *

# Read data from CSV
data = pd.read_csv('data.csv', sep=';', header=None, names=['Investment', 'Cost', 'Return', 'Risk'])

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

# Define the problem
prob = LpProblem("Investment_Optimization", LpMaximize)

# Variables
x = LpVariable.dicts("Investment", range(n), cat='Binary')

# Objective function
prob += lpSum([x[i] * R[i] for i in range(n)])

# Constraints
prob += lpSum([x[i] * C[i] for i in range(n)]) <= available_capital, "Investment_Limit"
prob += lpSum([x[i] * L[i] for i in range(n)]) >= minimum_per_category[0], "Low_Risk_Min"
prob += lpSum([x[i] * M[i] for i in range(n)]) >= minimum_per_category[1], "Medium_Risk_Min"
prob += lpSum([x[i] * H[i] for i in range(n)]) >= minimum_per_category[2], "High_Risk_Min"
prob += lpSum([x[i] * C[i] * L[i] for i in range(n)]) <= cost_limit[0], "Low_Risk_Max"
prob += lpSum([x[i] * C[i] * M[i] for i in range(n)]) <= cost_limit[1], "Medium_Risk_Max"
prob += lpSum([x[i] * C[i] * H[i] for i in range(n)]) <= cost_limit[2], "High_Risk_Max"
# prob += lpSum([x[i] * R[i] for i in range(n)]) >= 2220001, "total ROI"
# prob += lpSum([x[i] * C[i] for i in range(n)]) <= 2380000, "total spent"

# Solve the problem
prob.solve(pulp.PULP_CBC_CMD(msg=True))

# Print the results

total_spent = 0

investments = {"Low Risk": [], "Medium Risk": [], "High Risk": []}

risk_dict = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}

for i in range(n):
    if x[i].value() == 1.0:
        investment_info = data.iloc[i]
        risk_category = risk_dict[investment_info['Risk']] 
        print(f"Investment {i + 1}  - Cost: {investment_info['Cost']}, Return: {investment_info['Return']}, Risk: {risk_category}")

        total_spent += investment_info['Cost']

        if L[i] == 1:
            investments["Low Risk"].append(investment_info['Investment'])
        elif M[i] == 1:
            investments["Medium Risk"].append(investment_info['Investment'])
        elif H[i] == 1:
            investments["High Risk"].append(investment_info['Investment'])

print(f"\nInvestments by risk category:")
for category, investments in investments.items():
    print(f"{category}: {investments}")
    
print(f"\nTotal ROI = {prob.objective.value()}")
print(f"Total Spent = {total_spent}")
print(f"Available - Spent = {available_capital - total_spent}")

print(f"Status: {LpStatus[prob.status]}")