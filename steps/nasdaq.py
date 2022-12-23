import os
import pandas, requests, datetime
import calendar as cal
from .get_date import get_date

class dividend_calendar:
    #class attributes 
    calendars = [] 
    url = 'https://api.nasdaq.com/api/calendar/dividends'
    hdrs =  {'Accept': 'application/json, text/plain, */*',
                 'DNT': "1",
                 'Origin': 'https://www.nasdaq.com/',
                 'Sec-Fetch-Mode': 'cors',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'}
    def __init__(self, year, month, tickers):

            #instance attributes
            self.year = int(year)
            self.month = int(month)
            self.tickers = list(tickers)
        
    def date_str(self, day):
        date_obj = datetime.date(self.year, self.month, day)
        date_str = date_obj.strftime(format='%Y-%m-%d')     
        return date_str

    def scraper(self, date_str):

        params = {'date': date_str}
        page=requests.get(self.url,headers=self.hdrs,params=params)
        dictionary = page.json()
        return dictionary
        
    def dict_to_df(self, dicti):
        ''' 
        Converts the JSON dictionary into a pandas dataframe
        Appends the dataframe to calendars class attribute         

        Parameters
        ----------
        dicti : Output from the scraper method as input.

        Returns
        -------
        calendar : Dataframe of stocks with that exdividend date

        Appends the dataframe to calendars class attribute

        If the date is formatted correctly, it will append a 
        dataframe to the calendars list (class attribute).  
        Otherwise, it will return an empty dataframe.         
        '''

        rows = dicti.get('data').get('calendar').get('rows')
        calendar = pandas.DataFrame(rows)
        self.calendars.append(calendar)
        return calendar


    def calendars_dict(self, day):

        day = int(day)
        date_str = self.date_str(day)      
        dictionary = self.scraper(date_str)
        self.dict_to_df(dictionary)          
        return dictionary

    def select_tickers(self):
        for i in self.dictionary:
            symbol = i['symbol']
        if symbol not in self.tickers:
            del i
        

# if __name__ == '__main__':
    
dates = get_date()
for i in dates:
    year, month = i 
    print('processing :{}-{}'.format(year ,month))
    tickers = []
    with open (r'steps\US_Ticker.csv' , mode='r') as f:
        for ticker in f:
            tickers.append(ticker)

    days_in_month = cal.monthrange(year, month)[1]

    target_month = dividend_calendar(year,month,tickers)

    function = lambda days: target_month.calendars_dict(days)


    iterator = list(range(1, days_in_month+1))
                    
    objects = list(map(function, iterator))

    concat_df = pandas.concat(target_month.calendars)
    

    drop_df = concat_df.dropna(how='any')

    final_df = drop_df.set_index('companyName')
    
    final_df.to_csv('outputs/dividends_calendar{}{}.csv'.format(year,month),date_format='%Y-%m-%d')
