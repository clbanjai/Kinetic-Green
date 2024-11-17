import pandas as pd

# Load the county scores data from JSON file
county_scores_df = pd.read_json('county_scores.json')

# Load the county coordinates data from CSV file
coordinates_df = pd.read_csv('texas_county_coordinates.csv')

# Standardize the county names in coordinates_df to match county_scores_df
coordinates_df['County'] = coordinates_df['County'].str.replace(' County', '', regex=False)

# Merge the county scores data with coordinates data on the 'County' column
merged_df = county_scores_df.merge(coordinates_df, on='County', how='left')

# Print the merged DataFrame to verify the results
print(merged_df.head())

# Save the merged data back to a new JSON file
merged_df.to_json('county_scores_with_coords.json', orient='records')

print("Merging complete. The merged data is saved as 'county_scores_with_coords.json'.")
