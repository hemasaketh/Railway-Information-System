import pandas as pd
import sqlite3

#load the csv data into dataframe
df = pd.read_csv('trains.csv')

#connect to sqlite database
conn = sqlite3.connect('trains_.db')

#write dataframe to SQLite table
df.to_sql('trains_',conn,if_exists='replace',index=False)


#creating a cursor object
cursor = conn.cursor()


# Step 7: Define and execute a query
query = 'SELECT * FROM trains_ LIMIT 10'  # Example query to select the first 10 rows
cursor.execute(query)


rows = cursor.fetchall()
for row in rows:
    print(row)



#commit and close
conn.commit()
conn.close()




