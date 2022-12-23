import pandas as pd
import datetime
import os

import json
import csv
from steps.get_date import get_date


x = get_date()
year1, month1 = x[0]
year2,month2 = x[1]
year3,month3 = x[2]

csvFile = r'outputs\dividends_calendar{}{}.csv.'.format(year3,month3)
csvFile2 = r'outputs\dividends_calendar{}{}.csv.'.format(year2,month2)
csvFile3 = r'outputs\dividends_calendar{}{}.csv.'.format(year1,month1)
os.remove(csvFile2)
os.remove(csvFile3)


jsonFile = r'outputs\merged.json'
tickers = []
with open(r'steps\US_Ticker.csv', newline='') as f:
    
    reader = csv.reader(f)
    for i in reader:
        tickers.append(i[0])

    
def make_json (csvFile,jsonFile):
    data = []
    with open (csvFile,mode='r') as f:
        csvReader = csv.DictReader(f)
        
        for i in csvReader:
            if i['symbol'] in tickers:  
                if datetime.datetime.strptime(i['dividend_Ex_Date'],'%m/%d/%Y') >= datetime.datetime.today():
                    print(i['symbol'],i['dividend_Ex_Date'])
                    data.append(i)
                else:
                    print('time passed  ' ,'symbol :' , i['symbol'] , 'date : ',i['dividend_Ex_Date'])



    with open (jsonFile, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


make_json(csvFile,jsonFile)






