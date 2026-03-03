"""
Testing taking csv and plotting
"""

# pip install pandas 
import pandas as pd

# Read the csv file
data = pd.read_csv('Most_Simple_model_-_Lines_1_2.csv',sep='\t',header=1)

# Print it out if you want
print(data)