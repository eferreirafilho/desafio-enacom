import pandas as pd
import random
import csv

# Number of data points to generate
num_data_points = 10000

# Investment names (for simplicity, just numbers converted to strings)
investments = [str(i) for i in range(1, num_data_points+1)]

# Cost of investments (random integers between 50,000 and 1,000,000)
costs = [random.randint(50000, 1000000) for _ in range(num_data_points)]

# Returns of investments (random integers between 80,000 and 900,000)
returns = [random.randint(80000, 900000) for _ in range(num_data_points)]

# Risk categories (random choice between 0, 1, 2)
risks = [random.choice([0, 1, 2]) for _ in range(num_data_points)]

# Combine the lists into a data frame
data = pd.DataFrame({
    'Investment': investments,
    'Cost': costs,
    'Return': returns,
    'Risk': risks
})

# Save the data to a CSV file
data.to_csv('fake_data.csv', sep=';', index=False, header=False)
