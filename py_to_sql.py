import pandas as pd
import mysql.connector

data = r"C:\Users\Hp\Desktop\Python\Telecom Customer Churn\Telco-Customer-Churn.xlsx - in.csv"

df = pd.read_csv(data)

# Replace empty strings or spaces in TotalCharges with NaN
df['TotalCharges'] = df['TotalCharges'].replace(r'^\s*$', None, regex=True)

# Drop missing and duplicate rows
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

customers_df = df[['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents']]

services_df = df[['customerID', 'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
                  'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']]

accounts_df = df[['customerID', 'tenure', 'Contract', 'PaperlessBilling', 'PaymentMethod',
                  'MonthlyCharges', 'TotalCharges']]

churn_df = df[['customerID', 'Churn']]

conn = mysql.connector.connect(host='hostname', username='username', password='password', database='telecom_db')  
my_cursor = conn.cursor()

insert_customers = """
INSERT INTO Customers (customerID, gender, SeniorCitizen, Partner, Dependents)
VALUES (%s, %s, %s, %s, %s)
"""
my_cursor.executemany(insert_customers, customers_df.values.tolist())

insert_services = """
INSERT INTO Services (customerID, PhoneService, MultipleLines, InternetService, OnlineSecurity,
                      OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
my_cursor.executemany(insert_services, services_df.values.tolist())

insert_accounts = """
INSERT INTO Accounts (customerID, tenure, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
my_cursor.executemany(insert_accounts, accounts_df.values.tolist())

insert_churn = """
INSERT INTO Churn (customerID, Churn)
VALUES (%s, %s)
"""
my_cursor.executemany(insert_churn, churn_df.values.tolist())

conn.commit()
conn.close()

print("Data successfully inserted into MySQL tables in batches!")
