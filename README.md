# COVID-19 Data Analysis Project

This is a complete, real-time step-by-step data analysis project involving SQL and a Python Dashboard. 

## Project Structure
- `setup_database.py`: Downloads the real dataset from *Our World in Data* and loads it into an SQLite database (`covid_data.db`).
- `analysis_queries.sql`: Contains the raw SQL queries demonstrating various data aggregations, calculations, and window functions used in this project.
- `dashboard.py`: A Streamlit interactive dashboard that connects to the database, runs SQL queries, and visualizes the results.
- `requirements.txt`: Contains the necessary Python libraries.

## Step-by-Step Instructions to Run

### Step 1: Install Dependencies
Open your terminal (PowerShell or Command Prompt) and navigate to this folder:
```bash
cd "C:\Users\Varshinivelmurugan\OneDrive\Desktop\Covid 19"
pip install -r requirements.txt
```

### Step 2: Set Up the Database
In the same terminal, run the setup script. This will download the current Covid-19 dataset and create a local SQLite database file called `covid_data.db`.
*(Note: Downloading the dataset might take a minute, depending on your internet connection.)*
```bash
python setup_database.py
```

### Step 3: Explore the SQL Queries
Open the `analysis_queries.sql` file in any text editor. It contains all the step-by-step SQL queries you can use to answer specific business questions about the data (e.g., Infection Rates, Death Count). These queries form the core analysis of your project.

### Step 4: Run the Interactive Dashboard
To see the "Dashboard Format" of your completed project, run the Streamlit app. This will start a local server and automatically open a beautiful presentation of your data in your web browser.
```bash
streamlit run dashboard.py
```

## Dashboard Features
- **Global Overview**: Real-time calculated KPIs for Total Cases, Deaths, and Death Percentage globally.
- **Top Infections**: Plotly bar chart displaying the 20 countries with the highest infection rates compared to their population.
- **Continent Breakdown**: A pie chart of total deaths by continent.
- **Raw Data Viewer**: Easy access to scroll through the raw SQL result sets.

