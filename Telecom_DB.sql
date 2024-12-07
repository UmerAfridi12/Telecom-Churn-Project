USE telecom_db

CREATE TABLE Customers (
    customerID VARCHAR(255) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen BOOLEAN,
    Partner VARCHAR(3),
    Dependents VARCHAR(3)
);

CREATE TABLE Services (
    serviceID INT AUTO_INCREMENT PRIMARY KEY,
    customerID VARCHAR(255),
    PhoneService VARCHAR(3),
    MultipleLines VARCHAR(50),
    InternetService VARCHAR(50),
    OnlineSecurity VARCHAR(50),
    OnlineBackup VARCHAR(50),
    DeviceProtection VARCHAR(50),
    TechSupport VARCHAR(50),
    StreamingTV VARCHAR(50),
    StreamingMovies VARCHAR(50),
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
);

CREATE TABLE Accounts (
    accountID INT AUTO_INCREMENT PRIMARY KEY,
    customerID VARCHAR(255),
    tenure INT,
    Contract VARCHAR(50),
    PaperlessBilling VARCHAR(50),
    PaymentMethod VARCHAR(50),
    MonthlyCharges DECIMAL(10, 2),
    TotalCharges DECIMAL(10, 2),
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
);

CREATE TABLE Churn (
    churnID INT AUTO_INCREMENT PRIMARY KEY,
    customerID VARCHAR(255),
    Churn VARCHAR(3),
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
);

SELECT * FROM Customers LIMIT 10;

SELECT COUNT(*) AS total_customers FROM Customers;

SELECT S.InternetService, SUM(A.MonthlyCharges) AS TotalRevenue
FROM Services S
JOIN Accounts A ON S.customerID = A.customerID
GROUP BY S.InternetService;

SELECT C.customerID, C.gender, A.tenure, A.MonthlyCharges, Ch.Churn
FROM Customers C
JOIN Accounts A ON C.customerID = A.customerID
JOIN Churn Ch ON C.customerID = Ch.customerID
WHERE Ch.Churn = 'Yes';

SELECT S.InternetService, Ch.Churn, COUNT(*) AS churned_customers
FROM Customers C
JOIN Services S ON C.customerID = S.customerID
JOIN Churn Ch ON C.customerID = Ch.customerID
WHERE Ch.Churn = 'Yes'
GROUP BY S.InternetService;

SELECT A.Contract, Ch.Churn, COUNT(*) AS churned_per_contract
FROM Customers C
JOIN Accounts A ON C.customerID = A.customerID
JOIN Churn Ch ON C.customerID = Ch.customerID
WHERE Ch.Churn = 'Yes'
GROUP BY A.Contract;

SELECT A.PaymentMethod, Ch.Churn, COUNT(*) AS churned_per_payment_method
FROM Customers C
JOIN Accounts A ON C.customerID = A.customerID
JOIN Churn Ch ON C.customerID = Ch.customerID
WHERE Ch.Churn = 'Yes'
GROUP BY A.PaymentMethod;

SELECT Contract, 
       AVG(MonthlyCharges) AS avg_monthly_charges, 
       AVG(TotalCharges) AS avg_total_charges 
FROM Accounts 
GROUP BY Contract;

SELECT AVG(A.MonthlyCharges) AS avg_monthly_charges, Ch.Churn, A.Contract
FROM Customers C
JOIN Accounts A ON A.customerID = C.customerID
JOIN Churn Ch ON C.customerID = Ch.customerID
WHERE Ch.Churn = 'YES'
GROUP BY A.Contract;

SELECT AVG(A.TotalCharges) AS avg_total_charges, Ch.Churn, A.Contract
FROM Customers C
JOIN Accounts A ON A.customerID = C.customerID
JOIN Churn Ch ON C.customerID = Ch.customerID
WHERE Ch.Churn = 'YES'
GROUP BY A.Contract;


