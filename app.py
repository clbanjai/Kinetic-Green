from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the trained models
logistic_model = joblib.load('models/logistic_model.pkl')
cox_model = joblib.load('models/cox_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Retrieve input data from the form
        input_data = {
            'Supply_Demand_Ratio': float(request.form['supply_demand_ratio']),
            'Weather_Index': float(request.form['weather_index']),
            'Grid_Score': float(request.form['grid_score']),
            'Average_Wait_Time': float(request.form['average_wait_time']),
            # Add other variables here
        }

        # Convert input data to DataFrame
        input_df = pd.DataFrame([input_data])

        # Logistic Regression Prediction
        ppa_prob = logistic_model.predict_proba(input_df)[0][1]
        ppa_prediction = 'likely' if ppa_prob >= 0.5 else 'unlikely'

        # Cox Model Prediction
        survival_function = cox_model.predict_survival_function(input_df)
        completion_prob = 1 - survival_function.loc[24].values[0]  # Adjust the time as needed

        # Render the results template with predictions
        return render_template(
            'result.html',
            ppa_prob=ppa_prob,
            ppa_prediction=ppa_prediction,
            completion_prob=completion_prob,
            input_data=input_data
        )

if __name__ == '__main__':
    app.run(debug=True)
