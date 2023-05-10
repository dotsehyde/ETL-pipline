import pandas as pd
import sqlite3

# Extract data
data = pd.read_csv("./gameSale.csv")
population = pd.read_csv("./population.csv")


# Transform data
data = data.drop_duplicates() # Remove duplicates
population = population.drop_duplicates() # Remove duplicates
data = data.rename(columns={"NA_Sales": "America", "EU_Sales": "Europe","JP_Sales":"Asia","Other_Sales":"ROW","Global_Sales":"Total_sales"}) # Rename columns
data = data.dropna() # Remove rows with missing values
# convert the 'YeR' column from float to int
data['Year'] = data['Year'].astype(int)


# reduce the columns to only the ones we need
population = population[['Name','Population']]
# remove the rows with 'NaN' value
population = population.dropna()
population["Population"] = pd.to_numeric(population["Population"].str.replace(",", "")) # Change data type
 
# Add North America and South America population
americas_df = population.loc[(population['Name'] == 'North America') | (population['Name'] == 'South America')]
americas_total = americas_df.sum(numeric_only=True)
americas_total['Name'] = 'America'
population.drop(population[(population['Name'] == 'North America') | (population['Name'] == 'South America')].index, inplace=True)

# Add Africa and Australia population to ROW
row_df = population.loc[(population['Name'] == 'Africa') | (population['Name'] == 'Australia')]
row_total = row_df.sum(numeric_only=True)
row_total['Name'] = 'ROW'
population.drop(population[(population['Name'] == 'Africa') | (population['Name'] == 'Australia')].index, inplace=True)

# Add ROW and Americas to population
population.loc[len(population)+1] = row_total
population.loc[len(population)+1] = americas_total

# Create a pivot table with Name as index, and Population as values
population_pivot = pd.pivot_table(population, index=None, columns='Name', values='Population', aggfunc='sum')

# Remove the Name index from the pivot table
population_pivot.index.name = None

# Rename the columns to remove the Name label
population_pivot.columns.name = None

# Reset the index to make Population a column
population = population_pivot.reset_index()

# Output the DataFrame
print(population)

# Load data
conn = sqlite3.connect("gameData.db")
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE games
             (Rank INT PRIMARY KEY,
             Name TEXT,
             Platform TEXT,
             Year INT,
             Genre TEXT,
             Publisher TEXT,
             America REAL,
             Europe REAL,
             Asia REAL,
             ROW REAL,
             Total_sales REAL);''')

# Table for population
c.execute('''CREATE TABLE population
            (America REAL,
             Asia REAL,
             Europe REAL,
             ROW REAL
             );''')

# Load data
# Save to SQLite DB
data.to_sql("games", conn, if_exists="replace", index=False)
population.to_sql("population", conn, if_exists="replace", index=False)
# Save to csv file
data.to_csv("new_games.csv", index=False)
population.to_csv("new_population.csv", index=False)
# Commit changes and close connection
conn.commit()
conn.close()
