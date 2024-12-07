import os
import pymysql
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
from dotenv import load_dotenv
import google.generativeai as genai

# Initialize the app and load environment variables
app = Flask(__name__)
CORS(app)
load_dotenv()

# Load the trained model pipeline
model_pipeline = joblib.load('model_pipeline.pkl')

# Configure GenAI Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Google Gemini Model and provide queries as responses
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the MySQL database
def read_sql_query(sql):
    conn = pymysql.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="telecom_db"
    )
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Define the prompt for converting questions to SQL
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database is named `telecom_db` and has the following tables and columns:

    - `Customers` (columns: customerID, gender, SeniorCitizen, Partner, Dependents)
    - `Accounts` (columns: tenure, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges)
    - `Services` (columns: PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies)
    - `Churn` (columns: customerID, Churn)

    Examples of queries:
    - How many customers have churned?
      SQL: SELECT COUNT(*) FROM Churn WHERE Churn = "Yes";
    - List all customers with high MonthlyCharges.
      SQL: SELECT customerID, MonthlyCharges FROM Accounts WHERE MonthlyCharges > 100;

    Ensure the SQL output does not include any ``` in the beginning or end and does not have the word "sql" in the output.
    """
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract data from the request
        input_data = request.get_json()

        # Validate input data
        required_fields = [
            "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", 
            "PhoneService", "MultipleLines", "InternetService", 
            "OnlineSecurity", "OnlineBackup", "DeviceProtection", 
            "TechSupport", "StreamingTV", "StreamingMovies", 
            "Contract", "PaperlessBilling", "PaymentMethod", 
            "MonthlyCharges", "TotalCharges"
        ]
        
        for field in required_fields:
            if field not in input_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Convert input data into a DataFrame
        input_df = pd.DataFrame([input_data])

        # Preprocess the input DataFrame
        input_df = pd.get_dummies(input_df)

        # Ensure the DataFrame has the same columns as the training set
        input_df = input_df.reindex(columns=model_pipeline.named_steps['xgbclassifier'].feature_names_in_, fill_value=0)

        # Make predictions
        prediction = model_pipeline.predict(input_df)

        # Return the prediction in a JSON response
        return jsonify({'prediction': str(prediction[0])})

    except Exception as e:
        return jsonify({'error': str(e)}), 500   

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # Get the question from the request
        question = request.get_json().get('question', '')

        # Generate SQL query from the question using the LLM
        sql_query = get_gemini_response(question, prompt)

        # Execute the SQL query
        result = read_sql_query(sql_query)

        # Return the SQL query and result in a JSON response
        return jsonify({'sql_query': sql_query, 'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
