document.getElementById('churn-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    // Collect form data
    const customerData = {
        CreditScore: parseInt(document.getElementById('creditScore').value),
        Geography: parseInt(document.getElementById('geography').value),
        Gender: parseInt(document.getElementById('gender').value),
        Age: parseInt(document.getElementById('age').value),
        Tenure: parseInt(document.getElementById('tenure').value),
        Balance: parseFloat(document.getElementById('balance').value),
        NumOfProducts: parseInt(document.getElementById('numOfProducts').value),
        HasCrCard: parseInt(document.getElementById('hasCrCard').value),
        IsActiveMember: parseInt(document.getElementById('isActiveMember').value),
        EstimatedSalary: parseFloat(document.getElementById('estimatedSalary').value)
    };

    try {
        // Send a POST request to your API
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(customerData)
        });

        // Parse the JSON response
        const result = await response.json();

        // Display the result
        document.getElementById('result').innerHTML = `
            <h3>Churn Probability: ${result.churn_probability.toFixed(2)}</h3>
            <h3>Churn Class: ${result.churn_class === 1 ? 'Likely to Churn' : 'Not Likely to Churn'}</h3>
        `;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = '<p style="color: red;">Error predicting churn. Please try again later.</p>';
    }
});
