import pandas as pd
import tkinter as tk
from tkinter import filedialog, Scale, Button, Label, Entry, messagebox, BooleanVar, Checkbutton
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview
import tkinter.font as font
from pulp import LpStatusOptimal, LpStatus
from generate_fake_data import generate_fake_data
from otimizacao_investimentos_linear_programming import InvestmentOptimizer
from otimizacao_investimentos_genetic_algorithm import GeneticAlgorithmOptimizer
from multiple_solutions_LP import get_n_best_solutions

import os

class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ENACOM - Otimização de Investimentos")  
        self.geometry('1280x600')

        self.data_options = ["data.csv", "fake_data.csv"]
        self.multiple_solutions_file = 'multiple_solutions.csv'
        self.solvers = ["Programação Linear (Determinístico, Ótimo)", "Algoritmo Genético (Estocástico)"]

        Label(self, text="Selecionar dados:").grid(column=0, row=0, sticky='e')
        self.data_cb = Combobox(self, values=self.data_options, width=50)
        self.data_cb.current(0)  
        self.data_cb.grid(column=1, row=0)

        self.load_button = Button(self, text="Carregar Dados", command=self.load_data)
        self.load_button.grid(column=1, row=1)

        Label(self, text="Capital disponível:").grid(column=0, row=2, sticky='e')
        self.available_capital_entry = Entry(self, width=50)
        self.available_capital_entry.insert(0, '2400000')
        self.available_capital_entry.grid(column=1, row=2)

        Label(self, text="Limite de custo (Baixo Risco, Médio Risco, Alto Risco):").grid(column=0, row=3, sticky='e')
        self.cost_limit_entry = Entry(self, width=50)
        self.cost_limit_entry.insert(0, '[1200000, 1500000, 900000]')
        self.cost_limit_entry.grid(column=1, row=3)

        Label(self, text="Mínimo por categoria (Baixo Risco, Médio Risco, Alto Risco):").grid(column=0, row=4, sticky='e')
        self.minimum_per_category_entry = Entry(self, width=50)
        self.minimum_per_category_entry.insert(0, '[2, 2, 1]')
        self.minimum_per_category_entry.grid(column=1, row=4)

        Label(self, text="Número de pontos de dados falsos:").grid(column=0, row=5, sticky='e')
        self.num_fake_data_points_entry = Entry(self, width=50)
        self.num_fake_data_points_entry.insert(0, '5000')
        self.num_fake_data_points_entry.grid(column=1, row=5)

        self.gen_button = Button(self, text="Gerar Dados Falsos", command=self.gen_data)
        self.gen_button.grid(column=1, row=6)

        Label(self, text="Selecionar solver:").grid(column=0, row=7, sticky='e')
        self.solver_cb = Combobox(self, values=self.solvers, width= 50)
        self.solver_cb.current(0)
        self.solver_cb.grid(column=1, row=7)

        self.solve_button = Button(self, text="Resolver", command=self.solve)
        self.solve_button.grid(column=1, row=8)

        self.solution_button = Button(self, text="Visualizar Solução", command=self.view_solution)
        self.solution_button.grid(column=1, row=9)
        
        self.tree = ttk.Treeview(self, show='headings')
        self.tree.grid(column=1, row=10)

        # Configurar a grade
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(10, weight=1)
        
        # Configurando o Treeview
        self.tree.grid(column=0, row=10, sticky='nsew', columnspan=2)
        
        # Adicionar checkbutton para habilitar ou desabilitar múltiplas soluções
        self.multiple_solutions = BooleanVar(value=False)
        self.multiple_solutions_cb = Checkbutton(self, text='Múltiplas soluções', variable=self.multiple_solutions)
        self.multiple_solutions_cb.grid(column=1, row=11)

        # Adicionar entrada para definir o número de soluções
        self.num_solutions_entry = tk.Entry(self, width=50)
        self.num_solutions_entry.insert(0, '5')
        self.num_solutions_entry.grid(column=1, row=12)

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
            messagebox.showerror("Erro", "A entrada deve ser um número inteiro positivo.")
            return None

    def validate_float(self, value):
        try:
            return float(value)
        except ValueError:
            messagebox.showerror("Erro", "A entrada deve ser um número flutuante.")
            return None

    def load_data(self):
        self.selected_data_option = self.data_cb.get()
        try:
            if self.selected_data_option == "data.csv":
                self.data = str(self.data_options[0])
                print('Dados: ' + str(self.data_options[0]) + ' carregados!')
            elif self.selected_data_option == "fake_data.csv":
                self.data = str(self.data_options[1])
                print('Dados: ' + str(self.data_options[1]) + ' carregados!')
            else:
                raise ValueError("Opção de dados inválida selecionada.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar os dados: {str(e)}")

    def gen_data(self):
        try:
            num_fake_data_points = self.validate_positive_integer(self.num_fake_data_points_entry.get())
            if num_fake_data_points is None:
                return

            self.data = generate_fake_data(num_fake_data_points)
            self.data_cb.set("fake_data.csv")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar dados falsos: {str(e)}")

    def solve(self):
        try:
            available_capital = self.validate_float(self.available_capital_entry.get())
            cost_limit = [self.validate_positive_integer(x) for x in eval(self.cost_limit_entry.get())]
            minimum_per_category = [self.validate_positive_integer(x) for x in eval(self.minimum_per_category_entry.get())]

            if None in cost_limit or None in minimum_per_category or available_capital is None:
                return
            solver = self.solver_cb.get()
            if self.data is None:  
                raise ValueError("Carregar dados primeiro!")
            else:            
                if self.multiple_solutions.get():
                    available_capital = self.validate_float(self.available_capital_entry.get())
                    cost_limit = [self.validate_positive_integer(x) for x in eval(self.cost_limit_entry.get())]
                    minimum_per_category = [self.validate_positive_integer(x) for x in eval(self.minimum_per_category_entry.get())]
                    num_solutions = self.validate_positive_integer(self.num_solutions_entry.get())
                    get_n_best_solutions(num_solutions, self.data, available_capital, cost_limit, minimum_per_category, singleobjective=True)
                else:
                    if solver == self.solvers[0]:
                        self.optimizer = InvestmentOptimizer(self.data, available_capital, cost_limit, minimum_per_category, singleobjective = True)
                    elif solver == self.solvers[1]:
                        self.optimizer = GeneticAlgorithmOptimizer(self.data, available_capital, cost_limit, minimum_per_category, singleobjective = True)
                    else:
                        raise ValueError("Seleção inválida do solver.")
                    
                self.optimizer.define_problem()
                self.optimizer.solve()
                solution = self.optimizer.get_results()
                self.optimizer.save_results(solution)
        except Exception as e: 
            messagebox.showerror("Erro", f"Erro enquanto resolvendo: {str(e)}")


    def view_solution(self):
        try:
            if self.multiple_solutions.get():
                self.solutions = pd.read_csv("multiple_solutions.csv", header=None)
            else:
                self.solutions = pd.read_csv("solutions.csv", header=None)

            self.data_pd = pd.read_csv(self.selected_data_option, delimiter=';', header=None, names=['Investimento', 'Custo', 'Retorno', 'Risco'])
            available_capital = self.validate_float(self.available_capital_entry.get())

            for i in self.tree.get_children():
                self.tree.delete(i)

            columns = ['Investimentos', 'Custo Total', 'Capital Restante', 'ROI', 'Risco Baixo', 'Risco Médio', 'Risco Alto']
            self.tree['columns'] = columns

            for i, column in enumerate(self.tree['columns']):
                self.tree.column(column, anchor='center', minwidth=100, width=int(self.winfo_width()/len(columns)))
                self.tree.heading(column, text=column, anchor='center')

            result_data = []
            for index, solution in self.solutions.iterrows():
                selected_investments = self.data_pd[solution == 1.0]
                selected_investments.reset_index(drop=True, inplace=True)
                total_cost = selected_investments['Custo'].sum()
                total_return = selected_investments['Retorno'].sum()
                risk_counts = selected_investments['Risco'].value_counts()
                remaining_capital = available_capital - total_cost

                investments = ', '.join([str(i) for i in selected_investments['Investimento']])
                if len(selected_investments) > 10:
                    investments = 'Selecionado ' + str(len(selected_investments)) + ' Investimentos'
                
                result_data.append([investments, total_cost, remaining_capital, total_return, risk_counts.get(0, 0), risk_counts.get(1, 0), risk_counts.get(2, 0)])

            result_data = sorted(result_data, key = lambda x: (x[3], -x[2])) # Ordenar por ROI e capital restante

            result_data = sorted(result_data, key = lambda x: (x[3], -x[2]), reverse=True)  # Ordenar por ROI e capital restante, em ordem decrescente

            for data in result_data:
                # Verifica se há outro resultado com o mesmo ROI e mais capital restante
                for other_data in result_data:
                    if data[3] == other_data[3] and data[2] < other_data[2]:
                        self.tree.insert('', 'end', values=data, tags=('strikethrough',))
                        self.tree.tag_configure('strikethrough', foreground='red')
                        break
                else:
                    self.tree.insert('', 'end', values=data)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao visualizar a solução: {str(e)}")

if __name__ == "__main__":
    try:
        app = Application()
        app.mainloop()
    except Exception as e:
        print(f'Erro na aplicação: {str(e)}')
