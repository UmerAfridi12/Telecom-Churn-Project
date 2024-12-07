document.addEventListener('DOMContentLoaded', () => {
    // Churn Prediction Form Submission
    const predictForm = document.getElementById('churn-form');

    predictForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

        // Collecting form data
        const formData = new FormData(predictForm);
        const formValues = {};

        formData.forEach((value, key) => {
            if (key === 'tenure' || key === 'SeniorCitizen') {
                formValues[key] = parseInt(value);
            } else if (key === 'MonthlyCharges' || key === 'TotalCharges') {
                formValues[key] = parseFloat(value);
            } else {
                formValues[key] = value;
            }
        });

        // POST request to the Flask backend for churn prediction
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formValues)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').textContent = data.error ? `Error: ${data.error}` : `Prediction: ${data.prediction}`;
        })
        .catch(error => {
            document.getElementById('result').textContent = `Error: ${error.message}`;
        });
    });

// LLM Query Form Submission
const queryForm = document.getElementById('queryForm');

queryForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default submission

    const question = document.getElementById('question').value;

    // POST request to the Flask backend for generating SQL query
    fetch('http://127.0.0.1:5000/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
    })
    .then(response => response.json())
    .then(data => {
        // Display both SQL query and result
        if (data.error) {
            document.getElementById('queryResult').textContent = `Error: ${data.error}`;
        } else {
            document.getElementById('queryResult').innerHTML = `
                <strong>Result:</strong><br>${JSON.stringify(data.result, null, 2)}<br><br>
                <strong>SQL Query:</strong><br>${data.sql_query}
                
            `;
        }
    })
    .catch(error => {
        document.getElementById('queryResult').textContent = `Error: ${error.message}`;
    });
});

});
