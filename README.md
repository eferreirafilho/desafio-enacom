# Optimization and Python Challenge


This project is an investment optimization application that uses linear programming and genetic algorithm to find the best set of investments based on available capital, cost limit and minimum per category. This application is implemented in Python and uses the tkinter library for the graphical user interface.
Requirements

     Python 3.x
     Python libraries: pandas, tkinter, pulp, numpy, matplotlib, deap


## Installation Instructions

Clone this repository or download the source code.
Make sure Python is installed on your system.
Install the necessary libraries. If you are using pip you can do this by running

     pip install pandas tkinter pulp numpy matplotlib deap.

## How to use

Run the python file

     optimization_gui.py

The application will launch and you will see the graphical user interface.

![Alt text](/images/image-5.png)

Select the data you want to use for optimization. By default you can choose between "data.csv" and "fake_data.csv"

We call the following instance "standard problem" (This is the instance saved in data.csv.):

![Alt text](/images/enacom.png)

Enter the available capital, cost limit and minimum per category.
Choose the type of solver you want to use: Linear Programming (Deterministic, Optimal) or Genetic Algorithm (Stochastic).
Click the "Resolve" button to start optimization. The solution will be saved to a CSV file.
You can preview the solution by clicking the "View Solution" button.
If you want to generate and use fake data, enter the number of fake data points and click "Generate Fake Data".
The application also supports multiple solutions. To enable this, check the 'Multiple solutions' option and enter the number of solutions desired.

It is also possible to run the Linear Programming solution or the genetic algorithm separately, just run the files *otimizacao_investimentos_prog_linear.py* or *programacao_investimentos_algo_genetico.py*, respectively.

## Functionalities

**Load Data:** Allows the user to load data to be used in optimization.

**Generate Fake Data:** Generates a set of fake data based on the number of fake data points provided by the user.

**Solve:** Starts optimization based on user-supplied parameters.

**View Solution:** Shows the optimization solution in a table.

**Multiple Solutions:** Provides the option to obtain multiple solutions to the optimization problem.

## Results (standard problem)

- Investment 1 - Cost: 470,000, Return: 410000, Risk: Low
- Investment 2 - Cost: 400,000, Return: 330000, Risk: Low
- Investment 4 - Cost: 270,000, Return: 250000, Risk: Medium
- Investment 5 - Cost: 340,000, Return: 320000, Risk: Medium
- Investment 6 - Cost: 230,000, Return: 320000, Risk: Medium
- Investment 7 - Cost: 50,000, Return: 90000, Risk: Medium
- Investment 9 - Cost: 320,000, Return: 120000, Risk: High
- Investment 13 - Cost: 300,000, Return: 380000, Risk: Medium

Investments by risk category:
Low: [1, 2]
Medium: [4, 5, 6, 7, 13]
High: [9]

- Total ROI = 2,220,000
- Total Spent = 2,380,000
- Available - Spent = 20,000
- Status: Optimal Solution

Varying available capital:

![Alt text](/images/image.png)

## Other Analysis

### Maximize ROI and maximize efficiency

![Alt text](/images/image-1.png)

### Maximize ROI and minimize risk

![Alt text](/images/image-2.png)

### Maximize ROI and minimize expenses

![Alt text](/images/image-3.png)

Red dots (less money spent for the same ROI):

![Alt text](/images/image-4.png)

## Unitary tests

- Checks whether the optimization problem has been defined correctly.
- Checks whether solving the optimization problem returns an optimal state.
- Tests whether the results are returned correctly and ensures that the variables are within pre-defined limits.
- Checks if the class returns an error when the input file is not valid.
- Checks if the class returns an error when the input file does not exist.
- Tests whether the class returns an error when the data file is empty.
- Checks if the class returns an error when the available capital is invalid.
- Checks if the class returns an error when the available capital is zero.
- Checks if the class returns an error when the minimum per category is unfeasible.
- Checks whether the class returns an error when the cost limits are unfeasible.

