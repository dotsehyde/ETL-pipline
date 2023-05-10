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
americas_total['Name'] = 'Americas'
print(americas_total)
population.drop(population[(population['Name'] == 'North America') | (population['Name'] == 'South America')].index, inplace=True)

# Add Africa and Australia population to ROW
row_df = population.loc[(population['Name'] == 'Africa') | (population['Name'] == 'Australia')]
row_total = row_df.sum(numeric_only=True)
row_total['Name'] = 'ROW'
population.drop(population[(population['Name'] == 'Africa') | (population['Name'] == 'Australia')].index, inplace=True)

# Add ROW and Americas to population
population.loc[len(population)+1] = row_total
population.loc[len(population)+1] = americas_total



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
            (Name TEXT,
             Population REAL);''')

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
