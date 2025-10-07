from dotenv import load_dotenv
import os
import requests
from datetime import date
import pandas as pd
import json


# start date- end date, end date- today
class Extract():
    def __init__(self, d_type):
        self.api_key = self.get_api_key()
        self.rate_limit = 100
        self.d_type = d_type
        self.end_date = date.today()

    def get_api_key():
        load_dotenv()
        donki_key = os.getenv("DONKI_API_KEY")
        return donki_key

    def get_dates(self)->tuple:
        '''keep track of last dates extracted and return the next dates'''
        start = "2025-01-01"
        end = "2025-08-01"
        return start, end
    
    def get_donki_url(self, start, end)->str:
        '''returns api url to get json data of given type'''
        self.d_type = self.d_type.upper()
        if self.d_type not in ['CME', 'GST', 'FLR', 'IPS', 'HSS']:
            return "Error fetching data: Wrong 'type' mentioned..."
        
        url = f"https://api.nasa.gov/DONKI/{type}?startDate={start}&endDate={end}&api_key={self.api_key}"
        return url

    def get_donki_json(type, url)->list: 
        '''returns json output of url given'''
        try:
            response = requests.get(url)
            response.raise_for_status()
            print("Response successful")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error occurred: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error occurred: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error occurred: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected Request error occurred: {e}")
        else:
            data = response.json()
            return data

    # EXTRACT 
    def collect_donki_data(self, type)->list:
        '''orchestration- runs all methods in order to get json data'''
        start, end = self.get_dates()
        url = self.get_donki_url(start=start, end=end, type=type)
        data = self.get_donki_json(type, url)
        return data
    

class Transform():
    def __init__(self, type, json_data):
        self.type = type
        self.json_data = json_data

    def get_dataframe(self): 
        '''transforms json output to dataframe based on type of data'''
        if self.type == 'CME':
            self.parse_cme_data(self.json_data)
        elif self.type == 'GST':
            self.parse_gst_data(self.json_data)
        elif self.type == 'FLR':
            self.parse_flr_data(self.json_data)
        elif self.type == 'IPS':
            self.parse_ips_data(self.json_data)
        else:
            self.parse_hss_data(self.json_data)
    

    def parse_cme_data(self)->object:
        df = pd.json_normalize(self.json_datadata)
        df['cmeAnalyses'] = df['cmeAnalyses'].apply(lambda x: x[0] if x != None else None)

        df_cme = df[['activityID', 'cmeAnalyses']].copy() # to avoid pandas warning- working on subsets better to explixly use copy
        df_cme = pd.json_normalize(df_cme.to_dict(orient='records')) # normalize expects json input so we convert back to dict
        df_cme = df_cme.rename(columns=lambda x: x.replace('cmeAnalyses.', ''))

        df_enlil = df_enlil[['activityID', 'enlilList']].copy() 
        df_enlil['enlilList'] = df_enlil['enlilList'].apply(lambda x: x[0] if x != [] else None)
        df_enlil = pd.json_normalize(df_enlil.to_dict(orient='records'))
        df_enlil = df_enlil.rename(columns=lambda x: x.replace('enlilList.', 'enlil.'))

        df = df.merge(df_cme, on='activityID', how='inner')
        df = df.merge(df_enlil, on='activityID', how='inner')
        return df
        
    def parse_gst_data(self)->object:
        df = pd.json_normalize(self.json_data)
        return df

    def parse_flr_data(self)->object:
        df = pd.json_normalize(self.json_data)
        df['note'] = df['note'].apply(lambda x: None if x == "" else x) # if str is "" then should be None
        return df

    def parse_ips_data(self)->object:
        df = pd.json_normalize(self.json_data)
        return df

    def parse_hss_data(self):
        df = pd.json_normalize(self.json_data)
        return df