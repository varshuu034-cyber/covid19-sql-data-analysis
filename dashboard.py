import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Configuration
st.set_page_config(page_title="COVID-19 Data Dashboard", page_icon="🦠", layout="wide")

st.title("🦠 COVID-19 Data Analysis Dashboard")
st.markdown("This dashboard is built using Python, SQLite, and Streamlit, querying a live/real COVID-19 dataset.")

# Function to connect to db and query
@st.cache_data
def load_data(query):
    conn = sqlite3.connect("covid_data.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

try:
    # ---------------------------
    # Top Level Metrics
    # ---------------------------
    st.header("Global Overview")
    global_query = """
    SELECT SUM(new_cases) AS total_cases, 
           SUM(CAST(new_deaths AS INT)) AS total_deaths
    FROM covid_deaths
    WHERE continent IS NOT NULL;
    """
    global_data = load_data(global_query)
    
    col1, col2, col3 = st.columns(3)
    if not global_data.empty:
        tot_cases = global_data['total_cases'][0]
        tot_deaths = global_data['total_deaths'][0]
        death_percent = (tot_deaths / tot_cases) * 100 if tot_cases else 0
        
        col1.metric("Total Global Cases", f"{tot_cases:,.0f}")
        col2.metric("Total Global Deaths", f"{tot_deaths:,.0f}")
        col3.metric("Global Death Percentage", f"{death_percent:.2f}%")

    st.divider()

    # ---------------------------
    # Highest Infection Rates
    # ---------------------------
    st.header("Countries with Highest Infection Rate")
    infection_query = """
    SELECT location, population, 
           MAX(total_cases) AS HighestInfectionCount, 
           MAX((CAST(total_cases AS FLOAT) / population)) * 100 AS PercentPopulationInfected
    FROM covid_deaths
    WHERE continent IS NOT NULL AND population > 1000000
    GROUP BY location, population
    ORDER BY PercentPopulationInfected DESC
    LIMIT 20;
    """
    infection_data = load_data(infection_query)
    
    fig1 = px.bar(infection_data, x="location", y="PercentPopulationInfected", 
                  color="PercentPopulationInfected",
                  title="Top 20 Countries by Infection Rate (%)",
                  labels={"location": "Country", "PercentPopulationInfected": "Infected (%)"},
                  color_continuous_scale="Reds")
    st.plotly_chart(fig1, use_container_width=True)

    st.divider()
    
    # ---------------------------
    # Total Deaths by Continent
    # ---------------------------
    st.header("Total Deaths by Continent")
    continent_query = """
    SELECT continent, 
           MAX(CAST(total_deaths AS INT)) AS TotalDeathCount
    FROM covid_deaths
    WHERE continent IS NOT NULL
    GROUP BY continent
    ORDER BY TotalDeathCount DESC;
    """
    continent_data = load_data(continent_query)
    
    fig2 = px.pie(continent_data, names="continent", values="TotalDeathCount", 
                  title="Total COVID-19 Deaths per Continent", hole=0.3)
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ---------------------------
    # Viewing Raw Data
    # ---------------------------
    st.header("Explore Raw Data")
    st.write("First 100 rows of the `covid_deaths` table:")
    raw_query = """
    SELECT location, date, total_cases, new_cases, total_deaths, population
    FROM covid_deaths
    WHERE continent IS NOT NULL
    ORDER BY date DESC
    LIMIT 100;
    """
    raw_data = load_data(raw_query)
    st.dataframe(raw_data)

except Exception as e:
    st.error(f"Error connecting to database or fetching data. Have you run `setup_database.py` yet? Details: {e}")
