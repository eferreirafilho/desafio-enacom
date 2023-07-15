import matplotlib.pyplot as plt
from otimizacao_investimentos_linear_programming import InvestmentOptimizer
import csv

CAPITAL_START = 1000
CAPITAL_END = 5000001
CAPITAL_STEP = 10000
COST_LIMIT = [1200000, 1500000, 900000]
MINIMUM_PER_CATEGORY = [2, 2, 1]
# UNLIMITED_COST_LIMIT = [1e20, 1e20, 1e20]  # Very high cost limits
# ZERO_MINIMUM_PER_CATEGORY = [0, 0, 0]  # Zero minimum per category
DATA_FILE = 'data.csv'
FIGURE_SIZE = (10, 6)

def optimize_investment(capital, rois, successful_capitals, cost_limit, minimum_per_category, singleobjective):
    try:
        optimizer = InvestmentOptimizer(DATA_FILE, available_capital = capital, 
                                        cost_limit = cost_limit, 
                                        minimum_per_category = minimum_per_category, singleobjective = singleobjective)
        optimizer.define_problem()
        optimizer.solve()
        solution = optimizer.get_results()  # Get the solution
        rois.append(optimizer.total_roi)  # Append ROI to the list.
        successful_capitals.append(capital)  # Append successful capital to the list.
        optimizer.save_results(solution)  # Save the solution to a CSV file
    except Exception as e:
        print(f"An error occurred with capital {capital}: {e}")

def plot_roi_vs_capital(successful_capitals, rois, label):
    plt.plot(successful_capitals, rois, label=label)
    
def optimize_investment_spent(capital, rois, spent_capitals, cost_limit, minimum_per_category, singleobjective):
    try:
        optimizer = InvestmentOptimizer(DATA_FILE, available_capital = capital, 
                                        cost_limit = cost_limit, 
                                        minimum_per_category = minimum_per_category, singleobjective = singleobjective)
        optimizer.define_problem()
        optimizer.solve()
        solution = optimizer.get_results()  # Get the solution
        rois.append(optimizer.total_roi)  # Append ROI to the list.
        spent_capitals.append(optimizer.total_spent)  # Append spent capital to the list.
        optimizer.save_results(solution)  # Save the solution to a CSV file
    except Exception as e:
        print(f"An error occurred with capital {capital}: {e}")

def plot_spent_vs_roi(spent_capitals, rois, label):
    plt.plot(spent_capitals, rois, label=label)

def main():
    capitals = range(CAPITAL_START, CAPITAL_END, CAPITAL_STEP)
    
    # Define the result lists for both instances
    successful_capitals = []  # List to save successful capitals.
    rois = []  # List to save ROIs for each successful capital.
    successful_capitals_efficiency = []  # List to save successful capitals for the efficiency case.
    rois_efficiency = []  # List to save ROIs for each successful capital for the efficiency case.
    
    spent_capitals = []  # List to save spent capitals.
    spent_rois = []  # List to save ROIs for each spent capital.
    spent_capitals_efficiency = []  # List to save spent capitals for the efficiency case.
    spent_rois_efficiency = []  # List to save ROIs for each spent capital for the efficiency case.

    for capital in capitals:
        optimize_investment(capital, rois, successful_capitals, COST_LIMIT, MINIMUM_PER_CATEGORY, True)
        optimize_investment(capital, rois_efficiency, successful_capitals_efficiency, COST_LIMIT, MINIMUM_PER_CATEGORY, False)
        
        optimize_investment_spent(capital, spent_rois, spent_capitals, COST_LIMIT, MINIMUM_PER_CATEGORY, True)
        optimize_investment_spent(capital, spent_rois_efficiency, spent_capitals_efficiency, COST_LIMIT, MINIMUM_PER_CATEGORY, False)


    efficient_points = [(c_eff, r_eff) for c, r, c_eff, r_eff in zip(spent_capitals, rois, spent_capitals_efficiency, rois_efficiency) 
                    if r == r_eff and c_eff < c]

    efficient_capitals, efficient_rois = zip(*efficient_points)
    
    
    efficient_cases = [{'capital': c, 'roi': r, 'capital_eff': c_eff, 'roi_eff': r_eff} 
                   for c, r, c_eff, r_eff in zip(spent_capitals, rois, spent_capitals_efficiency, rois_efficiency) 
                   if r == r_eff and c_eff < c]


    fig, axs = plt.subplots(2, figsize=FIGURE_SIZE)
    
    # Plotting available capital vs. ROI
    axs[0].plot(successful_capitals, rois, label='Maximizar ROI')
    axs[0].plot(successful_capitals_efficiency, rois_efficiency, label='Maximizar Eficiência do Investimento')
    axs[0].set_xlabel('Capital Disponível (R$)')
    axs[0].set_ylabel('Retorno sobre o Investimento(ROI, R$)')
    axs[0].set_title('Capital Disponível vs. ROI')
    axs[0].legend()
    axs[0].grid(True)
    
   # Plotting money spent vs. ROI
    axs[1].plot(spent_capitals, spent_rois, label='Maximizar ROI')
    axs[1].plot(spent_capitals_efficiency, spent_rois_efficiency, label='Maximizar Eficiência do Investimento')

    # axs[0].scatter(successful_capitals_efficiency, rois_efficiency, color='blue', label='Maximizar Eficiência do Investimento')
    # axs[0].scatter(efficient_capitals, efficient_rois, color='red', label='Menos Dinheiro Gasto para o Mesmo ROI')

    axs[1].scatter(spent_capitals_efficiency, rois_efficiency, color='blue', label='Maximizar Eficiência do Investimento')
    axs[1].scatter(efficient_capitals, efficient_rois, color='red', label='Menos Dinheiro Gasto para o Mesmo ROI')

    axs[1].set_xlabel('Dinheiro Gasto (R$)')
    axs[1].set_ylabel('Retorno sobre o Investimento(ROI, R$)')
    axs[1].set_title('Dinheiro Gasto vs. ROI')
    axs[1].legend()
    axs[1].grid(True)
    
    plt.tight_layout()
    plt.show()
    
    with open('efficient_cases.csv', 'w', newline='') as csvfile:
        fieldnames = ['capital', 'roi', 'capital_eff', 'roi_eff']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for case in efficient_cases:
            writer.writerow(case)


if __name__ == "__main__":
    main()
