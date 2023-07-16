import matplotlib.pyplot as plt
from otimizacao_investimentos_prog_linear import InvestmentOptimizer

CAPITAL_START = 1000
CAPITAL_END = 5000001
CAPITAL_STEP = 10000
COST_LIMIT = [1200000, 1500000, 900000]
MINIMUM_PER_CATEGORY = [2, 2, 1]
# UNLIMITED_COST_LIMIT = [1e20, 1e20, 1e20]  # Very high cost limits
# ZERO_MINIMUM_PER_CATEGORY = [0, 0, 0]  # Zero minimum per category
DATA_FILE = 'data.csv'
FIGURE_SIZE = (10, 6)

def optimize_investment(capital, rois, successful_capitals, cost_limit, minimum_per_category, multiobjective):
    try:
        optimizer = InvestmentOptimizer(DATA_FILE, available_capital = capital, 
                                        cost_limit = cost_limit, 
                                        minimum_per_category = minimum_per_category, multiobjective = multiobjective)
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

def main():
    capitals = range(CAPITAL_START, CAPITAL_END, CAPITAL_STEP)
    
    # Define the result lists for both instances
    successful_capitals = []  # List to save successful capitals.
    rois = []  # List to save ROIs for each successful capital.
    successful_capitals_efficiency = []  # List to save successful capitals for the efficiency case.
    rois_efficiency = []  # List to save ROIs for each successful capital for the efficiency case.

    for capital in capitals:
        optimize_investment(capital, rois, successful_capitals, COST_LIMIT, MINIMUM_PER_CATEGORY, True)
        optimize_investment(capital, rois_efficiency, successful_capitals_efficiency, COST_LIMIT, MINIMUM_PER_CATEGORY, False)

    # Plotting available capital vs. ROI
    plt.figure(figsize=FIGURE_SIZE)
    plot_roi_vs_capital(successful_capitals, rois, 'Maximizar ROI')
    plot_roi_vs_capital(successful_capitals_efficiency, rois_efficiency, 'Maximizar Eficiência do Investimento')
    plt.xlabel('Capital Disponível (R$)')
    plt.ylabel('Retorno sobre o Investimento(ROI, R$)')
    plt.title('Capital Disponível vs. ROI')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
