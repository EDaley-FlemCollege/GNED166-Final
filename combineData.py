import pandas as pd

# Load the CSV files into dataframes
df1 = pd.read_csv('deforrest.csv')
df2 = pd.read_csv('perCapita.csv')

# Merge the dataframes based on the "YEAR" and "COUNTRY" columns
mergedDf = pd.merge(df1, df2, on=['Year', 'Country'])

mergedDf = mergedDf[['Year', 'Country', 'Mean_deforestation', 'Mean_forest-regrowth', 'Mean_wood-harvest', 'Mean_GFED4_peat', 'Per-capita_Per-capita territorial']]

# Output the merged dataframe to a CSV file
mergedDf.to_csv('mergedData.csv', index=False)

print("Merged data saved to mergedData.csv")
