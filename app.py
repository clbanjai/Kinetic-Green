import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
import os

# Load your dataset
data = pd.read_csv('data/your_dataset.csv')

# Define predictor variables and target variable
predictor_vars = [
    'Supply_Demand_Ratio',
    'Weather_Index',
    'Grid_Score',
    'Average_Wait_Time',
    # Add other variables here
]

X = data[predictor_vars]
y = data['PPA_Secured']

# Handle missing values
X = X.fillna(X.mean())
y = y.fillna(y.mode()[0])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
logistic_model = LogisticRegression(max_iter=1000)
logistic_model.fit(X_train, y_train)

# Ensure 'models' directory exists
if not os.path.exists('models'):
    os.makedirs('models')

# Save the logistic regression model
joblib.dump(logistic_model, 'models/logistic_model.pkl')
print("Logistic regression model saved successfully.")
