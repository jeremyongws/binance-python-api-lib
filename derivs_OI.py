import json
import requests
import pdb
from datetime import datetime
import csv

DERIV_URL = 'https://dapi.binance.com/futures/data/openInterestHist?'
# FUT_URL = 'https://fapi.binance.com/futures/data/openInterestHist?'
interval = '1d'
contract_type = 'PERPETUAL'

def timestamp_to_date(timestamp):
    time_format = '%m-%d-%Y %H:%M:%S'
    #API returns ms, python uses s
    return datetime.utcfromtimestamp(timestamp/1000).strftime(time_format)


def getOIData(pair,interval='1d'):
    symbol,api = pair
    if api == "dapi":
        req_url = DERIV_URL
    # elif api == "fapi":
    #     req_url = FUT_URL
    else:
        return "ERROR! Bad API Request url."
    print(req_url)
    req_url += 'pair='+symbol+'&period='+interval+'&limit=1000'+'&contractType='+contract_type
    res = requests.get(req_url)
    data = res.json()
    # pdb.set_trace()
    formatted_data = []
    for day_data in data:
        #Convert open & close time to human readable format
        pdb.set_trace()
        day_data[0],day_data[6] = timestamp_to_date(day_data[0]),timestamp_to_date(day_data[6])
        #remove some useless data at end of array
        day_data = day_data[:-3 or None]
        #add pair to array
        day_data.insert(0,symbol)
        formatted_data.append(day_data)
    return formatted_data

with open("shitcoin_pairs.csv","r") as pairs_csv:
     csv_reader = csv.reader(pairs_csv, delimiter=',')
     pairs = list(csv_reader)[1:] #remove header row

results = []
for pair in pairs:
    pair_data = getOIData(pair)
    results.extend(pair_data)
    print(f'{pair[0]} data pulled.')


titles = [
"Pair","Open Time","Open","High","Low","Close","Volume","Close Time",
"Quote/Base Asset Volume","No. of Trades"]

with open('data.csv','w+') as f:
    writer = csv.writer(f)
    writer.writerow(titles)
    writer.writerows(results)
    print("Data written to data.csv")
