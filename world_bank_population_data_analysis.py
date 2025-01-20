# -*- coding: utf-8 -*-
"""World Bank Population Data Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1b_BAR3grF9KYq9l5Zg3DYw5MiBKoD8Hn
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from google.colab import files
uploaded = files.upload()

# Assuming the uploaded file is named 'yourfile.csv'
df = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_900.csv',skiprows=4,header=0)
Metadata_Country = pd.read_csv('Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_900.csv')
Metadata_Indicator = pd.read_csv('Metadata_Indicator_API_SP.POP.TOTL_DS2_en_csv_v2_900.csv')

# Display the first few rows of the DataFrame
df.head()

df.info()

Metadata_Country.head()

Metadata_Indicator.head()

merged_df = pd.merge(df, Metadata_Country, on='Country Code', how='left')
merged_df.head()

merged_df.info()

pd.isnull(merged_df).sum()

merged_df.drop(columns=['Country Code','Indicator Name','Indicator Code','SpecialNotes','Unnamed: 5'],axis=1,inplace=True)

pd.set_option('display.max_columns', None)
merged_df.head()

merged_df.info()

merged_df.describe()

merged_df.describe(include='object')

from scipy import stats
from scipy.stats import zscore

def detect_outliers_zscore(merged_df, threshold=3):
    numeric_columns = merged_df.select_dtypes(include=[np.number]).columns  # Choosing only numeric columns, fixed syntax error
    numeric_data = merged_df[numeric_columns].T
    z_scores = np.abs(stats.zscore(numeric_data, axis=0))
    outliers = (z_scores > threshold).any(axis=0)
    return outliers, z_scores.T

outliers, z_scores = detect_outliers_zscore(merged_df)    # Calling the function with correct name
# Display rows with outliers
outliers_df = merged_df[outliers]  # Fixed variable name to outliers_df
print("Rows with Outliers:")
print(outliers_df)

columns_of_interest = ['Country Name'] + [str(year) for year in range(1960, 2023)]
data_subset = merged_df[columns_of_interest]
# Choose three countries for visualization
countries_to_plot = ['Dominica', 'Guyana', 'Ukraine']
# Filter data for the selected countries
data_subset_countries = data_subset[data_subset['Country Name'].isin(countries_to_plot)]

melted_data = pd.melt(data_subset_countries, id_vars='Country Name', var_name='Year', value_name='Population')
# Create a line plot to visualize the data distribution for three countries
plt.figure(figsize=(14, 4))
sns.lineplot(x="Year", y='Population', hue='Country Name', data=melted_data, marker="o")
plt.title('Population Data Distribution for Selected Countries (1961-2022)')
plt.xlabel('Year')
plt.ylabel('Population')
plt.xticks(rotation=45, ha="right",fontsize=8)
plt.show()
# print("The graph clearly shows that Ukraine population is on decline, whereas in other two countries no significant positive trend is being observe")

year_to_visualize = 2021

# Create the bar chart
plt.figure(figsize=(12, 6))
sns.histplot(merged_df[str(year_to_visualize)], kde=True) # Use histplot for better visualization
plt.title(f'Population Distribution in {year_to_visualize}')
plt.xlabel('Population')
plt.ylabel('Frequency')
plt.show()

# Choose a year to visualize
year_to_visualize = 2023

# Create the bar chart
plt.figure(figsize=(12, 6))
sns.histplot(merged_df[str(year_to_visualize)], kde=False, bins=30)
plt.title(f'Population Distribution in {year_to_visualize}')
plt.xlabel('Population')
plt.ylabel('Frequency')
plt.show()

#  visualize the distribution of 'Region'
plt.figure(figsize=(8, 6))
sns.countplot(x='Region', data=merged_df) # Changed