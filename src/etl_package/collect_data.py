from dotenv import load_dotenv
import os
import requests
from datetime import date
import pandas as pd
import json

load_dotenv()
donki_key = os.getenv("DONKI_API_KEY")

# get start/end/type(user input) -- get url(start/end/type) -- data from url(url) -- parse required data(type/data) -- 

def get_donki_url(start, end, type)->str:
    if type not in ['CME', 'GST', 'FLR', 'IPS', 'HSS']:
        return "Error fetching data: Wrong 'type' mentioned..."
    
    url = f"https://api.nasa.gov/DONKI/{type}?startDate={start}&endDate={end}&api_key={donki_key}"
    return url

def get_donki_json(type, url)->list: # returns json output 
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data

def get_dates()->tuple:
    start = "2015-01-01"
    end = "2025-08-01"
    return start, end

# EXTRACT
def collect_donki_data(type):
    start, end = get_dates()
    url = get_donki_url(start=start, end=end, type=type)
    json_data = get_donki_json(type, url)
    with open(file=f"{type.lower()}.json", mode="w") as file:
        file.write(str(json_data))
    return json_data

# -----------------------------------------------------------------------------------

def parse_cme_data(data)->object:
    df = pd.json_normalize(data)
    df['cmeAnalyses'] = df['cmeAnalyses'].apply(lambda x: x[0] if x != [] else None)

    df_cme = df[['activityID', 'cmeAnalyses']].copy() # to avoid pandas warning- working on subsets better to explixly use copy
    df_cme = pd.json_normalize(df_cme.to_dict(orient='records')) # normalize expects json input so we convert back to dict
    df_cme = df_cme.rename(columns=lambda x: x.replace('cmeAnalyses.', '')) # to avoid long names of columns- cmeAnalyses already has unique fields

    df_enlil = df_cme[['activityID', 'enlilList']].copy()
    df_enlil = df_enlil.dropna() # some float (nan) values need to be eliminated to run apply next
    df_enlil['enlilList'] = df_enlil['enlilList'].apply(lambda x: x[0] if x != [] else None)
    df_enlil = pd.json_normalize(df_enlil.to_dict(orient='records'))
    df_enlil = df_enlil.rename(columns=lambda x: x.replace('enlilList.', 'enlil.'))

    df = pd.merge(df, df_cme, on='activityID', how='inner')
    df = pd.merge(df, df_enlil, on='activityID', how='inner')
    return df

def parse_gst_data(data)->object:
    df = pd.json_normalize(data)
    return df

def parse_flr_data(data)->object:
    df = pd.json_normalize(data)
    df['note'] = df['note'].apply(lambda x: None if x == "" else x) # if str is "" then should be None
    return df

def parse_ips_data(data)->object:
    df = pd.json_normalize(data)
    return df

def parse_hss_data(data):
    df = pd.json_normalize(data)
    return df

# TRANSFORM
def get_dataframe(type, data)->object: # transforms json output
    if type == 'CME':
        return parse_cme_data(data)
    elif type == 'GST':
        return parse_gst_data(data)
    elif type == 'FLR':
        return parse_flr_data(data)
    elif type == 'IPS':
        return parse_ips_data(data)
    else:
        return parse_hss_data(data)

