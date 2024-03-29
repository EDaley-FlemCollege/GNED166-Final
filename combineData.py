import pandas as pd
import pycountry

# Load the CSV files into dataframes
df1 = pd.read_csv('deforrest.csv')
df2 = pd.read_csv('perCapita.csv')

# Merge the dataframes based on the "YEAR" and "COUNTRY" columns
mergedDF = pd.merge(df1, df2, on=['Year', 'Country'])

mergedDF = mergedDF[['Year', 'Country', 'Mean_deforestation', 'Mean_forest-regrowth', 'Mean_wood-harvest', 'Per-capita_Per-capita territorial', 'Per-capita_Per-capita consumption']]

# Separate the merged dataframe into different dataframes based on the 'COUNTRY' column
correlationData = []
countryDFs = {}
for code, data in mergedDF.groupby('Country'):
    # Calculate the correlation coefficient between Mean_deforestation and Per-capita_Per-capita territorial
    defTerCorr = data['Mean_deforestation'].corr(data['Per-capita_Per-capita territorial'])
    harTerCorr = data['Mean_wood-harvest'].corr(data['Per-capita_Per-capita territorial'])
    defConCorr = data['Mean_deforestation'].corr(data['Per-capita_Per-capita consumption'])
    harConCorr = data['Mean_wood-harvest'].corr(data['Per-capita_Per-capita consumption'])
    try:
        country = pycountry.countries.get(alpha_3=code).name
    except AttributeError:
        country = code
    correlationData.append({
                        'Country': country, 
                        'Deforestation-Territorial Correlation': defTerCorr, 
                        'Harvest-Territorial Correlation': harTerCorr, 
                        'Deforestation-Consumption Correlation': defConCorr, 
                        'Harvest-Consumption Correlation': harConCorr
                        })
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