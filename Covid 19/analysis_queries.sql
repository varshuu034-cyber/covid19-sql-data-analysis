-- COVID-19 Data Analysis Queries
-- This file contains all the SQL queries used to analyse the Covid-19 Dataset.
-- We are using SQLite dialect.

-- 1. Select basic data that we are going to be starting with
SELECT location, date, total_cases, new_cases, total_deaths, population
FROM covid_deaths
WHERE continent IS NOT NULL
ORDER BY location, date;


-- 2. Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid in your country
SELECT location, date, total_cases, total_deaths, 
       (CAST(total_deaths AS FLOAT) / total_cases) * 100 AS DeathPercentage
FROM covid_deaths
WHERE continent IS NOT NULL
  AND location LIKE '%States%' 
ORDER BY location, date;


-- 3. Total Cases vs Population
-- Shows what percentage of the population got covid
SELECT location, date, population, total_cases, 
       (CAST(total_cases AS FLOAT) / population) * 100 AS PercentPopulationInfected
FROM covid_deaths
WHERE continent IS NOT NULL
ORDER BY location, date;


-- 4. Countries with Highest Infection Rate Compared to Population
SELECT location, population, 
       MAX(total_cases) AS HighestInfectionCount, 
       MAX((CAST(total_cases AS FLOAT) / population)) * 100 AS PercentPopulationInfected
FROM covid_deaths
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY PercentPopulationInfected DESC
LIMIT 20;


-- 5. Countries with Highest Death Count per Population
SELECT location, 
       MAX(CAST(total_deaths AS INT)) AS TotalDeathCount
FROM covid_deaths
WHERE continent IS NOT NULL 
GROUP BY location
ORDER BY TotalDeathCount DESC
LIMIT 20;


-- 6. Breakdown by Continent
-- Showing continents with the highest death count
SELECT continent, 
       MAX(CAST(total_deaths AS INT)) AS TotalDeathCount
FROM covid_deaths
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY TotalDeathCount DESC;


-- 7. Global Numbers (Overall Totals)
SELECT SUM(new_cases) AS total_cases, 
       SUM(CAST(new_deaths AS INT)) AS total_deaths, 
       (SUM(CAST(new_deaths AS FLOAT)) / SUM(new_cases)) * 100 AS DeathPercentage
FROM covid_deaths
WHERE continent IS NOT NULL;


-- 8. Total Population vs Vaccinations
-- Shows Percentage of Population that has received at least one Covid Vaccine
-- Since SQLite doesn't support complex variable assignments easily, we use CTEs.

WITH PopvsVac AS (
    SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
           SUM(CAST(vac.new_vaccinations AS INT)) OVER (
               PARTITION BY dea.location 
               ORDER BY dea.location, dea.date
           ) AS RollingPeopleVaccinated
    FROM covid_deaths dea
    JOIN covid_vaccinations vac
      ON dea.location = vac.location
     AND dea.date = vac.date
    WHERE dea.continent IS NOT NULL
)
SELECT *, (CAST(RollingPeopleVaccinated AS FLOAT) / population) * 100 AS PercentVaccinated
FROM PopvsVac;


-- 9. Create View to store data for later visualizations
-- (In SQLite, DROP VIEW IF EXISTS is safe)
DROP VIEW IF EXISTS PercentPopulationVaccinated;
CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
       SUM(CAST(vac.new_vaccinations AS INT)) OVER (
           PARTITION BY dea.location 
           ORDER BY dea.location, dea.date
       ) AS RollingPeopleVaccinated
FROM covid_deaths dea
JOIN covid_vaccinations vac
  ON dea.location = vac.location
 AND dea.date = vac.date
WHERE dea.continent IS NOT NULL;
