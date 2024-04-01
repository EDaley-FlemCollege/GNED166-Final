import pandas as pd
import pycountry
import datetime

def main():
    fixUnData('UnPop.csv')
    mainDF = createDf()
    saveDf('Data', mainDF)
    corrDF = createCountryDf(mainDF)
    #saveDf('correlationCoefficients', corrDF)

def getAlpha3(countryName):
    try:
        country = pycountry.countries.get(name=countryName)
        return country.alpha_3
    except AttributeError:
        return None

def fixUnData(path):
    unDF = pd.read_csv(path)
    unDF = unDF[['Location', 'Time', 'PopTotal']]
    # Apply the function to convert country names to alpha-3 codes
    unDF['Location'] = unDF['Location'].apply(lambda x: getAlpha3(x) if pd.notnull(x) else None)
    # Drop records where alpha-3 code is not found
    unDF = unDF.dropna(subset=['Location'])
    # Drop rows where 'Time' is in a future year
    unDF = unDF[unDF['Time'] <= datetime.datetime.now().year]
    # Rename 'Location' column to 'Country' and 'Time' column to 'Year'
    unDF = unDF.rename(columns={'Location': 'Country', 'Time': 'Year'})
    # Drop duplicate entries based on 'Country' and 'Year'
    unDF = unDF.drop_duplicates(subset=['Country', 'Year'])
    saveDf('population', unDF)

def createDf() :
    # Load the CSV files into dataframes
    df1 = pd.read_csv('deforrest.csv')
    df2 = pd.read_csv('perCapita.csv')
    df3 = pd.read_csv('population.csv')
    # Merge the dataframes based on the "YEAR" and "COUNTRY" columns
    mergedDF = pd.merge(df1, df2, on=['Year', 'Country'])
    mainDF = pd.merge(mergedDF, df3, on=['Year', 'Country'])
    mainDF = mainDF[['Year', 'Country', 'PopTotal', 'Mean_deforestation', 'Mean_wood-harvest', 'Per-capita_Per-capita territorial', 'Per-capita_Per-capita consumption']]
    mainDF = mainDF.rename(columns={
                                    'PopTotal' : 'Population', 
                                    'Mean_deforestation' : 'Deforestation', 
                                    'Mean_wood-harvest' : 'Harvest', 
                                    'Per-capita_Per-capita territorial' : 'PerCap-Territorial',
                                    'Per-capita_Per-capita consumption' : 'PerCap-Consumption'})
    # Add new columns 'Total Territorial' and 'Total Consumption'
    mainDF['Total-Territorial'] = mainDF['Population'] * mainDF['PerCap-Territorial']
    mainDF['Total-Consumption'] = mainDF['Population'] * mainDF['PerCap-Consumption']
    return mainDF

def saveDf(name, data, index=False) :
    data.to_csv(f'{name}.csv', index=index)
    print(f"Data for {data} saved to {name}")
    return f'{name}.csv'

def createCountryDf(data) :
    # Separate the merged dataframe into different dataframes based on the 'COUNTRY' column
    correlationData = []
    countryDFs = {}
    for code, data in data.groupby('Country'):
        # Calculate the correlation coefficient between Mean_deforestation and Per-capita_Per-capita territorial
        defTerCorr = data['Deforestation'].corr(data['PerCap-Territorial'])
        harTerCorr = data['Harvest'].corr(data['PerCap-Territorial'])
        defConCorr = data['Deforestation'].corr(data['PerCap-Consumption'])
        harConCorr = data['Harvest'].corr(data['PerCap-Consumption'])
        correlationData.append({
                            'Country': code, 
                            'Deforestation-Territorial': defTerCorr, 
                            'Harvest-Territorial': harTerCorr, 
                            'Deforestation-Consumption': defConCorr, 
                            'Harvest-Consumption': harConCorr
                            })
        countryDFs[code] = data
    # Save each country's dataframe to a separate CSV file
    for country, df in countryDFs.items():
        filename = f"CountryData/{country}"
        saveDf(filename, df)
    # Create a new dataframe with country and correlation coefficient
    correlationDF = pd.DataFrame(correlationData)
    return correlationDF

if __name__ == '__main__':
    main()