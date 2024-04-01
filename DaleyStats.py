import streamlit as st
import pandas as pd
import numpy as np
import pycountry

def getCountryName(code):
    try:
        country = pycountry.countries.get(alpha_3=code)
        return country.name
    except AttributeError:
        return None

def getAlpha3(countryName):
    try:
        country = pycountry.countries.get(name=countryName)
        return country.alpha_3
    except AttributeError:
        return None

# Load your data
data = pd.read_csv('Data.csv')

popTab, defoTab, compTab, leaderTab = st.tabs(['Population', 'Deforestation', 'Comparisons', 'Leaderboards'])

with popTab:
    # Get unique country names
    countries = data['Country'].unique()

    # Create a dropdown selectbox
    selectedCountry = st.selectbox('Select Country', [getCountryName(c) for c in countries], key='popTabSC')

    # Streamlit app
    st.title(f'Population Data for {selectedCountry}')

    # Filter data by selected country
    filteredData = data[data['Country'] == getAlpha3(selectedCountry)]

    # Display data by Country
    if not filteredData.empty: 
        # Display data
        st.line_chart(filteredData, x='Year', y=['Population-Increase', 'PerCap-Territorial-Increase', 'Total-Territorial-Increase'])
    else:
        st.write(f"No data available for {selectedCountry}.")

with defoTab:
    # Get unique country names
    countries = data['Country'].unique()

    # Create a dropdown selectbox
    selectedCountry = st.selectbox('Select Country', [getCountryName(c) for c in countries], key='defoTabSC')

    # Streamlit app
    st.title(f'Deforestation Data for {selectedCountry}')

    # Filter data by selected country
    filteredData = data[data['Country'] == getAlpha3(selectedCountry)]

    # Display data by Country
    if not filteredData.empty: 
        # Display data
        st.line_chart(filteredData, x='Year', y=['Deforestation-Increase', 'Harvest-Increase', 'Total-Territorial-Increase'])
    else:
        st.write(f"No data available for {selectedCountry}.")

with leaderTab:
    # Get unique Years names
    years = data['Year'].unique()

    # Create a dropdown selectbox
    selectedYear = st.selectbox('Select Year', years, key='leaderTabSC')

    # Filter data by selected year
    filteredData = data[data['Year'] == selectedYear]

    topPop = filteredData.nlargest(5, 'Population')
    topPop = topPop.reset_index(drop=True)
    topPop['Placement'] = topPop.index + 1
    topPop['Country'] = topPop['Country'].apply(getCountryName)
    topPop = topPop[['Placement', 'Country', 'Population']]

    topDefo = filteredData.nlargest(5, 'Deforestation')
    topDefo = topDefo.reset_index(drop=True)
    topDefo['Placement'] = topDefo.index + 1
    topDefo['Country'] = topDefo['Country'].apply(getCountryName)
    topDefo = topDefo[['Placement', 'Country', 'Deforestation']]

    topPerTerr = filteredData.nlargest(5, 'PerCap-Territorial')
    topPerTerr = topPerTerr.reset_index(drop=True)
    topPerTerr['Placement'] = topPerTerr.index + 1
    topPerTerr['Country'] = topPerTerr['Country'].apply(getCountryName)
    topPerTerr = topPerTerr[['Placement', 'Country', 'PerCap-Territorial']]

    topPerCon = filteredData.nlargest(5, 'PerCap-Consumption')
    topPerCon = topPerCon.reset_index(drop=True)
    topPerCon['Placement'] = topPerCon.index + 1
    topPerCon['Country'] = topPerCon['Country'].apply(getCountryName)
    topPerCon = topPerCon[['Placement', 'Country', 'PerCap-Consumption']]

    toptotalTerr = filteredData.nlargest(5, 'Total-Territorial')
    toptotalTerr = toptotalTerr.reset_index(drop=True)
    toptotalTerr['Placement'] = toptotalTerr.index + 1
    toptotalTerr['Country'] = toptotalTerr['Country'].apply(getCountryName)
    toptotalTerr = toptotalTerr[['Placement', 'Country', 'Total-Territorial']]

    topTotalCon = filteredData.nlargest(5, 'Total-Consumption')
    topTotalCon = topTotalCon.reset_index(drop=True)
    topTotalCon['Placement'] = topTotalCon.index + 1
    topTotalCon['Country'] = topTotalCon['Country'].apply(getCountryName)
    topTotalCon = topTotalCon[['Placement', 'Country', 'Total-Consumption']]

    #Tables
    titleList = ['Population', 'Deforestation', 'Per-Capita Territorial Emissions', 'Per-Capita Consumption Emissions', 'Total Territorial Emissions', 'Total Consumption Emissions']
    tableList = [topPop, topDefo, topPerTerr, topPerCon, toptotalTerr, topTotalCon]
    st.title(f'Leaderboard Data')
    for i in range(6) :
        st.write(titleList[i])  # Write the title
        st.table(tableList[i].set_index('Placement', drop=True))  # Display the corresponding table without index column