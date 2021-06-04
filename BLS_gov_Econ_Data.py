import pandas as pd
import numpy as np
import os 
import requests
import json
import sys



class Econ_Monitor():

    """
    Pull Economic Data from BLS.gov using their API
    """

    def __init__(self):
        self.headers = {'Content-type': 'application/json'}
        self.api_url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
        self.data_dic = {}

    def get_data(self,series:list, start:str, end:str):
        
        # pull data
        data = json.dumps({"seriesid": series,"startyear": start, "endyear":end})
        p = requests.post(self.api_url, data=data, headers=self.headers)
        json_data = json.loads(p.text)
        # parse json output
        for ser,num in zip(series,range(0,len(series))):
            df = pd.json_normalize(json_data['Results']['series'][num]['data'])
            df['Month'] = df['period'].apply(lambda x: x[1:])
            df['Date'] = df['year'].astype(str) + '-' +df['Month'].astype(str)
            df['Date'] = pd.to_datetime(df['Date'])
            df['value'] = df['value'].astype(float)
            df.sort_values('Date',inplace=True)
            
            # Add DataFrame to dic
            self.data_dic[ser] = df


    def plot(self,series:str,title:str):
        #Plot Values
        self.data_dic[series].sort_values('Date').plot(x='Date',y='value',figsize=(15,10),title=title)


if __name__ == "__main__":
    # Meant to be used as a module, but can easily be modifed to run in command line.
    pass
