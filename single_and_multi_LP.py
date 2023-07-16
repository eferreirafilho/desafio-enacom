import pandas as pd
from pulp import *

class InvestmentOptimizer:
    def __init__(self, data, available_capital, cost_limit, minimum_per_category, singleobjective):
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

        self.singleobjective = singleobjective
        self.available_capital = available_capital
        self.cost_limit = cost_limit
        self.minimum_per_category = minimum_per_category

    def define_problem(self):
        number_of_investment_options = len(self.data)
        investment_costs = self.data['Cost'].values
        return_of_investments = self.data['Return'].values  # ROIs

        low_risk_category = [1 if r == 0 else 0 for r in self.data['Risk'].values]  # Low risk investments
        medium_risk_category = [1 if r == 1 else 0 for r in self.data['Risk'].values]  # Medium risk investments
        high_risk_category = [1 if r == 2 else 0 for r in self.data['Risk'].values]  # High risk investments

        prob = LpProblem("Investment_Optimization", LpMaximize)

        chosen_investments = LpVariable.dicts("Investment", range(number_of_investment_options), cat='Binary')
        total_spent = lpSum([chosen_investments[i] * investment_costs[i] for i in range(number_of_investment_options)])
        
        if self.singleobjective:
            prob += lpSum([chosen_investments[i] * return_of_investments[i] for i in range(number_of_investment_options)])
        else:
        # Objective components
            total_roi = lpSum([chosen_investments[i] * return_of_investments[i] for i in range(number_of_investment_options)])

            # Define weights
            weight_roi = 0.9  # Adjust these weights according to your preference
            weight_spent = 0.1

            # Create the combined objective function
            prob += weight_roi * total_roi - weight_spent * total_spent

        prob += lpSum([chosen_investments[i] * investment_costs[i] for i in range(number_of_investment_options)]) <= self.available_capital, "Investment_Limit"
        prob += lpSum([chosen_investments[i] * low_risk_category[i] for i in range(number_of_investment_options)]) >= self.minimum_per_category[0], "Low_Risk_Min"
        prob += lpSum([chosen_investments[i] * medium_risk_category[i] for i in range(number_of_investment_options)]) >= self.minimum_per_category[1], "Medium_Risk_Min"
        prob += lpSum([chosen_investments[i] * high_risk_category[i] for i in range(number_of_investment_options)]) >= self.minimum_per_category[2], "High_Risk_Min"
        prob += lpSum([chosen_investments[i] * investment_costs[i] * low_risk_category[i] for i in range(number_of_investment_options)]) <= self.cost_limit[0], "Low_Risk_Max_Cost"
        prob += lpSum([chosen_investments[i] * investment_costs[i] * medium_risk_category[i] for i in range(number_of_investment_options)]) <= self.cost_limit[1], "Medium_Risk_Max_Cost"
        prob += lpSum([chosen_investments[i] * investment_costs[i] * high_risk_category[i] for i in range(number_of_investment_options)]) <= self.cost_limit[2], "High_Risk_Max_Cost"
        
        self.prob = prob
        self.chosen_investments = chosen_investments
        self.low_risk_category = low_risk_category
        self.medium_risk_category = medium_risk_category
        self.high_risk_category = high_risk_category

    def solve(self):
        self.prob.solve(pulp.PULP_CBC_CMD(msg=True))
        
    def get_results(self):
        if self.prob.status != LpStatusOptimal:
            raise ValueError('The problem is infeasible.')
        total_spent = 0
        total_roi = 0  # Initialize total ROI
        solution = []  # For storing the solution
        investments = {"Low Risk": [], "Medium Risk": [], "High Risk": []}
        risk_dict = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}

        for i in range(len(self.data)):
            solution.append(int(self.chosen_investments[i].value()))  # Save the solution
            if self.chosen_investments[i].value() == 1.0:
                investment_info = self.data.iloc[i]
                risk_category = risk_dict[investment_info['Risk']] 
                print(f"Investment {i + 1}  - Cost: {investment_info['Cost']}, Return: {investment_info['Return']}, Risk: {risk_category}")

                total_spent += investment_info['Cost']
                total_roi += investment_info['Return']  # Add the return of the chosen investment to total ROI

                if self.low_risk_category[i] == 1:
                    investments["Low Risk"].append(investment_info['Investment'])
                elif self.medium_risk_category[i] == 1:
                    investments["Medium Risk"].append(investment_info['Investment'])
                elif self.high_risk_category[i] == 1:
                    investments["High Risk"].append(investment_info['Investment'])

        self.investments = investments
        self.total_roi = total_roi  # Update total ROI
        self.total_spent = total_spent
        self.available_minus_spent = self.available_capital - total_spent

        print(f"\nInvestments by risk category:")
        for category, investment_list in self.investments.items():
            print(f"{category}: {investment_list}")

        print(f"\nTotal ROI = {self.total_roi}")
        print(f"Total Spent = {self.total_spent}")
        print(f"Available - Spent = {self.available_minus_spent}")
        print(f"Status: {LpStatus[self.prob.status]}")
        self.status = LpStatus[self.prob.status]
        
        return solution

    def save_results(self, solution):
        df = pd.DataFrame([solution])  # Notice the brackets around solution, it makes solution a row instead of a column
        df.to_csv('solutions.csv', index=False, header=False)

if __name__ == "__main__":
    try:
        optimizer = InvestmentOptimizer('data.csv', available_capital = 2400000, cost_limit = [1200000, 1500000, 900000], minimum_per_category = [2, 2, 1], singleobjective = True)
        optimizer.define_problem()
        optimizer.solve()
        solution = optimizer.get_results()  # Get the solution
        optimizer.save_results(solution)  # Save the solution to a CSV file
    except Exception as e:
        print(f"An error occurred: {e}")
