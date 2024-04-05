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

introText = """
**Understanding the Interplay of Population Growth, Deforestation, and Global Warming**\n
In a world where the consequences of our actions are becoming increasingly evident, it's paramount to grasp the intricate connections between human activity and the environment. Our website serves as a beacon of knowledge, shedding light on two critical pillars shaping our planet's future: population growth and deforestation.\n
**Visualizing Data**\n
Through insightful graphs and illustrations, we harness data sourced from authoritative bodies such as the Global Carbon Project and the UN Department of Economic and Social Affairs. These visual representations serve as windows into the complex dynamics shaping our world, offering clarity and comprehension amidst the sea of information.\n
**Population Growth**\n
With each passing moment, the global population swells, placing unprecedented demands on our planet's resources. While population growth signifies progress and vitality in societies worldwide, its ramifications ripple across social, economic, and environmental landscapes. From strained infrastructure to heightened competition for finite resources, the impacts are palpable.\n
**Deforestation**\n
In tandem with population growth, rampant deforestation further exacerbates the environmental challenges we face. The relentless pursuit of agricultural expansion and urban development has led to vast swaths of forests being cleared, disrupting ecosystems and accelerating climate change. The consequences are dire, threatening biodiversity, exacerbating carbon emissions, and jeopardizing the very balance of our planet.\n
**Consequences**\n
The repercussions of population growth and deforestation extend far beyond mere statistics. They manifest in tangible ways, shaping our societies, economies, and environments in profound ways. Social disparities widen as resources dwindle. Economies falter under the weight of unsustainable practices. And our planet suffers the irreversible scars of ecological degradation.\n
**Empowering Change Through Knowledge**\n
Yet, amidst the challenges lie opportunities for transformation. By understanding the interplay of population growth, deforestation, and global warming, we equip ourselves with the tools needed to enact meaningful change. Through education, advocacy, and collective action, we can forge a path towards a more sustainable future, one where harmony between humanity and the natural world is not just a distant dream but a tangible reality.\n
**Explore, Learn, Act**\n
Join us as we embark on a journey of discovery, navigating the intersections of population growth, deforestation, and global warming. Through the lens of data and the power of visualization, let us illuminate pathways towards a more equitable, sustainable world—for the benefit of all inhabitants, present and future.\n
"""

# Load your data
data = pd.read_csv('Data.csv')

introTab, popTab, defoTab, compTab, leaderTab = st.tabs(['Preamble', 'Population', 'Deforestation', 'Comparisons', 'Leaderboards'])

def display_footer():
    st.markdown("---")
    st.write("GitHub Repository: https://github.com/EDaley-FlemCollege/GNED166-Final")
    with st.container(border=True):
        st.write("Data Sources")
        st.write('The Global Carbon Budget 2023 (Friedlingstein et al., 2023b, ESSD)')
        st.write('United Nations, Department of Economic and Social Affairs, Population Division (2022). World Population Prospects 2022, Online Edition.')

with introTab:
    st.title(f'Welcome to Daley Stats')
    st.markdown(introText)

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

with compTab:
    # List of all available countries
    countries = data['Country'].unique()
    stats = data.columns.tolist()

    # Create a dropdown selectbox
    selectedStat = st.selectbox('Select Statistic', stats[2:], key='compTabSC')

    # Multiselect widget to select countries
    selectedCountries = st.multiselect('Select countries', [getCountryName(c) for c in countries])

    # Get the alpha-3 country codes for selected countries one by one
    selectedCountryCodes = [getAlpha3(country) for country in selectedCountries]

    # Filter the DataFrame for selected countries
    filteredData = data[data['Country'].isin(selectedCountryCodes)]

    if not filteredData.empty: 
        # Display data
        catDF = pd.DataFrame()
        for code, info in filteredData.groupby('Country'):
            info = info[['Year', selectedStat]].set_index('Year').rename(columns={selectedStat: getCountryName(code)})
            catDF = pd.concat([catDF, info], axis=1)
        st.line_chart(catDF)
    else:
        st.write(f"No data selected.")


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

# Display source and GitHub link on all tabs
display_footer()