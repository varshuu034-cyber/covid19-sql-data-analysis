import pandas as pd
import sqlite3
import os

def setup_db():
    print("Downloading COVID-19 dataset from Our World in Data (this may take a minute)...")
    url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
    
    # We will read only the columns we need to keep the database lightweight and fast
    columns_to_keep = [
        'iso_code', 'continent', 'location', 'date', 'population', 
        'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
        'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
        'new_vaccinations', 'gdp_per_capita'
    ]
    
    # Read CSV
    df = pd.read_csv(url, usecols=columns_to_keep)
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"Data downloaded successfully. Shape: {df.shape}")
    
    # We will split this into two tables for better SQL practice:
    # 1. covid_deaths
    deaths_cols = ['iso_code', 'continent', 'location', 'date', 'population', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'gdp_per_capita']
    df_deaths = df[deaths_cols].copy()
    
    # 2. covid_vaccinations
    vacc_cols = ['iso_code', 'continent', 'location', 'date', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations']
    df_vaccinations = df[vacc_cols].copy()
    
    # Connect to SQLite
    db_path = 'covid_data.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed old database.")
        
    conn = sqlite3.connect(db_path)
    print("Connected to SQLite Database.")
    
    # Load into db
    print("Loading 'covid_deaths' table...")
    df_deaths.to_sql('covid_deaths', conn, index=False, if_exists='replace')
    
    print("Loading 'covid_vaccinations' table...")
    df_vaccinations.to_sql('covid_vaccinations', conn, index=False, if_exists='replace')
    
    print("Database setup complete! 'covid_data.db' is ready for analysis.")
    conn.close()

if __name__ == "__main__":
    setup_db()
