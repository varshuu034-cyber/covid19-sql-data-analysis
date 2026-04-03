import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set aesthetics
sns.set_theme(style="whitegrid")

# Connect to database
conn = sqlite3.connect('covid_data.db')

# 1. Top 15 Countries by Infection Rate (%)
q1 = """
SELECT location, 
       MAX((CAST(total_cases AS FLOAT) / population)) * 100 AS PercentPopulationInfected
FROM covid_deaths
WHERE continent IS NOT NULL AND population > 1000000
GROUP BY location
ORDER BY PercentPopulationInfected DESC
LIMIT 15;
"""
df1 = pd.read_sql(q1, conn)

plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(
    data=df1, 
    x="PercentPopulationInfected", 
    y="location", 
    palette="Reds_r"
)
plt.title('Top 15 Countries by COVID-19 Infection Rate (%)', fontsize=16)
plt.xlabel('Infected Population (%)', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.tight_layout()
plt.savefig('infection_rates.png', dpi=300)
plt.close()

# 2. Total Deaths by Continent
q2 = """
SELECT continent, 
       MAX(CAST(total_deaths AS INT)) AS TotalDeathCount
FROM covid_deaths
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY TotalDeathCount DESC;
"""
df2 = pd.read_sql(q2, conn)

plt.figure(figsize=(8, 8))
plt.pie(
    df2['TotalDeathCount'], 
    labels=df2['continent'], 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=sns.color_palette("muted")
)
plt.title('Total COVID-19 Deaths by Continent', fontsize=16)
plt.tight_layout()
plt.savefig('deaths_by_continent.png', dpi=300)
plt.close()

conn.close()
print("Images generated successfully.")
