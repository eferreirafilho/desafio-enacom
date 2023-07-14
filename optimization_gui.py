import pandas as pd
import tkinter as tk
from tkinter import filedialog, Scale, Button, Label, Entry, messagebox
from tkinter import ttk
from tkinter.ttk import Combobox
from pulp import LpStatusOptimal, LpStatus
from generate_fake_data import generate_fake_data
from otimizacao_investimentos_linear_programming import InvestmentOptimizer
from otimizacao_investimentos_genetic_algorithm import GeneticAlgorithmOptimizer

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ENACOM - Investment Optimization")  
        self.geometry('1280x600')

        self.data_options = ["data.csv", "fake_data.csv"]
        self.solvers = ["Linear Programming (Deterministic, Optimal)", "Genetic Algorithm (Stochastic)"]

        Label(self, text="Select data:").grid(column=0, row=0, sticky='e')
        self.data_cb = Combobox(self, values=self.data_options, width=50)
        self.data_cb.current(0)  
        self.data_cb.grid(column=1, row=0)

        self.load_button = Button(self, text="Load Data", command=self.load_data)
        self.load_button.grid(column=1, row=1)

        Label(self, text="Available capital:").grid(column=0, row=2, sticky='e')
        self.available_capital_entry = Entry(self, width=50)
        self.available_capital_entry.insert(0, '2400000')
        self.available_capital_entry.grid(column=1, row=2)

        Label(self, text="Cost limit (Low Risk, Medium Risk, High Risk):").grid(column=0, row=3, sticky='e')
        self.cost_limit_entry = Entry(self, width=50)
        self.cost_limit_entry.insert(0, '[1200000, 1500000, 900000]')
        self.cost_limit_entry.grid(column=1, row=3)

        Label(self, text="Minimum per category (Low Risk, Medium Risk, High Risk):").grid(column=0, row=4, sticky='e')
        self.minimum_per_category_entry = Entry(self, width=50)
        self.minimum_per_category_entry.insert(0, '[2, 2, 1]')
        self.minimum_per_category_entry.grid(column=1, row=4)

        Label(self, text="Number of fake data points:").grid(column=0, row=5, sticky='e')
        self.num_fake_data_points_entry = Entry(self, width=50)
        self.num_fake_data_points_entry.insert(0, '5000')
        self.num_fake_data_points_entry.grid(column=1, row=5)

        self.gen_button = Button(self, text="Generate Fake Data", command=self.gen_data)
        self.gen_button.grid(column=1, row=6)

        Label(self, text="Select solver:").grid(column=0, row=7, sticky='e')
        self.solver_cb = Combobox(self, values=self.solvers, width= 50)
        self.solver_cb.current(0)
        self.solver_cb.grid(column=1, row=7)

        self.solve_button = Button(self, text="Solve", command=self.solve)
        self.solve_button.grid(column=1, row=8)

        self.solution_button = Button(self, text="View Solution", command=self.view_solution)
        self.solution_button.grid(column=1, row=9)
        
        self.tree = ttk.Treeview(self, show='headings')
        self.tree.grid(column=1, row=10)

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(10, weight=1)
        # Configuring the Treeview
        self.tree.grid(column=0, row=10, sticky='nsew', columnspan=2)

        self.data = None
        self.solution = None
        self.optimizer = None

    def validate_positive_integer(self, value):
        try:
            value = int(value)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            messagebox.showerror("Error", "Input should be a positive integer.")
            return None

    def validate_float(self, value):
        try:
            return float(value)
        except ValueError:
            messagebox.showerror("Error", "Input should be a float.")
            return None

    def load_data(self):
        self.selected_data_option = self.data_cb.get()
        try:
            if self.selected_data_option == "data.csv":
                self.data = str(self.data_options[0])
                print('Data: ' + str(self.data_options[0]) + ' loaded!')
            elif self.selected_data_option == "fake_data.csv":
                self.data = str(self.data_options[1])
                print('Data: ' + str(self.data_options[1]) + ' loaded!')
            else:
                raise ValueError("Invalid data option selected.")
        except Exception as e:
            messagebox.showerror("Error", f"Error while loading data: {str(e)}")

    def gen_data(self):
        try:
            num_fake_data_points = self.validate_positive_integer(self.num_fake_data_points_entry.get())
            if num_fake_data_points is None:
                return

            self.data = generate_fake_data(num_fake_data_points)
            self.data_cb.set("fake_data.csv")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error while generating fake data: {str(e)}")

    def solve(self):
        try:
            available_capital = self.validate_float(self.available_capital_entry.get())
            cost_limit = [self.validate_positive_integer(x) for x in eval(self.cost_limit_entry.get())]
            minimum_per_category = [self.validate_positive_integer(x) for x in eval(self.minimum_per_category_entry.get())]

            if None in cost_limit or None in minimum_per_category or available_capital is None:
                return
            solver = self.solver_cb.get()
            if self.data is None:  
                raise ValueError("No data provided.")
            else:
                if solver == "Linear Programming (Deterministic, Optimal)":
                    self.optimizer = InvestmentOptimizer(self.data, available_capital, cost_limit, minimum_per_category)
                elif solver == "Genetic Algorithm (Stochastic)":
                    self.optimizer = GeneticAlgorithmOptimizer(self.data, available_capital, cost_limit, minimum_per_category)
                else:
                    raise ValueError("Invalid solver option selected.")

                self.optimizer.define_problem()
                self.optimizer.solve()
                solution = self.optimizer.get_results()
                self.optimizer.save_results(solution)
        except Exception as e: 
            messagebox.showerror("Error", f"Error while solving: {str(e)}")
            
    def view_solution(self):
        try:
            # Load solution and data
            self.solution = pd.read_csv("solutions.csv", header=None).values[0]
            if len(self.solution) == 1:
                messagebox.showerror("Error", "No valid solution found")
                
            self.data_pd = pd.read_csv(self.selected_data_option, delimiter=';', header=None, names=['Investment', 'Cost', 'Return', 'Risk'])
          
            # Filter out non-selected investments
            selected_investments = self.data_pd[self.solution == 1.0]

            # Reset index
            selected_investments.reset_index(drop=True, inplace=True)

            # Get total cost, ROI and risk counts
            total_cost = selected_investments['Cost'].sum()
            total_return = selected_investments['Return'].sum()
            risk_counts = selected_investments['Risk'].value_counts()

            # Available capital and remaining capital after investments
            available_capital = self.validate_float(self.available_capital_entry.get())
            remaining_capital = available_capital - total_cost

            # Clear existing tree
            for i in self.tree.get_children():
                self.tree.delete(i)

            columns = ['Investments', 'Total Cost', 'Remaining Capital', 'ROI', 'Low Risk', 'Medium Risk', 'High Risk']
            self.tree['columns'] = columns
            for i, column in enumerate(self.tree['columns']):
                self.tree.column(column, anchor='center', minwidth=100, width=int(self.winfo_width()/len(columns)))  # Set the width of the columns
                self.tree.heading(column, text=column, anchor='center')

            # Insert data
            investments = ', '.join([str(i) for i in selected_investments['Investment']])
            if len(selected_investments) > 10:
                investments = 'Selected ' + str(len(selected_investments)) + ' Investments'
            self.tree.insert('', 'end', values=[investments, f"R$ {total_cost:.2f}", f"R$ {remaining_capital:.2f}", f"R$ {total_return:.2f}", risk_counts.get(0, 0), risk_counts.get(1, 0), risk_counts.get(2, 0)])

        except Exception as e:
            if len(self.solution) != 1:
                messagebox.showerror("Error", f"Error while viewing solution: {str(e)}")

if __name__ == "__main__":
    try:
        app = Application()
        app.mainloop()
    except Exception as e:
        print(f'Error in application: {str(e)}')
