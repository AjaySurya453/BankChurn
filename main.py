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

# Load your trained model
model = tf.keras.models.load_model('churn_model.h5')

@app.post("/predict")
async def predict_churn(data: CustomerData):
    # Prepare input data for the model
    input_data = np.array([[
        data.CreditScore, data.Geography, data.Gender, data.Age,
        data.Tenure, data.Balance, data.NumOfProducts,
        data.HasCrCard, data.IsActiveMember, data.EstimatedSalary
    ]])

    # Get the prediction from the model
    prediction = model.predict(input_data)[0][0]  # Get probability

    # Return the prediction as JSON
    return {"churn_probability": float(prediction)}

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
