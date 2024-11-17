import pandas as pd
import numpy as np
from datetime import timedelta

# Step 1: Load Data
# Load county population data
population_df = pd.read_csv('texas_county_population.csv')

# Read the ERCOT Interconnection Queue data
queue = pd.read_csv('ERCOT_Interconnection_Queue.csv')

# Convert date columns to datetime format
date_columns = ['Screening Study Started', 'Screening Study Complete', 'FIS Requested', 'FIS Approved']
for col in date_columns:
    queue[col] = pd.to_datetime(queue[col], errors='coerce')

# Fill missing FIS Approved dates with two years from now
two_years_from_now = pd.Timestamp.now() + timedelta(days=2 * 365)
queue['FIS Approved'] = queue['FIS Approved'].fillna(two_years_from_now)

# Calculate the difference in days for the screening study
queue['Screening Study Duration (days)'] = (queue['Screening Study Complete'] - queue['Screening Study Started']).dt.days

# Calculate the difference in days for FIS approval
queue['FIS Approval Duration (days)'] = (queue['FIS Approved'] - queue['FIS Requested']).dt.days

# Handle missing or invalid values by coercing to numeric
queue['Screening Study Duration (days)'] = pd.to_numeric(queue['Screening Study Duration (days)'], errors='coerce')
queue['FIS Approval Duration (days)'] = pd.to_numeric(queue['FIS Approval Duration (days)'], errors='coerce')

# Calculate average durations by County
wait_times_df = queue.groupby('County').agg(
    Avg_Screening_Study_Duration=('Screening Study Duration (days)', 'mean'),
    Avg_FIS_Approval_Duration=('FIS Approval Duration (days)', 'mean')
).reset_index()

# Load supply capacity data
supply_df = pd.read_csv('Supply.csv')

# Load solar resource data
solar_df = pd.read_csv('texas_solar_production.csv')

# Step 2: Prepare DataFrames for Merging

# Standardize county names in population_df
population_df['County'] = population_df['County'].str.replace(' County', '', regex=False)

# Since supply_df and solar_df have state-level data, we need to distribute them to counties

# a. Calculate per capita supply
total_supply_mwh = supply_df['value'].sum()  # Assuming 'value' is in megawatthours
total_population = population_df['Population'].sum()
per_capita_supply_mwh = total_supply_mwh / total_population

# Add 'Supply_MWh' column to population_df
population_df['Supply_MWh'] = population_df['Population'] * per_capita_supply_mwh

# b. Calculate per capita solar capacity factor
average_capacity_factor = solar_df['capacity_factor'].mean()

# Assign the average capacity factor to all counties
population_df['Capacity_Factor'] = average_capacity_factor

# Step 3: Merge DataFrames on 'County' column
data_df = population_df.merge(wait_times_df, on='County', how='left')

# Step 4: Calculate Per Capita Electricity Consumption
state_total_demand = 400000  # GWh/year (example value)
state_population = population_df['Population'].sum()

per_capita_consumption = state_total_demand / state_population  # GWh per person per year

# Estimate County-Level Electricity Demand
data_df['County_Demand_GWh'] = data_df['Population'] * per_capita_consumption

# Step 5: Prepare Wait Time Data

# Calculate total wait time in days
data_df['Total_Wait_Days'] = data_df['Avg_Screening_Study_Duration'] + data_df['Avg_FIS_Approval_Duration']

# Handle missing values
data_df['Total_Wait_Days'] = data_df['Total_Wait_Days'].fillna(0)

# Convert to years
data_df['Wait_Time_Years'] = data_df['Total_Wait_Days'] / 365

# Step 6: Normalize and Scale Scores

# a. Average Wait Times Scoring
def wait_time_score(wait_time_years):
    if wait_time_years >= 10:
        return 0
    elif wait_time_years >= 8:
        return 0.5
    elif wait_time_years >= 6:
        return 1
    elif wait_time_years >= 4:
        return 1.5
    elif wait_time_years >= 2:
        return 2
    else:
        return 2.5

data_df['Wait_Time_Score'] = data_df['Wait_Time_Years'].apply(wait_time_score)

# b. Electricity Demand Score
demand_min = data_df['County_Demand_GWh'].min()
demand_max = data_df['County_Demand_GWh'].max()

data_df['Normalized_Demand'] = (data_df['County_Demand_GWh'] - demand_min) / (demand_max - demand_min)
data_df['Demand_Score'] = data_df['Normalized_Demand'] * 2.5

# c. Supply Capacity Score
supply_min = data_df['Supply_MWh'].min()
supply_max = data_df['Supply_MWh'].max()

data_df['Normalized_Supply'] = (data_df['Supply_MWh'] - supply_min) / (supply_max - supply_min)
data_df['Supply_Score'] = data_df['Normalized_Supply'] * 2.5

# d. Solar Resource Score
# Add slight random variations to Capacity_Factor for demonstration purposes
np.random.seed(42)
data_df['Capacity_Factor'] += np.random.normal(0, 0.5, size=len(data_df))

# Ensure Capacity_Factor stays within realistic bounds (e.g., 0% to 100%)
data_df['Capacity_Factor'] = data_df['Capacity_Factor'].clip(lower=0, upper=100)

solar_min = data_df['Capacity_Factor'].min()
solar_max = data_df['Capacity_Factor'].max()

data_df['Normalized_Solar'] = (data_df['Capacity_Factor'] - solar_min) / (solar_max - solar_min)
data_df['Solar_Score'] = data_df['Normalized_Solar'] * 2.5

# Step 7: Calculate Total Scores
data_df['Total_Score'] = data_df['Wait_Time_Score'] + data_df['Demand_Score'] + data_df['Supply_Score'] + data_df['Solar_Score']

# Step 8: Prepare Data for Interactive Map
output_df = data_df[['County', 'Total_Score', 'Wait_Time_Score', 'Demand_Score', 'Supply_Score', 'Solar_Score']]

print(output_df)
# Export to CSV
output_df.to_csv('county_scores.csv', index=False)

# Alternatively, export to JSON
output_df.to_json('county_scores.json', orient='records')
