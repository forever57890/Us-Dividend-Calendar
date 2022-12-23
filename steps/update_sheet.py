import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def to_google_sheet():

    scopes = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
 
    credentials = ServiceAccountCredentials.from_json_keyfile_name(r"steps\crypto-price-369400-b2f32852ff4c.json", scopes)
    client = gspread.authorize(credentials)
    
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/14NGjPzI-qxUlzy7fSJR3kBu6I85I7vQ4Umz_n2Tp5KM/edit#gid=0")
    worksheet = sheet.get_worksheet(0)


    df = pd.read_json(r'outputs\merged.json')
    
    worksheet.update([df.columns.values.tolist()]+ df.values.tolist())

    

to_google_sheet()