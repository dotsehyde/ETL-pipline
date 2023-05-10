-- Retrieve the total population of the Americas
SELECT SUM(Population) as Total_Population
FROM population
WHERE Name = 'Americas';

-- Retrieve the top 10 best-selling games of all-time
SELECT Name, Total_sales
FROM games
ORDER BY Total_sales DESC
LIMIT 10;

-- Retrieve the total sales for each publisher in Europe
SELECT Publisher, SUM(Europe) as Total_Sales
FROM games
WHERE Year > 2010
GROUP BY Publisher;

-- Retrieve the total sales for each platform in Asia
SELECT Platform, SUM(Asia) as Total_Sales
FROM games
WHERE Genre = 'Role-Playing'
GROUP BY Platform;

-- Retrieve the total sales for each year
SELECT Year, SUM(Total_sales) as Total_Sales
FROM games
GROUP BY Year;

-- Retrieve the average sales per game by platform:

SELECT Platform, AVG(Total_sales) as Average_Sales
FROM games
GROUP BY Platform;
