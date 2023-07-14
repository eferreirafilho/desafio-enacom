import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('previous_solutions.csv')

# Extract the values from the DataFrame
total_roi = df['total_roi']
total_spent = df['total_spent']
roi_spent_ratio = total_spent / total_roi

# Plotting Money Spent/ROI ratio
plt.scatter(roi_spent_ratio, total_roi)
plt.title('Money Spent/ROI Ratio vs Total ROI')
plt.xlabel('Money Spent/ROI Ratio')
plt.ylabel('Total ROI')

# Add labels for each data point
for i, txt in enumerate(roi_spent_ratio):
    plt.annotate(txt, (roi_spent_ratio[i], total_roi[i]), xytext=(-10, 10), textcoords='offset points')

# Display the plot
plt.show()
