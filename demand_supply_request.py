import requests
import os
import pandas as pd

api_key = "zPamRVTDhbg4KhhEqRRCD6Xod9QWpyyp3geG7uWj"



def fetch_demand_data(start_time, end_time,grid_operator="NE", frequency="daily"):
    url = f"https://api.eia.gov/v2/electricity/rto/daily-region-sub-ba-data/data/?frequency={frequency}&data[0]=value&start={start_time}&end={end_time}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    data = data['response']['data']

    # Convert the data into a pandas DataFrame
    df = pd.DataFrame(data)
    df.to_csv('Demand.csv')

def fetch_supply_data(start_time,end_time):
    url = f"https://api.eia.gov/v2/electricity/rto/daily-region-data/data/?frequency=daily&data[0]=value&facets[respondent][]=ERCO&start=2024-11-01&end=2024-11-16&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={api_key}"
    response=requests.get(url)
    data=response.json()
    data=data['response']['data']
    df=pd.DataFrame(data)
    df.to_csv("Supply.csv")

def annual_capacity_by_state():
    url=f"https://api.eia.gov/v2/electricity/state-electricity-profiles/capability/data/?frequency=annual&data[0]=capability&start=2023&end=2023&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={api_key}"
    response=requests.get(url)
    data=response.json()
    data=data['response']['data']
    df=pd.DataFrame(data)
    df.to_csv("capacity.csv")
fetch_supply_data("2024-11-04","2024-11-04")

annual_capacity_by_state()
