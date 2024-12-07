import mysql.connector
import pandas as pd

# Connecting to MySQL
conn = mysql.connector.connect(
    host='hostname',        
    user='username',    
    password='password',
    database='telecom_db'     
)

# Creating a cursor object
cursor = conn.cursor()

# Fetch all table names
cursor.execute("SHOW TABLES")
tables = [table[0] for table in cursor.fetchall()]

# Dictionary to store data from each table
database_data = {}

# Loop through each table and fetch all its data
for table in tables:
    query = f"SELECT * FROM {table}"
    cursor.execute(query)
    
    # Fetching all rows from the current table
    rows = cursor.fetchall()
    
    # Getting column names for the current table
    column_names = [i[0] for i in cursor.description]
    
    # Creating a DataFrame for better data handling
    table_data = pd.DataFrame(rows, columns=column_names)
    
    # Store DataFrame in dictionary with the table name as key
    database_data[table] = table_data

# Closing the connection
conn.close()

# Display the retrieved data (optional)
for table, data in database_data.items():
    print(f"\nData from {table} table:")
    print(data)

