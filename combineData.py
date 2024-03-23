import pandas as pd

# Load the CSV files into dataframes
df1 = pd.read_csv('deforrest.csv')
df2 = pd.read_csv('perCapita.csv')

# Merge the dataframes based on the "YEAR" and "COUNTRY" columns
mergedDF = pd.merge(df1, df2, on=['Year', 'Country'])

mergedDF = mergedDF[['Year', 'Country', 'Mean_deforestation', 'Mean_forest-regrowth', 'Mean_wood-harvest', 'Per-capita_Per-capita territorial']]

# Separate the merged dataframe into different dataframes based on the 'COUNTRY' column
correlationData = []
countryDFs = {}
for country, data in mergedDF.groupby('Country'):
    # Calculate the correlation coefficient between Mean_deforestation and Per-capita_Per-capita territorial
    correlationCoefficient = data['Mean_deforestation'].corr(data['Per-capita_Per-capita territorial'])
    correlationData.append({'Country': country, 'CorrelationCoefficient': correlationCoefficient})
    countryDFs[country] = data

# Save each country's dataframe to a separate CSV file
for country, df in countryDFs.items():
    filename = f"CountryData\{country}Data.csv"
    df.to_csv(filename, index=False)
    print(f"Data for {country} saved to {filename}")

# Create a new dataframe with country and correlation coefficient
correlationDF = pd.DataFrame(correlationData)

# Save the dataframe to a CSV file
correlationDF.to_csv('correlationCoefficients.csv', index=False)

print("Correlation coefficients saved to correlationCoefficients.csv")