import datetime 
from dateutil.relativedelta import *



def get_date():
    date = datetime.date.today()
    # date = date.strftime("%Y-%m-%d")
    date_1 = date + relativedelta(months = +1)
    date_2 = date + relativedelta(months = +2)
    date = str(date)
    date_1 = str(date_1)
    date_2 = str(date_2)
    
    list =[date, date_1, date_2]
    dates = []
    for date in list:
        year, month ,day = date.split('-')
        year = int(year)
        month = int(month)
        dates.append((year, month))
    return dates
