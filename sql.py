import pandas as pd
import sqlite3

# Load the CSV data into a DataFrame
df = pd.read_csv('trains.csv')

# Connect to SQLite database
conn = sqlite3.connect('trains_.db')

# Write DataFrame to SQLite table
df.to_sql('trains_', conn, if_exists='replace', index=False)

# Create a cursor object
cursor = conn.cursor()

# Get column names and their types dynamically
cursor.execute('PRAGMA table_info(trains_)')
columns = cursor.fetchall()

# Step 1: Define and execute a query to convert all text columns to lowercase
for column in columns:
    column_name, column_type = column[1], column[2]
    
    # Only convert text-based columns to lowercase (TEXT or VARCHAR)
    if 'TEXT' in column_type.upper():
        query = f"UPDATE trains_ SET {column_name} = LOWER({column_name}) WHERE {column_name} IS NOT NULL"
        cursor.execute(query)

# Commit the changes
conn.commit()

# Step 2: Verify the changes by fetching and printing the first 10 rows
cursor.execute('SELECT * FROM trains_ LIMIT 10')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()
