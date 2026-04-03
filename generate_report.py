import sqlite3
import pandas as pd

conn = sqlite3.connect('covid_data.db')

queries = {
    "Global COVID-19 Summary": """
        SELECT SUM(new_cases) AS total_cases, 
               SUM(CAST(new_deaths AS INT)) AS total_deaths,
               (SUM(CAST(new_deaths AS FLOAT)) / SUM(new_cases)) * 100 AS global_death_percentage
        FROM covid_deaths
        WHERE continent IS NOT NULL;
    """,
    "Top 10 Countries by Infection Rate (%)": """
        SELECT location, population, 
               MAX(total_cases) AS HighestInfectionCount, 
               MAX((CAST(total_cases AS FLOAT) / population)) * 100 AS PercentPopulationInfected
        FROM covid_deaths
        WHERE continent IS NOT NULL AND population > 1000000
        GROUP BY location, population
        ORDER BY PercentPopulationInfected DESC
        LIMIT 10;
    """,
    "Top 10 Countries by Total Death Count": """
        SELECT location, 
               MAX(CAST(total_deaths AS INT)) AS TotalDeathCount
        FROM covid_deaths
        WHERE continent IS NOT NULL 
        GROUP BY location
        ORDER BY TotalDeathCount DESC
        LIMIT 10;
    """
}

with open('output_report.md', 'w', encoding='utf-8') as f:
    f.write("# 📊 COVID-19 Data Analysis Output\n\n")
    f.write("Here are the real results generated from your SQLite database running the SQL queries:\n\n")
    
    for title, q in queries.items():
        df = pd.read_sql(q, conn)
        f.write(f"### {title}\n")
        f.write(df.to_markdown(index=False))
        f.write("\n\n")
        
conn.close()
print("Report generated at output_report.md")
