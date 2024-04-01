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
        st.write(f"Data for {selectedCountry}")
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
        st.write(f"Data for {selectedCountry}")
        st.line_chart(filteredData, x='Year', y=['Deforestation-Increase', 'Harvest-Increase', 'Total-Territorial-Increase'])
    else:
        st.write(f"No data available for {selectedCountry}.")

with leaderTab:
    titleList = ['Population', 'Deforestation', 'Per-Capita Territorial Emissions', 'Per-Capita Consumption Emissions', 'Total Territorial Emissions', 'Total Consumption Emissions']
    st.title(f'Leaderboard Data')
    row1 = st.columns(2)
    row2 = st.columns(2)
    row3 = st.columns(2)
    for i,col in enumerate(row1 + row2 + row3) :
        tile = col.container(height=200)
        tile.write(titleList[i])