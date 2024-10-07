from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import numpy as np

app = FastAPI()

# Define the input data model
class CustomerData(BaseModel):
    CreditScore: int
    Geography: int  
    Gender: int  
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int 
    IsActiveMember: int 
    EstimatedSalary: float

# Load the saved model
model = tf.keras.models.load_model('churn_model.h5') 

@app.post("/predict")
async def predict_churn(data: CustomerData):
    # Convert input data to a NumPy array
    input_data = np.array([[
        data.CreditScore, data.Geography, data.Gender, data.Age,
        data.Tenure, data.Balance, data.NumOfProducts,
        data.HasCrCard, data.IsActiveMember, data.EstimatedSalary
    ]])

    # Make a prediction
    prediction = model.predict(input_data)
    
    # If the model returns a scalar (single prediction), handle it
    if isinstance(prediction, np.ndarray):
        prediction = prediction.item()  # Convert single-item array to scalar
    
    # You can apply a threshold if desired
    churn_class = 1 if prediction >= 0.5 else 0
    
    # Return the prediction as probability and classification
    return {"churn_probability": float(prediction), "churn_class": churn_class}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
